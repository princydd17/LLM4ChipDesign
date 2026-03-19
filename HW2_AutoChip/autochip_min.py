from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL_ID = "meta/llama-3.1-8b-instruct"


@dataclass(frozen=True)
class SimResult:
    ok: bool
    compile_ok: bool
    returncode: int
    stdout: str
    stderr: str
    cmd: str


@dataclass(frozen=True)
class Candidate:
    iteration: int
    response_num: int
    verilog_text: str
    sim: SimResult


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _extract_verilog(text: str, module_name: str) -> str:
    """
    Extract a synthesizable Verilog snippet from an LLM response.
    Prefers fenced ```verilog blocks, otherwise falls back to raw text.
    Ensures the top module name matches `module_name` by simple substitution
    if the response uses `top_module`.
    """
    fenced = re.findall(r"```(?:verilog|systemverilog)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE)
    code = fenced[0].strip() if fenced else text.strip()

    # Common HDLs in benchmarks use top_module. Normalize.
    code = re.sub(r"\bmodule\s+top_module\b", f"module {module_name}", code)
    return code.strip() + "\n"


def simulate_iverilog(
    *,
    workdir: Path,
    dut_path: Path,
    tb_path: Path,
    top: Optional[str] = None,
) -> SimResult:
    workdir.mkdir(parents=True, exist_ok=True)
    sim_out = workdir / "sim.out"

    cmd_compile = ["iverilog", "-g2012", "-o", str(sim_out), str(tb_path), str(dut_path)]
    if top:
        cmd_compile.insert(1, "-s")
        cmd_compile.insert(2, top)

    cp = _run(cmd_compile, cwd=workdir)
    compile_ok = cp.returncode == 0
    if not compile_ok:
        return SimResult(
            ok=False,
            compile_ok=False,
            returncode=cp.returncode,
            stdout=cp.stdout,
            stderr=cp.stderr,
            cmd=" ".join(cmd_compile),
        )

    cmd_run = ["vvp", str(sim_out)]
    rp = _run(cmd_run, cwd=workdir)
    ok = rp.returncode == 0
    return SimResult(
        ok=ok,
        compile_ok=True,
        returncode=rp.returncode,
        stdout=rp.stdout,
        stderr=rp.stderr,
        cmd=" ".join(cmd_compile) + " && " + " ".join(cmd_run),
    )


def _make_client(*, base_url: str, api_key: str):
    from openai import OpenAI

    return OpenAI(base_url=base_url, api_key=api_key)


def generate_candidates(
    *,
    base_url: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    n: int,
    max_tokens: int = 1400,
) -> list[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Set it to your NVIDIA/OpenAI-compatible key (e.g. nvapi-...)."
        )

    client = _make_client(base_url=base_url, api_key=api_key)
    outs: list[str] = []
    for _ in range(n):
        resp = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
        )
        outs.append(resp.choices[0].message.content or "")
    return outs


def _score(sim: SimResult) -> tuple[int, int, int]:
    """
    Lower is better.
    Priority: pass > compile_ok > shorter stderr.
    """
    if sim.ok:
        return (0, 0, 0)
    if not sim.compile_ok:
        return (2, 0, len(sim.stderr))
    return (1, sim.returncode, len(sim.stderr) + len(sim.stdout))


def verilog_loop(
    *,
    design_prompt: str,
    module_name: str,
    tb_path: Path,
    outdir: Path,
    base_url: str = DEFAULT_BASE_URL,
    model_id: str = DEFAULT_MODEL_ID,
    max_iterations: int = 5,
    num_candidates: int = 5,
    top: Optional[str] = None,
) -> Candidate:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "artifacts").mkdir(exist_ok=True)

    system_prompt = (
        "You generate synthesizable SystemVerilog/Verilog that compiles with iverilog (-g2012). "
        "Output ONLY the final code (prefer a single fenced ```verilog block)."
    )

    feedback: str = ""
    best: Optional[Candidate] = None

    for it in range(max_iterations):
        user_prompt = design_prompt
        if feedback:
            user_prompt = (
                design_prompt
                + "\n\n---\nThe previous attempt failed. Fix using this simulator feedback:\n"
                + feedback
            )

        raw_responses = generate_candidates(
            base_url=base_url,
            model_id=model_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            n=num_candidates,
        )

        candidates: list[Candidate] = []
        for i, raw in enumerate(raw_responses):
            code = _extract_verilog(raw, module_name)
            dut_path = outdir / "artifacts" / f"{module_name}_it{it}_c{i}.sv"
            dut_path.write_text(code)

            workdir = outdir / "artifacts" / f"sim_it{it}_c{i}"
            sim = simulate_iverilog(workdir=workdir, dut_path=dut_path, tb_path=tb_path, top=top)
            cand = Candidate(iteration=it, response_num=i, verilog_text=code, sim=sim)
            candidates.append(cand)

        candidates.sort(key=lambda c: _score(c.sim))
        best_this = candidates[0]

        # Save a compact log for the iteration.
        log = {
            "iteration": it,
            "base_url": base_url,
            "model_id": model_id,
            "num_candidates": num_candidates,
            "best": {
                "response_num": best_this.response_num,
                "ok": best_this.sim.ok,
                "compile_ok": best_this.sim.compile_ok,
                "cmd": best_this.sim.cmd,
                "stderr_tail": best_this.sim.stderr[-2000:],
                "stdout_tail": best_this.sim.stdout[-2000:],
            },
        }
        (outdir / f"iteration_{it}.json").write_text(json.dumps(log, indent=2))

        if best is None or _score(best_this.sim) < _score(best.sim):
            best = best_this

        if best_this.sim.ok:
            (outdir / f"{module_name}.sv").write_text(best_this.verilog_text)
            return best_this

        # Prepare feedback from the best failing candidate.
        feedback = textwrap.dedent(
            f"""\
            Command:
            {best_this.sim.cmd}

            STDERR:
            {best_this.sim.stderr[-4000:]}

            STDOUT:
            {best_this.sim.stdout[-2000:]}
            """
        ).strip()

    assert best is not None
    (outdir / f"{module_name}.sv").write_text(best.verilog_text)
    return best


def ensure_tooling() -> None:
    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        raise RuntimeError("iverilog/vvp not found. Install Icarus Verilog (iverilog).")


#!/usr/bin/env python3
"""LLM + Yosys optimization loop (Part 3).

Supports either:
- Direct OpenAI API (`OPENAI_API_KEY`)
- Gateway-style OpenAI-compatible endpoint (e.g., Portkey / NYU):
  `PORTKEY_API_KEY` (or `NYU_GATEWAY_API_KEY`) + `PORTKEY_BASE_URL`
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from run_yosys import synthesize  # noqa: E402

try:
    from openai import OpenAI
except ImportError as e:
    raise SystemExit("Install the OpenAI SDK: pip install openai") from e

MODE_TARGETS = {
    "area": 14,
    "delay": 6,
    "balanced": 10,
}


def build_system_prompt(delay_target: int, top: str) -> str:
    return (
        "You are an expert digital circuit designer. "
        f"The top module MUST be named exactly `{top}` with this port list: "
        f"module {top}(output [7:0] sum, output cout, input [7:0] a, input [7:0] b); "
        "Do not use a different top name (e.g. adder, adder8). "
        "You may add internal submodules (FA, etc.) as needed. "
        "Generate synthesizable Verilog only—prefer structural gates or assign-based logic that Yosys accepts; "
        "no testbench, no `timescale`, no markdown, no prose outside the module(s). "
        f"Target at most {delay_target} logic levels when STA reports levels; otherwise minimize cell count. "
        "Respond with ONLY Verilog source code—no markdown fences, no explanation."
    )


def _strip_markdown_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        t = "\n".join(lines).strip()
    return t


def llm_generate(
    client: Any,
    model: str,
    system_text: str,
    history: list[dict[str, str]],
) -> str:
    messages: list[dict[str, str]] = [{"role": "system", "content": system_text}]
    messages.extend(history)
    response = client.chat.completions.create(model=model, messages=messages)
    return _strip_markdown_fences(response.choices[0].message.content or "")


def build_feedback_prompt(
    iteration: int,
    ppa: dict[str, Any],
    best_ppa: dict[str, Any],
    delay_target: int,
) -> str:
    return (
        f"Iteration {iteration} synthesis results:\n"
        f"  - cell_count: {ppa.get('cell_count')}\n"
        f"  - logic_levels: {ppa.get('logic_levels')}\n"
        f"  - area_um2: {ppa.get('area_um2')}\n"
        f"Best so far: cells={best_ppa.get('cell_count')}, "
        f"levels={best_ppa.get('logic_levels')}, area_um2={best_ppa.get('area_um2')}\n"
        f"Delay target (levels): {delay_target}. "
        "Propose a new 8-bit adder Verilog implementation that improves PPA. "
        "Only output Verilog."
    )


def run_loop(
    baseline_verilog: str,
    top: str,
    out_dir: Path,
    client: Any,
    model: str,
    delay_target: int,
    max_iter: int,
    liberty: str | None,
) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    system_text = build_system_prompt(delay_target, top)
    history: list[dict[str, str]] = [
        {
            "role": "user",
            "content": (
                f"Here is an 8-bit adder baseline (Verilog). The synthesis top is `{top}` — "
                f"your design MUST keep that exact top module name and the same ports as this baseline. "
                "Your next message must be Verilog only.\n\n" + baseline_verilog
            ),
        }
    ]
    base_file = out_dir / "_baseline_for_synth.v"
    base_file.write_text(baseline_verilog, encoding="utf-8")
    ppa0, _ = synthesize(str(base_file), top, liberty=liberty)
    print(f"Baseline synthesis: {ppa0}", flush=True)

    best_ppa: dict[str, Any] = dict(ppa0)
    best_code = baseline_verilog
    results: list[dict[str, Any]] = [{"iteration": 0, "ppa": ppa0, "note": "golden baseline copy"}]

    for i in range(1, max_iter + 1):
        print(f"\n=== Iteration {i} ===", flush=True)
        try:
            verilog = llm_generate(client, model, system_text, history)
        except Exception as e:
            print(f"LLM error: {e}", flush=True)
            break

        fname = out_dir / f"candidate_{i}.v"
        fname.write_text(verilog, encoding="utf-8")

        try:
            ppa, _log = synthesize(str(fname), top, liberty=liberty)
        except Exception as e:
            print(f"Synthesis failed: {e}", flush=True)
            history.append({"role": "assistant", "content": verilog})
            history.append(
                {
                    "role": "user",
                    "content": "Synthesis failed. Fix syntax and Verilog semantics. Output Verilog only.",
                }
            )
            continue

        print(
            f"  cells={ppa.get('cell_count')} levels={ppa.get('logic_levels')} "
            f"area_um2={ppa.get('area_um2')}",
            flush=True,
        )
        results.append({"iteration": i, "ppa": ppa, "file": str(fname)})

        nc = ppa.get("cell_count")
        nl = ppa.get("logic_levels")
        bc = best_ppa.get("cell_count")
        if nc is not None and bc is not None:
            level_ok = nl is None or nl <= delay_target
            if level_ok and nc < bc:
                best_ppa = {
                    "cell_count": nc,
                    "logic_levels": nl,
                    "area_um2": ppa.get("area_um2"),
                }
                best_code = verilog
                print("  *** new best (lower cell count under delay target) ***", flush=True)

        history.append({"role": "assistant", "content": verilog})
        history.append(
            {"role": "user", "content": build_feedback_prompt(i, ppa, best_ppa, delay_target)}
        )

    return best_code, best_ppa, results


def main() -> None:
    ap = argparse.ArgumentParser(description="LLM–Yosys adder optimization loop")
    ap.add_argument(
        "--baseline",
        default=str(Path(__file__).resolve().parents[2] / "part1" / "golden" / "RCA8.v"),
        help="Baseline Verilog file",
    )
    ap.add_argument("--top", default="RCA8", help="Top module name")
    ap.add_argument(
        "--mode",
        choices=("area", "delay", "balanced"),
        default="balanced",
        help="Maps to delay level targets 14 / 6 / 10",
    )
    ap.add_argument("--out", type=Path, default=Path("run_out"), help="Output directory")
    ap.add_argument("--max-iter", type=int, default=10)
    ap.add_argument("--model", default=os.environ.get("OPTIMIZE_MODEL", "gpt-4o-mini"))
    ap.add_argument(
        "--base-url",
        default=os.environ.get("PORTKEY_BASE_URL"),
        help="Optional OpenAI-compatible base URL (e.g. NYU Portkey gateway)",
    )
    ap.add_argument("--liberty", default=None, help="Path to nangate45.lib (optional)")
    args = ap.parse_args()

    # Credential precedence:
    # 1) Gateway key vars for OpenAI-compatible gateways
    # 2) Standard OpenAI key
    # 3) Explicit fallback key var if user prefers
    api_key = (
        os.environ.get("PORTKEY_API_KEY")
        or os.environ.get("NYU_GATEWAY_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
    )
    if not api_key:
        print(
            "Set one of PORTKEY_API_KEY / NYU_GATEWAY_API_KEY / OPENAI_API_KEY in the environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    delay_target = MODE_TARGETS[args.mode]
    baseline = Path(args.baseline).read_text(encoding="utf-8")
    if args.base_url:
        print(f"Using gateway base URL: {args.base_url}", flush=True)
        client = OpenAI(api_key=api_key, base_url=args.base_url)
    else:
        client = OpenAI(api_key=api_key)

    liberty = args.liberty
    if liberty is None:
        cand = _SCRIPT_DIR / "nangate45.lib"
        if cand.is_file():
            liberty = str(cand)

    best_v, best_ppa, log = run_loop(
        baseline,
        args.top,
        args.out,
        client,
        args.model,
        delay_target,
        args.max_iter,
        liberty,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "best_adder.v").write_text(best_v, encoding="utf-8")
    out_json = {"best_ppa": best_ppa, "iterations": log, "mode": args.mode, "delay_target": delay_target}
    (args.out / "optimization_log.json").write_text(json.dumps(out_json, indent=2), encoding="utf-8")
    print("\nBest PPA:", best_ppa)


if __name__ == "__main__":
    main()

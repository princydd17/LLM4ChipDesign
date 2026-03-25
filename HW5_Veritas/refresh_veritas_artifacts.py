#!/usr/bin/env python3
"""
One-shot: build decoder_2x4 bench/tab, oracle-check, copy artifacts;
emit adder_5-bit.v from existing adder_5-bit.bench.

Run from repo root or HW5_Veritas:
  python3 HW5_Veritas/refresh_veritas_artifacts.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HW5 = Path(__file__).resolve().parent
ROOT = HW5.parent
NB = HW5 / "veritas_hw.ipynb"


def _strip_trailing_call(src: str, pattern: str) -> str:
    s = src.rstrip()
    s = re.sub(pattern, "", s, flags=re.MULTILINE | re.DOTALL)
    return s.strip() + "\n"


def _load_cell(nb: dict, predicate) -> int:
    for i, c in enumerate(nb["cells"]):
        s = "".join(c.get("source", []))
        if predicate(s):
            return i
    raise RuntimeError("cell not found")


def main() -> int:
    os.chdir(HW5)
    nb = json.loads(NB.read_text(encoding="utf-8"))

    i_cnf = _load_cell(nb, lambda s: "def cnf_to_bench(inputs,outputs,cnf)" in s)
    i_sim = _load_cell(nb, lambda s: "def bench_simulator(design,typ)" in s and "class BenchCircuit" in s)
    i_v = _load_cell(nb, lambda s: "def bench_to_verilog(design,typ)" in s)

    src_cnf = _strip_trailing_call(
        "".join(nb["cells"][i_cnf]["source"]),
        r"\ncnf_to_bench\(inputs,outputs,cnf\)\s*$",
    )
    src_sim = _strip_trailing_call(
        "".join(nb["cells"][i_sim]["source"]),
        r"\nbench_simulator\(design,typ\)\s*$",
    )
    src_v = _strip_trailing_call(
        "".join(nb["cells"][i_v]["source"]),
        r"\nbench_to_verilog\(design,\s*typ\)\s*$",
    )

    g: dict = {"__name__": __name__, "Path": Path}
    exec(compile(src_cnf, str(NB) + ":cnf_to_bench", "exec"), g)
    exec(compile(src_sim, str(NB) + ":bench_sim", "exec"), g)

    # --- Decoder 2x4 ---
    design, typ = "decoder", "2x4"
    g["design"], g["typ"] = design, typ
    g["inputs"] = "A0,A1"
    g["outputs"] = "Y0,Y1,Y2,Y3"
    g["cnf"] = (HW5 / "decoder_2x4.cnf").read_text(encoding="utf-8")
    print("--- cnf_to_bench decoder 2x4 ---", file=sys.stderr)
    g["cnf_to_bench"](g["inputs"], g["outputs"], g["cnf"])

    print("--- truth_table decoder 2x4 ---", file=sys.stderr)
    g["bench_simulator"](design, typ)

    exec(compile(src_v, str(NB) + ":verilog_dec", "exec"), g)
    print("--- bench_to_verilog decoder 2x4 ---", file=sys.stderr)
    g["bench_to_verilog"]("decoder", "2x4")

    # --- adder 5-bit Verilog ---
    g["design"], g["typ"] = "adder", "5-bit"
    bench5 = HW5 / "adder_5-bit.bench"
    if not bench5.is_file():
        print(f"error: missing {bench5} (run Part IV or generate bench first)", file=sys.stderr)
        return 2
    print("--- bench_to_verilog adder 5-bit ---", file=sys.stderr)
    exec(compile(src_v, str(NB) + ":verilog", "exec"), g)
    g["bench_to_verilog"]("adder", "5-bit")

    # --- Oracle + copy ---
    sys.path.insert(0, str(HW5))
    from oracle_veritas import (
        copy_run_artifacts,
        oracle_decoder_binary_inputs,
        validate_against_oracle,
    )

    tab_dec = HW5 / "decoder_2x4_tab.csv"
    ok, msg = validate_against_oracle(
        tab_dec,
        ["A0", "A1"],
        ["Y0", "Y1", "Y2", "Y3"],
        oracle_decoder_binary_inputs(2, ["Y0", "Y1", "Y2", "Y3"]),
    )
    print("Oracle decoder 2x4:", "PASS" if ok else "FAIL", "-", msg)
    if not ok:
        return 1

    dest = HW5 / "artifacts" / "decoder_2x4"
    copy_run_artifacts("decoder", "2x4", dest, repo_root=ROOT)
    print("Artifacts copied to", dest.resolve())

    # Refresh adder artifacts so 5-bit .v is included
    dest5 = HW5 / "artifacts" / "adder_5-bit"
    copy_run_artifacts("adder", "5-bit", dest5, repo_root=ROOT)
    print("Artifacts copied to", dest5.resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

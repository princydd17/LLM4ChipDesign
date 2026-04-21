#!/usr/bin/env python3
"""Run Yosys synthesis and parse PPA-related metrics from log output.

Without a Liberty file, Yosys `stat` reports cell counts but not um^2 area or
STA logic levels. Place `nangate45.lib` next to this script (or pass --liberty)
for full metrics.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any


def _yosys_synth_commands(verilog_file: str, top_module: str, liberty: str | None) -> list[str]:
    v = os.path.abspath(verilog_file)
    # Escape for Yosys: paths with spaces must be quoted inside the -p string.
    v_quoted = v.replace("\\", "/")
    if " " in v_quoted:
        v_read = f'read_verilog "{v_quoted}"'
    else:
        v_read = f"read_verilog {v_quoted}"

    cmds = [
        v_read,
        f"hierarchy -check -top {top_module}",
        "proc; opt; techmap; opt",
    ]
    if liberty and os.path.isfile(liberty):
        lib = os.path.abspath(liberty).replace("\\", "/")
        lib_q = f'"{lib}"' if " " in lib else lib
        cmds.append(f"dfflibmap -liberty {lib_q}")
        cmds.append(f"abc -liberty {lib_q}")
        cmds.append(f"stat -liberty {lib_q}")
    else:
        cmds.append("stat")
    return cmds


def synthesize(
    verilog_file: str,
    top_module: str,
    liberty: str | None = None,
) -> tuple[dict[str, Any], str]:
    env = os.environ.copy()
    cmds = _yosys_synth_commands(verilog_file, top_module, liberty)
    script = "; ".join(cmds)
    result = subprocess.run(
        ["yosys", "-p", script],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    log = result.stdout + result.stderr
    ppa = parse_stats(log)
    if result.returncode != 0 or (
        ppa.get("cell_count") is None
        and ("ERROR:" in log or "error:" in log.lower())
    ):
        raise RuntimeError(
            f"yosys failed (exit {result.returncode}). Last log lines:\n"
            + "\n".join(log.splitlines()[-12:])
        )
    return ppa, log


def parse_stats(log: str) -> dict[str, Any]:
    ppa: dict[str, Any] = {"area_um2": None, "cell_count": None, "logic_levels": None}

    m = re.search(r"Chip area for module.*?:\s+([\d.]+)", log)
    if m:
        ppa["area_um2"] = float(m.group(1))

    m = re.search(r"Number of cells:\s+(\d+)", log)
    if m:
        ppa["cell_count"] = int(m.group(1))

    if ppa["cell_count"] is None:
        for line in log.splitlines():
            s = line.strip()
            if re.match(r"^\d+\s+cells\s*$", s):
                ppa["cell_count"] = int(s.split()[0])

    m = re.search(
        r"Longest topological path.*?\(\s*(\d+)\s*levels?\s*\)",
        log,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        ppa["logic_levels"] = int(m.group(1))

    return ppa


def main() -> None:
    ap = argparse.ArgumentParser(description="Synthesize one Verilog file with Yosys and print JSON metrics.")
    ap.add_argument("verilog_file", help="Path to .v file")
    ap.add_argument("top_module", help="Top module name (e.g. RCA8)")
    ap.add_argument(
        "--liberty",
        default=None,
        help="Optional path to .lib (e.g. nangate45.lib) for area + STA depth",
    )
    args = ap.parse_args()
    liberty = args.liberty
    if liberty is None:
        here = os.path.dirname(os.path.abspath(__file__))
        cand = os.path.join(here, "nangate45.lib")
        if os.path.isfile(cand):
            liberty = cand

    ppa, _log = synthesize(args.verilog_file, args.top_module, liberty=liberty)
    print(json.dumps(ppa, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Plot cell count and logic levels vs iteration from optimization_log.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise SystemExit("Install matplotlib: pip install matplotlib") from e


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("optimization_log", type=Path, help="optimization_log.json")
    ap.add_argument("-o", "--output", type=Path, default=Path("ppa_trajectory.pdf"))
    args = ap.parse_args()

    data = json.loads(args.optimization_log.read_text(encoding="utf-8"))
    iters = [r["iteration"] for r in data["iterations"] if "ppa" in r]
    cells = [r["ppa"]["cell_count"] for r in data["iterations"] if "ppa" in r]
    levels = [r["ppa"].get("logic_levels") for r in data["iterations"] if "ppa" in r]

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 5))
    ax1.plot(iters, cells, marker="o", color="steelblue")
    ax1.set_ylabel("Cell count")
    ax1.grid(True)

    # logic_levels may be None — matplotlib will break; use masked or skip
    lv_num = [x if x is not None else float("nan") for x in levels]
    ax2.plot(iters, lv_num, marker="s", color="firebrick")
    ax2.set_ylabel("Logic levels")
    ax2.set_xlabel("Iteration")
    ax2.grid(True)

    plt.suptitle("LLM–Yosys optimization trajectory")
    plt.tight_layout()
    out = args.output
    plt.savefig(out, bbox_inches="tight")
    print(f"Wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()

# Part 3 optimization runs

Create one subdirectory per **mode** and/or **starting architecture**, for example:

- `mode_area_rca8/` — `optimize_adder.py --mode area --baseline .../RCA8.v --top RCA8 --out mode_area_rca8`
- `mode_delay_ksa8/`
- `mode_balanced_cla8/`

Each run should include:

- `optimization_log.json`
- `ppa_trajectory.pdf` (from `plot_ppa.py`)
- `best_adder.v`
- Optional: `equiv_log.txt`, simulation log from Iverilog

Use this folder for the **multi-start comparison table** in the final report.

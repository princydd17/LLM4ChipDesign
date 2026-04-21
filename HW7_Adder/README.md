# HW7 — LLM-Based Verilog Adder Generation and Verification

Course project (Parts 1–3): golden RTL → LLM descriptions → LLM Verilog → TB + simulation → Yosys PPA loop.

## Start here

- **`CHECKLIST.md`** — full deliverable list aligned with the project document (§6).
- **`part1/`** — adder selection, golden copies, NL + LLM Verilog placeholders, Part 1 verification template.
- **`part2/`** — testbench + simulation layout and Part 2 analysis template.
- **`part3/yosys/`** — `run_yosys.py`, `optimize_adder.py`, plotting, equiv template, `README.md` for Liberty/Yosys.
- **`reports/FINAL_REPORT_OUTLINE.md`** — structure for the PDF report.

## Submission reminders

- **GitHub only**; invite **weihuax6@gmail.com** if required.
- **No API keys** in the repo (use environment variables / local `.env`, gitignored).
- Notebooks or ChipChat flows should **run end-to-end** after you insert keys locally.

## Golden RTL upstream

The **Verilog-Adders** repo is cloned at repo root: `Verilog-Adders/`. Selected 8-bit golden copies for the default pair are under `part1/golden/`.

# HW7 — LLM-Based Verilog Adder Project — Deliverables Checklist

Document version aligned with **October 17, 2025** project spec (Parts 1–3). Check boxes as you complete items. Golden RTL lives in `Verilog-Adders/` at repo root (cloned from the course link).

---

## Setup (once)

- [x] `Verilog-Adders` present at repo root (or adjust paths in `part1/golden/README.md`).
- [x] `iverilog` / `vvp` installed; optional `gtkwave`.
- [x] **Part 3:** `yosys` installed (`yosys -V`). Optional: download `nangate45.lib` into `part3/yosys/` for area/delay numbers (see `part3/yosys/README.md`).
- [ ] LLM tools available (ChipChat / AutoChip) and API key **not** committed (use env / `.env`).

---

## Part 1 — LLM generation from golden designs

- [x] **Adder selection document** — `part1/ADDER_SELECTION.md` (two **different** architectures; justify choice).
- [x] **Natural language descriptions** — one per selected adder (Part 1 §4.2); store under `part1/nl_descriptions/`.
- [x] **LLM-generated Verilog** — one `.v` (or hierarchical set) per adder from ChipChat/AutoChip (Part 1 §4.3); store under `part1/llm_generated/` (e.g. `rca8_llm.v`, `cla8_llm.v`).
- [x] **Verification report (Part 1)** — `part1/verification_part1.md`: golden vs LLM (ports, hierarchy, style, functional notes, deviations).

**Default pair in this repo:** **RCA8** (ripple carry) + **CLA8** (carry lookahead). Change filenames if you pick different adders.

---

## Part 2 — LLM testbenches + simulation

- [x] **Internal-signal list** — documented per adder (carries, P/G, etc.) before TB generation.
- [x] **LLM-generated testbenches** — with internal checks; `part2/rca8/` and `part2/cla8/` (or your adder names).
- [x] **Simulation logs** — `iverilog` + `vvp` console output or saved logs per design.
- [x] **Analysis report (Part 2)** — `part2/analysis_part2.md` (PASS/FAIL, internal signals, issues, fixes).

---

## Part 3 — Yosys PPA optimization loop

- [x] **Scripts & config** — in `part3/yosys/`: `synth_adder.ys`, `equiv_check.ys` (adapt module names), `constraints.sdc`, `run_yosys.py`, `optimize_adder.py`, optional `plot_ppa.py`.
- [ ] **Liberty file** — `nangate45.lib` (or document alternative; do not commit if huge—use `.gitignore` + instructions).
- [x] **Three optimization modes** — area (delay target ~14 levels), delay (~6), balanced (~10); each with `optimization_log.json` + `ppa_trajectory.pdf` (or `.png`). *(Executed, but currently baseline-only due invalid API key; see `part3/runs/PART3_STATUS.md`)*
- [ ] **Multi-start** — runs from ≥2 baselines (e.g. `RCA8`, `KSA8`, `CLA8`); comparison table in report.
- [ ] **Best designs** — `best_adder.v` per run (or under `part3/runs/<mode>_<baseline>/`).
- [ ] **Verification** — iverilog sim of best design; Yosys `equiv` log vs golden; **Step 6** architecture explanations (LLM text) saved per best design.

---

## Final submission bundle

- [ ] **Final project report** — PDF covering experience, LLM accuracy/limits, TB quality, lessons, recommendations (`reports/Final_Project_Report.pdf` or course name).
- [ ] **GitHub:** invite **weihuax6@gmail.com** if required.
- [ ] **No secrets** — search repo for keys; `.env` gitignored.

---

## Quick status (fill in)

| Section | Status |
|--------|--------|
| Part 1 | ☐ Not started / ☐ In progress / ☑ Done |
| Part 2 | ☐ / ☐ / ☑ |
| Part 3 | ☐ / ☑ / ☐ |
| Final report | ☐ |

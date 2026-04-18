# HW6_LLMPirate

LLMPirate assignment workspace for LLM4ChipDesign.

## Files

- `LLMPirate_Student_Workshop.ipynb` — workshop notebook (run this; course submission name).
- `LLMPirate_Report_Template.md` — report skeleton aligned to the assignment format (if present).
- `runs/` — place exported outputs, logs, and intermediate rewritten RTL files.

## Quick start

1. Open `LLMPirate_Student_Workshop.ipynb`.
2. **API key:** Copy `.env.example` to `.env` in this folder and set `OPENAI_API_KEY` or `NYU_GATEWAY_API_KEY`. Cell **0.3** walks parent directories and loads `.env` when found. Or set `%env OPENAI_API_KEY=...` in a cell above 0.3.
3. Run **0.1 → 0.3** once. In cell **0.2**, **`NOTEBOOK_SKIP_SLOW_LLM_TASKS = True`** (default) skips slow **Task 1** and **Task 2** LLM calls so the rest of the notebook runs quickly; set it to **`False`** when you need those experiments.
4. Run Tasks **1–5** in order. For a **fast** NOR pipeline with formal equivalence, use **Task 3** with canonical NOR while the skip flag is on.
5. Fill in your report with observed outputs.

## Dependencies

Installed by cell **0.1**: `networkx`, `openai`, `portkey-ai`, `python-dotenv`. **Yosys** is optional but recommended for miter+SAT checks (`brew install yosys` on macOS).

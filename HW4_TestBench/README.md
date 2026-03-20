# HW4_TestBench — Enhanced LLM-Aided Testbench Generation

HW4 assignment (deadline: Mar. 14). Automatic Verilog testbench generation with golden reference outputs.

## Setup

- **Environment:** Google Colab (recommended) or local Jupyter/Python
- **Dependencies:** `openai` Python package; Python 3; `iverilog`/`vvp`; `gtkwave` (optional)
- **API key:** Set `OPENAI_API_KEY` to your NVIDIA key (nvapi-...). Do not commit keys.
- **Source notebook:** Start from the provided `Enhanced_LLM_Aided_Testbench_Generation.ipynb` (from course materials).

---

## Required deliverables

| Item | Description |
|------|-------------|
| `testbenchgen_hw.ipynb` | Executed notebook with outputs (template provided) |
| `TestbenchGen_Report.pdf` | Short report (see Report requirements below) |
| Artifact subfolders | `mux/`, `adder/`, `custom/` (generated when you run the notebook) |
| Repo access | Invite `weihuax6@gmail.com` as collaborator |

### Artifact structure (per run)

Each subfolder should contain:
- `testbench_initial.v`
- `golden_model.py`
- `test_patterns_with_golden.json`
- `testbench_final.v`

---

## Assignment checklist

### Part I — Run two tutorial examples (required)

Pick two from the notebook (recommended: one combinational, one arithmetic):

- [ ] Run full pipeline for each; generate all four artifacts
- [ ] Compile and simulate with `iverilog`/`vvp`; show exact command and passing output
- [ ] Show key sections of `testbench_final.v` (expected values, compares, pass/fail messages)

### Part II — Inspect and explain (required)

For **one** of your Part I examples, explain in notebook and report:

- [ ] **golden_model.py:** inputs/outputs and how it computes the reference output
- [ ] **test_patterns_with_golden.json:** fields and how expected outputs are stored
- [ ] **Updater effect:** one concrete before/after diff between `testbench_initial.v` and `testbench_final.v` (e.g., added compares/asserts)

### Part III — Custom module (required)

- [ ] Design a small Verilog module (e.g., priority encoder, saturating adder, small counter, UART TX skeleton)
- [ ] Write a clear natural-language spec (ports, bit-widths, corner cases)
- [ ] Run the pipeline end-to-end; ensure ≥ ~20 patterns (corner cases + randomized)
- [ ] Show passing `iverilog`/`vvp` run with `testbench_final.v`

### Part IV — Bug detection (required)

- [ ] Introduce a small intentional bug in the DUT (swap operands, invert condition, wrong carry)
- [ ] Re-run simulation; show failing output (include error snippet)
- [ ] Fix the DUT; show passing run

---

## Report requirements (TestbenchGen_Report.pdf)

- List the two tutorial examples and your custom module name
- Summarize LLM setup (model, key parameters, prompt choices)
- For each run: DUT interface (ports/widths) and `iverilog`/`vvp` commands
- Part II: short explanation of `golden_model.py` and `test_patterns_with_golden.json`
- Part IV: one failing snippet and final passing confirmation after fix

---

## Folder layout

```
HW4_TestBench/
├── README.md                  # this file
├── testbenchgen_hw.ipynb      # your executed notebook
├── TestbenchGen_Report.pdf    # report
├── mux/                       # Example 1 (2-to-1 mux) artifacts
│   ├── testbench_initial.v
│   ├── golden_model.py
│   ├── test_patterns_with_golden.json
│   └── testbench_final.v
├── adder/                     # Example 2 (4-bit adder) artifacts
│   └── ...
└── custom/                    # Your custom module artifacts
    └── ...
```

---


---

## Important reminders

- Notebook must run top-to-bottom (except adding API key in one place)
- Do not commit API keys or secrets
- Use the PDF checklist before submitting

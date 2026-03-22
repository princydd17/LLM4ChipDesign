# HW5 — Veritas (LLM4ChipDesign)

Correct-by-construction Verilog via **CNF → BENCH → Verilog**, with oracle validation.

## What’s in this folder (keep these)

| File / folder | Purpose |
|---------------|---------|
| **`veritas_hw.ipynb`** | Main notebook — run Steps 0–5, save with outputs for submission. |
| **`../colab-scripts/Veritas_tutorial.ipynb`** | Same content as `veritas_hw.ipynb` (course-style path); uses **`veritas_api_setup.py`** for **NVIDIA `nvapi-...`** keys. |
| **`veritas_api_setup.py`** | **API key / model / base URL** — loaded by `exec()` from the notebook so Jupyter never runs a stale in-memory copy of the setup. |
| **`hw5_config.py`** | Optional duplicate of API helpers (legacy); **`veritas_api_setup.py`** is what the notebook uses. |
| **`report_template.md`** | Outline for `Veritas_Report.pdf` (fill in, then export to PDF). |
| **`requirements.txt`** | `pip install -r requirements.txt` (OpenAI client for API calls). |
| **`.env.example`** | Shows env vars (no real secrets). Copy to `.env` locally if you use one. |
| **`artifacts/`** | Put each run’s outputs here, e.g. `artifacts/adder_3-bit/`, `artifacts/decoder_2x4/`. |

Do **not** commit API keys or `.env` with real keys.

## What you must submit (GitHub)

1. **`veritas_hw.ipynb`** — executed top-to-bottom with outputs.  
2. **Artifacts** — for **each** of the **three** runs (Part I ×2 + Part IV scale-up, or as your instructor interprets “three configurations”):  
   `{design}_{typ}.cnf`, `.bench`, `.csv`, `{design}_{typ}_tab.csv`, `.v` (use subfolders under `artifacts/`).  
3. **`Veritas_Report.pdf`** — export from `report_template.md` (or your editor).  
4. **Invite** `weihuax6@gmail.com` as collaborator on the repo.

## Assignment checklist (what to do)

### Part I — Two tutorial runs (≥1 non-adder)

- Pick **two** different `(DESIGN, TYP)` pairs (e.g. adder + decoder, or multiplexor + subtractor).  
- At least one must **not** be an adder.  
- In the notebook: set `DESIGN` / `TYP`, run LLM CNF → BENCH → sim → Verilog.  
- **Update I/O name lists** for CNF→BENCH when you change design (matches notebook).  
- Save all generated files under `HW5_Veritas/artifacts/...`.

### Part II — Oracle (both Part I runs)

- Use `{design}_{typ}_tab.csv` as truth table from BENCH.  
- Write a small **Python oracle** that matches the **same input order** as the CSV.  
- Record **pass/fail**; if fail, first mismatching row + likely cause (CNF vs naming).

### Part III — Different model (e.g. Gemini)

- Run the pipeline with **another** model (e.g. Gemini via OpenAI-compatible endpoint, or OpenRouter).  
- Note any **prompt / API** changes. Compare behavior vs GPT-style run.

### Part IV — Scale-up

- One **family**, small → **larger** supported size (e.g. 3-bit → 5-bit adder, or 2x4 → 5x32 decoder).  
- Full pipeline + oracle validation.  
- In report: **CNF size** (lines/clauses), **runtime**, **prompt tweaks**.

### Report (`Veritas_Report.pdf`)

- All **three** `(DESIGN, TYP)` configurations.  
- Per run: **I/O names**, **filenames**, **oracle** result.  
- **One paragraph**: why CNF helps correctness-by-construction.

## Setup

```bash
cd HW5_Veritas
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env and set OPENAI_API_KEY (never commit .env)
```

The notebook **auto-loads** `HW5_Veritas/.env` (or `./.env` from the current working directory) via `python-dotenv`. NVIDIA `nvapi-...` keys get the correct base URL + model automatically.

## Removed / not in repo

Older drafts referenced `veritas_homework.py`, PDF copies, and extra notebooks — those are **not** required for submission if you complete everything **inside `veritas_hw.ipynb`**. If you add helper scripts later, document them here.

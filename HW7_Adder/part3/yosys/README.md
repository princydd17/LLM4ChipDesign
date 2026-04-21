# Part 3 — Yosys + LLM optimization

## Files

| File | Purpose |
|------|---------|
| `run_yosys.py` | Synthesize one `.v` file; prints JSON (`cell_count`, optional `area_um2`, `logic_levels`). |
| `optimize_adder.py` | LLM loop with Yosys feedback; writes `best_adder.v` + `optimization_log.json`. |
| `plot_ppa.py` | Plot trajectory from `optimization_log.json`. |
| `synth_adder.ys` | Minimal **example** script (edit `read_verilog` / top). Prefer `run_yosys.py` for arbitrary paths. |
| `constraints.sdc` | ABC timing constraints when using Liberty. |
| `equiv_check_TEMPLATE.ys` | Starting point for `equiv_make` vs golden RTL. |

## Liberty file (optional but recommended for Part 3 metrics)

Download **Nangate 45nm** (or course-provided) `.lib`, save as `nangate45.lib` in this folder.  
If `run_yosys.py` finds `nangate45.lib` here, it passes it to ABC/STA automatically.

Example (if the course URL still works):

```bash
wget -O nangate45.lib "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/master/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib"
```

Without Liberty, `area_um2` and `logic_levels` are often `null`; the loop still tracks **cell count** from `stat`.

## Quick test (no API key)

```bash
cd HW7_Adder/part3/yosys
python3 run_yosys.py ../../part1/golden/RCA8.v RCA8
```

## Optimization loop (requires API key)

```bash
export OPENAI_API_KEY="your_key"
# optional: export OPTIMIZE_MODEL=gpt-4o
python3 optimize_adder.py --mode area --out ../../part3/runs/mode_area_rca8 --top RCA8
python3 plot_ppa.py ../../part3/runs/mode_area_rca8/optimization_log.json -o ../../part3/runs/mode_area_rca8/ppa_trajectory.pdf
```

### Using Portkey / NYU gateway (OpenAI-compatible)

Set gateway env vars (example):

```bash
export PORTKEY_BASE_URL="https://ai-gateway.apps.cloud.rt.nyu.edu/v1"
export PORTKEY_API_KEY="your_gateway_key"
export OPTIMIZE_MODEL="@vertexai/gemini-2.5-pro"
python3 optimize_adder.py --mode area --out ../../part3/runs/mode_area_rca8 --top RCA8
```

`optimize_adder.py` now accepts credentials in this order:
`PORTKEY_API_KEY` -> `NYU_GATEWAY_API_KEY` -> `OPENAI_API_KEY`.

Repeat for `--mode delay`, `--mode balanced`, and different `--baseline` paths for multi-start (e.g. `Verilog-Adders/.../KSA8.v` with `--top KSA8`).

## Equivalence checking

Edit `equiv_check_TEMPLATE.ys` so **golden** and **optimized** tops match your file names, then:

```bash
yosys -s equiv_check.ys
```

## Security

Do **not** commit API keys. `nangate45.lib` may be large; you may omit it from git if the course allows and document where graders can obtain it.

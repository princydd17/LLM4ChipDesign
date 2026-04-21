# Part 2 — Testbench generation + simulation

## Internal signals to verify (fill before TB gen)

### RCA8 (example)

- Inter-stage carries: `c[1]` … `c[7]` (names may differ in LLM netlist—align TB to **your** `llm_generated` RTL).
- Primary: `sum[7:0]`, `cout`.

### CLA8 (example)

- `g[7:0]`, `p[7:0]`, carry-related `c[6:0]` or equivalent; intermediate `e[…]` if exposed.
- Primary: `sum[7:0]`, `cout`.

## Folder layout

| Folder | Contents |
|--------|----------|
| `rca8/` | `*_tb.v`, optional `.vcd`, `sim_log.txt` |
| `cla8/` | same |

## Commands (reference)

```bash
iverilog -o sim_rca8.vvp ../part1/llm_generated/RCA8_llm.v rca8/RCA8_tb.v
vvp sim_rca8.vvp | tee rca8/sim_log.txt
```

Adjust paths to your actual LLM file and testbench names.

## Deliverable

- Saved **simulation logs** and short **analysis** in `analysis_part2.md`.

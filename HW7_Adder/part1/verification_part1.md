# Part 1 — Manual verification (golden vs LLM-generated)

## RCA8

| Check | Golden (`golden/RCA8.v`) | LLM (`llm_generated/RCA8_llm.v`) | Notes |
|--------|---------------------------|---------------------------|--------|
| Top module name | RCA8 | RCA8 | Match |
| Ports (names, widths, direction) | `output [7:0] sum, output cout, input [7:0] a, b` | `output [7:0] sum, output cout, input [7:0] a, b` | Match |
| Submodule hierarchy (e.g. FA) | `FA` submodule + 8 FA instances (`fa0`, `fa[6:1]`, `fa7`) | same structure | Match |
| Internal carries / style | `wire [7:1] c`, structural ripple chain | same | Match |
| Functional equivalence (expected) | Yes | Yes | Compile-check passes |

**Differences and assessment:**
- LLM version uses `1'b0` for initial carry-in instead of unsized `0`; functionally identical and style-safe.
- Gate-level FA equations and ripple wiring are preserved.

---

## CLA8

| Check | Golden (`golden/CLA8.v`) | LLM (`llm_generated/CLA8_llm.v`) | Notes |
|--------|---------------------------|---------------------------|--------|
| Top module name | CLA8 | CLA8 | Match |
| Ports | `output [7:0] sum, output cout, input [7:0] a, b` | same | Match |
| PG / carry network | `PGGen`, `g[7:0]`, `p[7:0]`, `c[7:0]`, `e[35:0]`, `cin=0` | same signals and unrolled carry SOP equations | Match |
| Functional equivalence (expected) | Yes | Yes | Compile-check passes |

**Differences and assessment:**
- LLM version uses `buf (cin, 1'b0)` vs `buf (cin, 0)`; functionally identical.
- Carry equations and sum equations match the golden architecture and structural style.

---

## Summary

- **Acceptable alternatives:** Minor literal-style differences (`0` vs `1'b0`) only; no architectural changes.
- **Issues requiring fix before Part 2:** None found in syntax/port/module checks. Both LLM files compile with `iverilog`.

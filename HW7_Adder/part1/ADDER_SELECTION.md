# Adder selection (Part 1, §4.1)

## Selected architectures

| | Adder 1 | Adder 2 |
|---|---------|---------|
| **Type** | Carry Ripple Adder (RCA) | Carry Lookahead Adder (CLA) |
| **Golden file** | `golden/RCA8.v` | `golden/CLA8.v` |
| **Top module** | `RCA8` | `CLA8` |

## Justification

- **RCA8** — Smallest conceptual step: chained full adders with carry rippling LSB→MSB. Good baseline for comparing LLM explanations and regenerated structure.
- **CLA8** — Uses block generate/propagate and lookahead carry logic in parallel with deeper AND/OR trees. Contrasts clearly with RCA on **delay vs area** and internal signals (e.g. `g`, `p`, `c`).

Together they span **simple sequential carry** vs **parallel carry computation**, which makes Part 2 internal-signal discussion meaningful.

## Architectural differences (summary)

| Aspect | RCA8 | CLA8 |
|--------|------|------|
| Carry path | Linear chain (worst-case delay ~8 stages of carry) | Lookahead equations; carries computed with wider fan-in logic |
| Internal structure | `FA` instances + ripple `c[i]` | `PGGen` for `g`,`p`; dense carry logic then XOR sums |
| Typical trade-off | Fewer gates / simpler layout vs long carry path | More gates / wiring vs shorter logical depth |

*If you change to other adders (e.g. KSA8, CSA8), update this table and file paths under `golden/` and `llm_generated/`.*

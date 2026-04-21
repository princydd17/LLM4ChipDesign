# CLA8 natural language description

## Overall architecture and purpose

The design implements an 8-bit unsigned binary adder using a **Carry Lookahead Adder (CLA)** architecture. It computes:

- `sum[7:0] = a[7:0] + b[7:0]`
- `cout` as carry out after bit 7

Unlike ripple carry, this design computes carries using explicit lookahead equations built from propagate/generate terms.

## Module hierarchy and interfaces

### Submodule: `PGGen`

- Inputs: `a`, `b`
- Outputs: `g`, `p`

Functionality:
- `g = a AND b` (generate)
- `p = a XOR b` (propagate)

### Top module: `CLA8`

- Inputs: `a[7:0]`, `b[7:0]`
- Outputs: `sum[7:0]`, `cout`
- Internal buses/signals:
  - `g[7:0]` generate signals
  - `p[7:0]` propagate signals
  - `c[7:0]` carry signals (`c[7]` drives `cout`)
  - `e[35:0]` intermediate product terms for carry equations
  - `cin` tied to constant `0`

`PGGen pggen[7:0]` computes all per-bit `g` and `p` in parallel.

## Signal flow and datapath

1. Set `cin = 0`.
2. Compute all `g[i]` and `p[i]` for i=0..7.
3. Compute each carry `c[i]` via expanded sum-of-products form:
   - Includes term `cin * p[0] * ... * p[i]`
   - Includes all terms `g[k] * p[k+1] * ... * p[i]` for k=0..i-1
   - Includes direct generate `g[i]`
4. Compute sums:
   - `sum[0] = p[0] XOR cin`
   - `sum[i] = p[i] XOR c[i-1]` for i=1..7
5. Set `cout = c[7]`.

## Key logic operations

- Parallel generate/propagate extraction
- Multi-input AND terms for carry products
- Multi-input OR terms for carry accumulation
- XOR for final sum bits

## Special design features

- Fully structural gate-level style (no behavioral `always` blocks)
- Explicit unrolled carry equations for all 8 bits
- Faster carry computation than ripple carry at the cost of additional logic/wiring complexity and larger fan-in terms

# RCA8 natural language description

## Overall architecture and purpose

The design implements an 8-bit unsigned binary adder using a **Ripple Carry Adder (RCA)** architecture. It computes:

- `sum[7:0] = a[7:0] + b[7:0]`
- `cout` as the final carry out from bit 7

The circuit is purely combinational and built structurally from repeated 1-bit full adder cells.

## Module hierarchy and interfaces

### Submodule: `FA`

- Inputs: `a`, `b`, `cin`
- Outputs: `sum`, `cout`
- Internal signals: `w0`, `w1`, `w2`

Functionality:
- `w0 = a XOR b`
- `sum = w0 XOR cin`
- `w1 = w0 AND cin`
- `w2 = a AND b`
- `cout = w1 OR w2`

This is the standard full-adder equation decomposed into primitive gates.

### Top module: `RCA8`

- Inputs: `a[7:0]`, `b[7:0]`
- Outputs: `sum[7:0]`, `cout`
- Internal carry bus: `c[7:1]`

Instantiation pattern:
1. `fa0` adds bit 0 with carry-in tied to logic `0`.
2. Arrayed instances `fa[6:1]` add bits 1..6, each using previous carry.
3. `fa7` adds bit 7 and produces final `cout`.

## Signal flow and datapath

Carry propagates **serially** from LSB to MSB:

- Stage 0 produces `c[1]`
- Stage 1 consumes `c[1]` and produces `c[2]`
- ...
- Stage 7 consumes `c[7]` and produces `cout`

Each bit’s sum depends on local inputs plus incoming carry from the previous stage.

## Key logic operations

- XOR network generates per-bit sum
- AND/OR network generates carry
- Structural chaining forms the ripple-carry path

## Special design features

- Uses Verilog array instantiation (`FA fa[6:1](...)`) for compact mid-stage wiring
- Fully structural gate-level style through `FA` submodule
- Simplicity-focused architecture with straightforward correctness reasoning, but carry delay grows linearly with bit width

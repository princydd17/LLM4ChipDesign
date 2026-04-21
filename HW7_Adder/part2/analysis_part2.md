# Part 2 — Simulation analysis

## RCA8 LLM design

- **Testbench file:** `rca8/RCA8_tb.v`
- **All output tests PASS/FAIL:** PASS on exhaustive sweep (`65536` vectors), `FAIL=0`
- **Internal signals checked:** `dut.c[7:1]` checked each vector against expected ripple carry chain; all matched
- **Issues / debugging:** No compile/runtime issues (`iverilog` + `vvp` passed)

## CLA8 LLM design

- **Testbench file:** `cla8/CLA8_tb.v`
- **All output tests PASS/FAIL:** PASS on exhaustive sweep (`65536` vectors), `FAIL=0`
- **Internal signals checked:** `dut.g[7:0]`, `dut.p[7:0]`, and `dut.c[7:0]` checked against expected generate/propagate and recursive carry equations; all matched
- **Issues / debugging:** No compile/runtime issues (`iverilog` + `vvp` passed)

## Comparison to golden (optional but useful)

- LLM RTL behavior is consistent with expected adder arithmetic for all tested vectors.
- No I/O mismatches were observed in Part 2 simulation runs.

## Answers to spec “analysis questions” (§5.4)

1. Primary outputs correct on all cases?  
   **Yes.** Both designs pass exhaustive `8-bit x 8-bit` vector testing.
2. Internal signals match architecture expectations?  
   **Yes.** RCA carry chain and CLA `g/p/c` internal networks matched expected values.
3. Unexpected transitions / values?  
   **None observed** in sampled simulation output; all vectors passed.
4. LLM vs golden behavioral differences?  
   **No behavioral differences found** in Part 2 vector testing.
5. Acceptable vs erroneous differences?
   Only minor coding-style differences (e.g., constant literal form) were observed earlier; they are acceptable and non-functional.

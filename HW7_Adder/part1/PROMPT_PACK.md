# Part 1 Prompt Pack (copy/paste)

## A) Verilog -> natural language description prompt

Analyze the following Verilog code and provide a detailed natural language description of the design. Include:
1) overall architecture and purpose,
2) module hierarchy and interfaces,
3) signal flow and datapath,
4) key logic operations,
5) special design features.
Be specific about how functionality is implemented and preserve module/port naming from the source.

[PASTE VERILOG HERE]

---

## B) Natural language -> Verilog regeneration prompt

Based on the following description, generate synthesizable Verilog code that implements this exact architecture.
Requirements:
- Keep the same top module name and port names/widths.
- Preserve module hierarchy and internal design style (structural if structural).
- Keep the carry logic approach faithful to the description.
- Output only Verilog code; no markdown, no explanation.

[PASTE DESCRIPTION HERE]

---

## C) Manual verification assistant prompt

Compare the following two Verilog designs (Golden vs LLM-generated).
Create a structured comparison covering:
- module names and hierarchy,
- port names/directions/bit-widths,
- key internal signals and carry logic,
- structural vs behavioral style,
- likely functional equivalence,
- any potential mismatch risks.
Return concise findings table + short conclusion.

Golden Verilog:
[PASTE]

LLM-generated Verilog:
[PASTE]

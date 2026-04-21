# LLM4ChipDesign

Homework repository for the LLM4ChipDesign course.  
Each assignment is organized in its own folder (`HW1` through `HW7`) with code, reports, and supporting artifacts.

## Repository Structure

```text
LLM4ChipDesign/
├── HW1_ChipChat/      # HW1: ChipChat fundamentals
├── HW2_AutoChip/      # HW2: AutoChip tutorial and report
├── HW3_ROME/          # HW3: ROME hierarchical RTL workflow
├── HW4_TestBench/     # HW4: LLM-aided testbench generation
├── HW5_Veritas/       # HW5: Veritas CNF -> BENCH -> Verilog pipeline
├── HW6_LLMPirate/     # HW6: LLMPirate workshop and IP experiments
├── HW7_Adder/         # HW7: Adder generation, verification, optimization
└── README.md
```

---

## HW1 - ChipChat (`HW1_ChipChat/`)

**Focus:** Basic LLM-assisted RTL design tasks (combinational + sequential).

**Key files:**
- `chipchat_exampleA.ipynb` - combinational example (binary-to-BCD)
- `chipchat_exampleB.ipynb` - FSM/sequence detector example
- `chipchat_extension.ipynb` - extension work (if applicable)

---

## HW2 - AutoChip (`HW2_AutoChip/`)

**Focus:** AutoChip workflow execution and manual refinement.

**Key files:**
- `example1.ipynb` - combinational AutoChip flow
- `example2.ipynb` - sequential/FSM AutoChip flow
- `autochip_min.py` - minimal generate/simulate/feedback loop
- `AutoChip_Report.pdf` - report for Part I trajectory + manual design
- `README.md` - run instructions and submission notes

---

## HW3 - ROME (`HW3_ROME/`)

**Focus:** Hierarchical RTL decomposition and regeneration using ROME-style prompting.

**Typical deliverables:**
- hierarchy decomposition artifacts
- regenerated RTL modules
- validation/comparison notes

See `HW3_ROME/` contents for exact files used in this submission.

---

## HW4 - Testbench Generation (`HW4_TestBench/`)

**Focus:** Enhanced LLM-aided testbench generation and validation.

**Typical deliverables:**
- generated testbenches
- simulation evidence
- analysis of test quality/coverage

See `HW4_TestBench/` for assignment-specific outputs and notes.

---

## HW5 - Veritas (`HW5_Veritas/`)

**Focus:** CNF -> BENCH -> Verilog pipeline with Veritas tooling.

**Key files:**
- `veritas_hw.ipynb` - main workflow notebook
- `README.md` - setup and execution notes
- generated artifacts and helper scripts under `HW5_Veritas/`

---

## HW6 - LLMPirate (`HW6_LLMPirate/`)

**Focus:** LLMPirate workshop/IP assignment experiments.

**Typical deliverables:**
- piracy/similarity evaluation scripts
- simulation support code
- analysis outputs from workshop tasks

See `HW6_LLMPirate/` for detailed subfolders and runnable components.

---

## HW7 - Adder Project (`HW7_Adder/`)

**Focus:** LLM-based adder generation, verification, and Yosys-guided optimization.

**Main stages:**
- Part 1: golden RTL selection + natural-language descriptions + LLM regeneration
- Part 2: testbench generation with internal-signal checks + exhaustive simulation
- Part 3: optimization loop (area/delay/balanced) + best-design validation + equivalence

**Start here:**
- `HW7_Adder/README.md`
- `HW7_Adder/CHECKLIST.md`

---

## Clone

```bash
git clone https://github.com/princydd17/LLM4ChipDesign.git
cd LLM4ChipDesign
```


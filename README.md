# LLM4ChipDesign

Coursework repository for **LLM4ChipDesign**, covering seven assignments on LLM-assisted RTL generation, verification, and optimization.

This repo is organized by homework (`HW1` ... `HW7`). Each folder includes the assignment artifacts used for grading: notebooks/scripts, RTL, testbenches, simulation logs, formal/equivalence outputs, and reports.

## Repository Layout

```text
LLM4ChipDesign/
├── HW1_ChipChat/      # Introductory LLM-assisted RTL tasks
├── HW2_AutoChip/      # AutoChip workflow + report
├── HW3_ROME/          # Hierarchical RTL decomposition/regeneration
├── HW4_TestBench/     # Enhanced testbench generation and validation
├── HW5_Veritas/       # CNF -> BENCH -> Verilog (Veritas)
├── HW6_LLMPirate/     # LLMPirate workshop/IP similarity workflows
├── HW7_Adder/         # End-to-end adder generation + Yosys optimization
└── README.md
```

## Toolchain Used Across Assignments

- **Python 3.x** for notebooks/scripts
- **Icarus Verilog** (`iverilog`, `vvp`) for simulation
- **Yosys** for synthesis/formal/equivalence tasks
- Assignment-specific helper scripts in each homework directory

## Homework Overview

### HW1 - ChipChat (`HW1_ChipChat/`)
**Objective:** Build intuition for LLM-guided RTL generation in combinational and sequential settings.

**Representative artifacts:**
- `chipchat_exampleA.ipynb` (combinational case)
- `chipchat_exampleB.ipynb` (FSM case)
- `chipchat_extension.ipynb` (extension work)

### HW2 - AutoChip (`HW2_AutoChip/`)
**Objective:** Execute AutoChip flows and compare automated vs manual design refinement.

**Representative artifacts:**
- `example1.ipynb`, `example2.ipynb`
- `autochip_min.py`
- `AutoChip_Report.pdf`

### HW3 - ROME (`HW3_ROME/`)
**Objective:** Perform hierarchical decomposition and module-level regeneration/evaluation.

**Representative artifacts:** decomposition prompts/results, regenerated RTL, and validation notes in `HW3_ROME/`.

### HW4 - TestBench (`HW4_TestBench/`)
**Objective:** Generate stronger testbenches with LLM assistance and evaluate quality/coverage.

**Representative artifacts:** generated testbenches, simulation outputs, and analysis docs in `HW4_TestBench/`.

### HW5 - Veritas (`HW5_Veritas/`)
**Objective:** Convert CNF specifications through BENCH to Verilog and validate implementation fidelity.

**Representative artifacts:**
- `veritas_hw.ipynb`
- conversion/utility scripts
- generated RTL and report material

### HW6 - LLMPirate (`HW6_LLMPirate/`)
**Objective:** Explore LLM-based IP similarity/piracy analysis workflows.

**Representative artifacts:** evaluation scripts, simulation helpers, and benchmark outputs under `HW6_LLMPirate/`.

### HW7 - Adder Project (`HW7_Adder/`)
**Objective:** End-to-end LLM-assisted adder design pipeline:
1. Golden RTL selection and natural-language abstraction  
2. LLM regeneration and structural/functional verification  
3. Yosys-based optimization loop (area/delay/balanced) with best-design validation

**Primary entry points:**
- `HW7_Adder/README.md`
- `HW7_Adder/CHECKLIST.md`

## Reproducibility Notes

- Most homework folders contain assignment-specific `README.md` files with run instructions.
- Environment variables / API keys are intentionally excluded from version control.
- Simulation and synthesis artifacts are included where required for grading evidence.

## Clone

```bash
git clone https://github.com/princydd17/LLM4ChipDesign.git
cd LLM4ChipDesign
```


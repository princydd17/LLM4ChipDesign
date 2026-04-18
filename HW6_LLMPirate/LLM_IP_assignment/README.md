# LLM-Based IP Piracy Attack Framework

## Assignment Overview

This repository contains the implementation of **LLMPirate**, a framework that demonstrates how Large Language Models (LLMs) can be used to perform IP piracy attacks on hardware circuits. This assignment will guide you through understanding and experimenting with automated circuit obfuscation techniques that evade detection tools.

## Background

Hardware IP piracy is a significant concern in the semiconductor industry. This framework demonstrates how LLMs can automatically transform circuit netlists to evade detection by state-of-the-art plagiarism detection tools including:
- **GNN4IP**: Graph Neural Network-based detection
- **MOSS**: Measure of Software Similarity
- **SIM**: Text-based similarity detection  
- **JPlag**: Token-based plagiarism detection

## Repository Structure

```
LLM_for_IP_Piracy/
├── src/                          # Main evaluation scripts
│   ├── config.py                 # Centralized path configuration (auto-detects repo structure)
│   ├── characterize_circuit.py   # Circuit analysis and query generation
│   ├── circuit_decomposer.py     # Boolean expression decomposition
│   ├── evaluate_piracy_using_cached_mapping_multiprocessing_v2.py  # Main evaluation
│   ├── *_evaluation.py           # Detection tool interfaces
│   └── cached_circuit_mapping_*.pkl  # Pre-generated LLM mappings
├── src_ablation_study_wo_SolA/   # Ablation study (without Solution A)
├── src_ablation_study_wo_SolB/   # Ablation study (without Solution B)
│   ├── GPT_communication_script.py  # LLM query script
│   └── functionality_checker.py      # Circuit equivalence verification
├── all_GNN4IP_files/             # GNN4IP detection tool and datasets
│   └── IP-Netlist-toy/           # Test circuit benchmarks
├── abc/                          # ABC synthesis tool and NanGate libraries (included)
│   ├── abc                       # ABC synthesis executable
│   ├── NangateOpenCellLibrary_typical.lib
│   └── NangateOpenCellLibrary_typical_reduced.lib
├── sim/                          # SIM similarity tool
└── jplag-5.0.0-jar-with-dependencies.jar  # JPlag detection tool
```

## Prerequisites

### Software Requirements
- Python 3.8+
- Java Runtime Environment 11+ (for JPlag)
  ```bash
  # Check Java version
  java -version
  
  # Install if needed (Ubuntu/Debian)
  sudo apt install default-jre
  ```
- Required Python packages:
  ```bash
  pip install openai anthropic networkx numpy pickle-mixin
  ```

### Hardware Requirements
- Multi-core CPU (recommended for parallel processing)
- At least 8GB RAM
- ~5GB disk space for datasets and results

### Configuration

All file paths are managed by `src/config.py` which automatically detects the repository structure.

**Required Large Files (Download Separately):**

Due to GitHub's file size limits, you need to download these separately:

1. **ABC Synthesis Tool** (117 MB)
   ```bash
   # Download and place in abc/ directory
   # Get from: https://github.com/berkeley-abc/abc
   # Or copy from: /home/gohil.vasudev/Documents/Research/RL/AI_vs_AI/abc/abc
   cp /path/to/abc abc/abc
   chmod +x abc/abc
   ```

2. **JPlag JAR** (94 MB)
   ```bash
   # Download JPlag 5.0.0
   wget https://github.com/jplag/JPlag/releases/download/v5.0.0/jplag-5.0.0-jar-with-dependencies.jar
   ```

3. **MOR1KX Circuit Files** (Optional, only for large circuit experiments)
   ```bash
   # These are 80+ MB files for the MOR1KX processor benchmark
   # Skip if you're only testing with smaller circuits (c432, c499, c880, IBEX, AES, GPS)
   ```

**Included in Repository:**
- ✅ NanGate cell libraries (`abc/*.lib`)
- ✅ GNN4IP detection framework
- ✅ SIM tool
- ✅ Small/medium circuit benchmarks (c432, c499, c880, IBEX, AES, GPS)

**Verify Installation:**
```bash
python3 src/config.py
```

You should see: `✓ All required paths validated successfully`

## Assignment Tasks

---

## **Phase 1: Understanding LLM-Based Circuit Transformation**

### Task 1.1: Analyze Pre-generated Mappings

The repository includes pre-generated circuit mappings from various LLMs. These mappings represent functionally equivalent transformations of logic gates.

**Objective:** Understand how LLMs transform circuits.

1. Navigate to the `src/` directory
2. Load and inspect a cached mapping file:

```python
import pickle

# Load GPT-4 mappings
with open('cached_circuit_mapping_GPT4.pkl', 'rb') as f:
    mappings = pickle.load(f)

# Examine mappings for 2-input NAND gates
print("NAND gate transformations:")
for target_gate, circuits in mappings['nand_2'].items():
    print(f"\n{target_gate}:")
    for circuit in circuits:
        print(circuit)
```

**Expected Output:** You should see circuits like:
```
NOR:
my_N0 = NOR(A1, A1)
my_N1 = NOR(A2, A2)
Y = NOR(my_N0, my_N1)
```

**Questions to Answer:**
- How many different gate types can transform a NAND gate?
- Which LLM produces the most diverse transformations?
- Are all transformations functionally equivalent?

---

### Task 1.2: Generate Your Own LLM Mappings (Optional Advanced Task)

**Objective:** Query an LLM to generate new circuit transformations.

**⚠️ Note:** This requires an OpenAI API key (or other LLM API). Skip this if you don't have access.

1. Navigate to `src_ablation_study_wo_SolB/`
2. Edit `GPT_communication_script.py` and add your API key
3. Run the script:

```bash
cd src_ablation_study_wo_SolB/
python GPT_communication_script.py
```

**What Happens:**
- The script queries the LLM with circuit transformation tasks
- Uses `functionality_checker.py` to verify functional equivalence
- Implements iterative refinement (up to 5 attempts)
- Caches successful transformations to `cached_circuit_mapping_GPT3dot5.pkl`

**Observe:**
- How many attempts does the LLM need on average?
- Which gate transformations are most challenging?
- Do simpler or more complex gates have higher success rates?

---

## **Phase 2: Performing IP Piracy Evaluation**

### Task 2.1: Run Basic Piracy Evaluation

**Objective:** Evaluate how well LLM-transformed circuits evade detection.

1. Navigate to the `src/` directory:
```bash
cd src/
```

2. Run the main evaluation script:
```bash
python evaluate_piracy_using_cached_mapping_multiprocessing_v2.py
```

**What This Does:**
- Loads original circuits from `all_GNN4IP_files/IP-Netlist-toy/`
- Applies LLM mappings using different strategies:
  - `random`: Random gate selection
  - `NAND`, `NOR`: Specific gate targeting
  - `AND_NOT`, `OR_NOT`: Multi-gate combinations
- Tests each transformation 5 times (for statistical robustness)
- Evaluates against all detection tools
- Saves results to `master_results.pkl`

**Expected Runtime:** 
- Small circuits (c432, c499, c880): 15-30 minutes
- With all 8 LLMs: 2-4 hours

**Monitor Progress:**
```bash
tail -f all_log.log
```

---

### Task 2.2: Analyze Results

After evaluation completes, analyze the results:

```python
import pickle
import numpy as np

# Load results
with open('master_results.pkl', 'rb') as f:
    results = pickle.load(f)

# Analyze success rates
llm_name = 'cached_circuit_mapping_GPT4'
mapping_strategy = 'NAND'
detection_tool = 'GNN4IP'

for variant in results[llm_name][mapping_strategy]:
    scores = results[llm_name][mapping_strategy][variant][detection_tool]
    print(f"{variant}: Mean similarity = {np.mean(scores):.3f}")
```

**Questions to Answer:**
1. Which LLM produces the most effective obfuscations?
2. Which mapping strategy is most successful?
3. Which detection tool is hardest to evade?
4. Is there variability across the 5 random samples?

---

### Task 2.3: Case Study on Larger Circuits

**Objective:** Test on realistic, larger designs.

1. Edit `evaluate_piracy_using_cached_mapping_multiprocessing_v2_for_case_study.py`
2. Change line 495 to select a design:
```python
designs = ['IBEX']  # Options: IBEX, AES, GPS, MOR1KX
```

3. Run the case study:
```bash
python evaluate_piracy_using_cached_mapping_multiprocessing_v2_for_case_study.py
```

**Larger Designs:**
- **IBEX**: RISC-V processor (~10K gates)
- **AES**: AES encryption core
- **GPS**: GPS baseband processor
- **MOR1KX**: OpenRISC processor

**Expected Runtime:** Several hours per design

**Analysis Questions:**
- Do larger circuits have higher/lower evasion rates?
- Is the relationship between circuit size and detection consistent?

---

## **Phase 3: Advanced Experiments**

### Task 3.1: Ablation Study - Impact of Self-Correction

**Objective:** Measure the impact of iterative LLM refinement.

The `wo_SolC` (without Solution C) versions test performance when using only first-attempt LLM responses.

```bash
python evaluate_piracy_using_cached_mapping_multiprocessing_v2_ablation_study_wo_SolC.py
```

**Compare:**
- Results in `master_results.pkl` (with self-correction)
- Results in `master_results_ablation_study_wo_SolC.pkl` (without)

**Expected Finding:**
Self-correction should improve success rates by 15-30%.

---

### Task 3.2: Circuit Characterization

**Objective:** Analyze circuit properties that affect evasion success.

Run characterization scripts:

```bash
# Count gates in circuits
python count_num_gates.py

# Find longest paths (circuit depth)
python find_longest_paths.py
```

**Analysis:**
- Correlate gate counts with evasion success
- Examine if circuit depth affects detection
- Plot results:

```python
import pickle
import matplotlib.pyplot as plt

with open('master_percent_change_in_min_num_gates.pkl', 'rb') as f:
    gate_changes = pickle.load(f)

# Plot gate count changes after transformation
# (Add your analysis code here)
```

---

### Task 3.3: Compare Detection Tools

**Objective:** Understand strengths/weaknesses of each detector.

Create a comparison analysis:

```python
import pickle
import pandas as pd

with open('master_results.pkl', 'rb') as f:
    results = pickle.load(f)

# Create comparison table
comparison = {}
for llm in results:
    for strategy in results[llm]:
        for variant in results[llm][strategy]:
            for tool in ['GNN4IP', 'SIM', 'Jplag']:
                scores = results[llm][strategy][variant][tool]
                key = f"{llm}_{strategy}"
                if key not in comparison:
                    comparison[key] = {t: [] for t in ['GNN4IP', 'SIM', 'Jplag']}
                comparison[key][tool].extend(scores)

# Calculate mean scores
df = pd.DataFrame({
    k: {tool: np.mean(v[tool]) for tool in v}
    for k, v in comparison.items()
}).T

print(df)
```

**Questions:**
- Which tool is most robust?
- Are there strategies that work against some tools but not others?
- Can you find patterns in which transformations are most effective?

---

## Understanding the Code

### Key Files and Their Purposes

#### Circuit Analysis
- **`characterize_circuit.py`**: 
  - Analyzes circuit netlists to identify gate types
  - Generates query templates for LLMs
  - Functions: `characterize_generic_netlist()`, `create_LLM_circuit_query_template()`

- **`circuit_decomposer.py`**:
  - Decomposes complex Boolean expressions into primitive gates
  - Ensures LLM responses use only allowed gate types
  - Function: `final_decompose_expression()`

#### LLM Interaction
- **`GPT_communication_script.py`** (`src_ablation_study_wo_SolB/`):
  - Queries LLMs with circuit transformation requests
  - Implements iterative refinement loop
  - Verifies functional equivalence
  - Caches successful transformations

- **`functionality_checker.py`**:
  - Simulates circuits using random test vectors
  - Verifies input/output equivalence
  - Uses NetworkX for graph-based simulation

#### Configuration
- **`config.py`**:
  - Centralized path configuration for all tools and datasets
  - Auto-detects repository root directory
  - Provides validation functions to check installation
  - All scripts import paths from here for portability

#### Evaluation
- **`evaluate_piracy_using_cached_mapping_multiprocessing_v2.py`**:
  - Main evaluation orchestrator
  - Applies cached transformations to benchmark circuits
  - Runs detection tools in parallel
  - Aggregates results

#### Detection Tool Interfaces
- **`MOSS_evaluation.py`**: MOSS similarity checker interface
- **`sim_evaluation.py`**: SIM text similarity interface  
- **`Jplag_evaluation.py`**: JPlag plagiarism detector interface
- **GNN4IP**: Graph neural network detector (in `all_GNN4IP_files/`)

---

## Tips for Success

### Performance Optimization
1. **Parallel Processing**: The scripts use multiprocessing. More cores = faster execution.
2. **Checkpoint Progress**: Results are saved incrementally to avoid data loss.
3. **Memory Management**: Large designs may require 16GB+ RAM.

### Debugging
- Check log files: `all_log.log`, `Sim_log.log`, etc.
- Verify configuration: `python3 src/config.py` to validate all paths
- Ensure detection tools are properly installed

### Common Issues

**Issue**: `FileNotFoundError` for any tool
- **Solution**: Run `python3 src/config.py` to check which paths are missing
- Verify the repository structure is intact (all directories present)

**Issue**: Java errors with JPlag
- **Solution**: Ensure Java 11+ is installed: `java -version`

**Issue**: ABC executable permission denied
- **Solution**: Make ABC executable: `chmod +x abc/abc`

**Issue**: Import errors from config
- **Solution**: Ensure you're running scripts from the correct directory (repository root or `src/`)

---

## Deliverables

1. **Results Analysis Report** (~3-5 pages):
   - Success rates by LLM and strategy
   - Detection tool comparison
   - Circuit size analysis
   - Visualization of key findings

2. **Code Modifications**:
   - At least one experiment modification (e.g., new mapping strategy, different threshold)
   - Document changes in comments

3. **Critical Analysis** (1-2 pages):
   - Security implications of LLM-based IP piracy
   - Potential countermeasures
   - Ethical considerations

---

## Grading Rubric

- **Understanding (30%)**: Correct analysis of mappings and transformations
- **Experimentation (40%)**: Successfully running evaluations and generating results
- **Analysis (20%)**: Insightful interpretation of results
- **Critical Thinking (10%)**: Thoughtful discussion of implications

---

## Additional Resources

### Papers
- "LLMPirate: Leveraging Large Language Models for IP Piracy" (arXiv)
- "GNN4IP: Graph Neural Networks for Hardware IP Protection"

### Tools Documentation
- [JPlag Documentation](https://jplag.ipd.kit.edu/)
- [MOSS Submission Guide](https://theory.stanford.edu/~aiken/moss/)
---

## Academic Integrity Notice

This framework is for **educational purposes only**. The techniques demonstrated should be used to:
- Understand security vulnerabilities in hardware IP
- Develop better detection methods
- Advance research in IP protection

**Do not use this for:**
- Actual IP theft
- Circumventing legal protections
- Any malicious purposes

Violations of academic integrity policies or laws will be reported.

---

## Contact and Support

For questions about this assignment:
1. Check existing log files for error messages
2. Review the code comments for clarification
3. Consult the course instructor

---

## License

This code is provided for educational purposes. Refer to individual tool licenses for commercial use restrictions.

---
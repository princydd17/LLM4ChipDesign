## HW2_AutoChip (AutoChip Tutorial Assignment)

This folder is a **self-contained HW2 workspace** using a minimal AutoChip-style loop:
- generate Verilog with an LLM
- compile/simulate with `iverilog` + `vvp`
- feed errors back into the next iteration

It is set up for the two ChipChat examples typically used for HW2:
- **Example 1 (combinational)**: binary-to-BCD converter
- **Example 2 (sequential/FSM)**: sequence detector

### What you submit (per HW2 spec)

- `example1.ipynb`
- `example2.ipynb`
- `AutoChip_Report.pdf` (you create this; included here)

### One-time setup

- **Install Icarus Verilog**
  - macOS (Homebrew): `brew install iverilog`
  - Ubuntu/Colab: `apt-get update && apt-get install -y iverilog`

- **Set your API key**
  - NVIDIA/OpenAI-compatible: set `OPENAI_API_KEY` to your NVIDIA key (starts with `nvapi-...`)

Example (macOS/zsh):

```bash
export OPENAI_API_KEY="nvapi-REPLACE_ME"
```

### Run the notebooks

- Open and run:
  - `example1.ipynb`
  - `example2.ipynb`

Each notebook:
- downloads the official testbench used in ChipChat
- runs the AutoChip loop (iterations + multiple candidates)
- prints the exact `iverilog`/`vvp` commands and the passing output
- saves outputs under `runs/`

### Notes / knobs

The notebooks default to NVIDIA’s OpenAI-compatible endpoint:
- base URL: `https://integrate.api.nvidia.com/v1`
- model: `meta/llama-3.1-8b-instruct`

You can change these in the notebook cell that sets:
- `BASE_URL`
- `MODEL_ID`
- `NUM_CANDIDATES`
- `MAX_ITERS`


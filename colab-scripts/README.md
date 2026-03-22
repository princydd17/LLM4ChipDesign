# Colab scripts (Veritas)

This folder mirrors the **course** layout (`colab-scripts/Veritas_tutorial.ipynb`).

## Files

| File | Purpose |
|------|---------|
| **`Veritas_tutorial.ipynb`** | Same pipeline as `HW5_Veritas/veritas_hw.ipynb` (synced copy). |
| **`veritas_api_setup.py`** | API key + **NVIDIA NIM** base URL (`https://integrate.api.nvidia.com/v1`) + default model `meta/llama-3.1-8b-instruct` when using `nvapi-...` keys. |

## Google Colab

1. Upload **`Veritas_tutorial.ipynb`** and **`veritas_api_setup.py`** to the same Colab session folder (or clone this repo and open the notebook from `/content/.../colab-scripts`).
2. In the first code cell, run `%pip install -q openai python-dotenv` if needed.
3. Set your key: `os.environ["OPENAI_API_KEY"] = "nvapi-..."` **or** use `MANUAL_API_KEY` in that cell.
4. Run the API setup cell, then the rest top-to-bottom.

## Homework submission

Course submissions typically use **`HW5_Veritas/veritas_hw.ipynb`** — keep that copy executed with outputs; this `colab-scripts` copy is for alignment with the shared tutorial path.

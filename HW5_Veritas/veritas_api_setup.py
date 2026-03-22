# Loaded by veritas_hw.ipynb via exec() — edit MANUAL_API_KEY in the notebook cell before exec,
# or create HW5_Veritas/.env with OPENAI_API_KEY=...
from __future__ import annotations

import os
from pathlib import Path

_here = Path(__file__).resolve().parent

# --- load .env (same folder as this file, or cwd) ---
try:
    from dotenv import load_dotenv
    for _env in (
        _here / ".env",
        Path.cwd() / ".env",
        Path.cwd() / "HW5_Veritas" / ".env",
    ):
        if _env.is_file():
            load_dotenv(_env)
            break
    else:
        load_dotenv()
except ImportError:
    pass

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"
OPENAI_DEFAULT_MODEL = "gpt-5-mini-2025-08-07"

_g = globals()
_manual = str(_g.get("MANUAL_API_KEY") or "").strip()

# Accept common env names (NVIDIA console sometimes labels keys separately)
_key = (
    (os.getenv("OPENAI_API_KEY") or "").strip()
    or (os.getenv("NVIDIA_API_KEY") or "").strip()
    or _manual
)
API_KEY = _key or None

BASE_URL = os.getenv("OPENAI_BASE_URL") or None
_explicit_model = os.getenv("OPENAI_MODEL")
MODEL_NAME = _explicit_model or OPENAI_DEFAULT_MODEL

if API_KEY and API_KEY.startswith("nvapi-"):
    if not BASE_URL:
        BASE_URL = NVIDIA_BASE_URL
    if _explicit_model is None:
        MODEL_NAME = NVIDIA_DEFAULT_MODEL

if not API_KEY:
    raise ValueError(
        "No API key found.\n"
        f"  1) Create {_here / '.env'} with:\n"
        "       OPENAI_API_KEY=nvapi-...\n"
        "     (or NVIDIA_API_KEY=nvapi-...)\n"
        "  2) In the notebook cell above exec(): set MANUAL_API_KEY = 'nvapi-...'\n"
        "  3) Or in a cell: %env OPENAI_API_KEY=nvapi-...\n"
        "  4) pip install python-dotenv  (needed to load .env files)\n"
    )

print(f"Using model: {MODEL_NAME}")
print(f"Base URL: {BASE_URL or '(OpenAI default — sk-... keys only)'}")
print("veritas_api_setup.py loaded — OK (this line proves you are not on the old notebook cell)")

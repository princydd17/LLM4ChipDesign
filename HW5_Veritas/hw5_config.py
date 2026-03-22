"""
Veritas HW5 — API configuration.

Loads `.env` from this file's directory first (HW5_Veritas/.env), so it works even when
Jupyter's cwd is the repo root. Do not commit real keys.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"
OPENAI_DEFAULT_MODEL = "gpt-5-mini-2025-08-07"


def _load_dotenv_files() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    here = Path(__file__).resolve().parent
    cwd = Path.cwd()
    candidates = [
        here / ".env",
        cwd / ".env",
        cwd / "HW5_Veritas" / ".env",
    ]
    for env_path in candidates:
        if env_path.is_file():
            load_dotenv(env_path)
            return
    load_dotenv()


def setup_veritas_api(manual_key: str = "") -> Tuple[Optional[str], Optional[str], str]:
    """
    Returns (API_KEY, BASE_URL, MODEL_NAME).

    Priority: OPENAI_API_KEY env (after dotenv) -> manual_key string.
    """
    _load_dotenv_files()

    _key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not _key:
        _key = (manual_key or "").strip()
    api_key = _key or None

    base_url = os.getenv("OPENAI_BASE_URL") or None
    explicit_model = os.getenv("OPENAI_MODEL")
    model_name = explicit_model or OPENAI_DEFAULT_MODEL

    if api_key and api_key.startswith("nvapi-"):
        if not base_url:
            base_url = NVIDIA_BASE_URL
        if explicit_model is None:
            model_name = NVIDIA_DEFAULT_MODEL

    return api_key, (base_url or None), model_name


def require_api_key(manual_key: str = "") -> Tuple[str, Optional[str], str]:
    """Like setup_veritas_api but raises if no key."""
    api_key, base_url, model_name = setup_veritas_api(manual_key=manual_key)
    if not api_key:
        here = Path(__file__).resolve().parent
        raise ValueError(
            "No API key found. Do one of:\n"
            f"  1) Create {here / '.env'} with OPENAI_API_KEY=... (copy from .env.example)\n"
            "  2) export OPENAI_API_KEY=... before starting Jupyter\n"
            "  3) In a notebook cell: %env OPENAI_API_KEY=...\n"
            "  4) Set MANUAL_API_KEY = '...' in the notebook setup cell\n"
            "Then restart the kernel and run the setup cell again."
        )
    return api_key, base_url, model_name

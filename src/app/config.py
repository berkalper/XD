from __future__ import annotations

from pathlib import Path
import sys


def get_data_path() -> Path:
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path.cwd()
    return base_dir / "data" / "patients.json"

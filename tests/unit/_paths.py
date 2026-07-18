# SPDX-License-Identifier: Apache-2.0
"""Test import path helpers for the source-layout packages."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_SRC = ROOT / "packages" / "contracts" / "src"
EVAL_CORE_SRC = ROOT / "packages" / "eval-core" / "src"

for path in (CONTRACTS_SRC, EVAL_CORE_SRC):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)


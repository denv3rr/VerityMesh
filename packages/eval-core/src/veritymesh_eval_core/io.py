# SPDX-License-Identifier: Apache-2.0
"""Safe file loading and deterministic JSON writing for evaluation bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from veritymesh_contracts.errors import ContractValidationError, ValidationIssue
from veritymesh_contracts.suite import EvalSuite


MAX_SUITE_BYTES = 1_000_000


def load_suite(path: Path) -> tuple[EvalSuite, str]:
    raw = path.read_bytes()
    if len(raw) > MAX_SUITE_BYTES:
        raise ContractValidationError(
            [ValidationIssue("$", f"suite file is larger than {MAX_SUITE_BYTES} bytes", "too_large")]
        )

    payload = _loads_by_suffix(path, raw)
    if not isinstance(payload, dict):
        raise ContractValidationError([ValidationIssue("$", "suite document must be an object", "type")])
    return EvalSuite.from_mapping(payload), raw.decode("utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(payload) + "\n", encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)


def _loads_by_suffix(path: Path, raw: bytes) -> Any:
    text = raw.decode("utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ContractValidationError(
                [ValidationIssue("$", f"invalid JSON: {exc.msg}", "parse_error")]
            ) from exc
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ContractValidationError(
                [
                    ValidationIssue(
                        "$",
                        "YAML suites require installing the optional 'yaml' extra; JSON suites work without dependencies",
                        "missing_dependency",
                    )
                ]
            ) from exc
        return yaml.safe_load(text)
    raise ContractValidationError(
        [ValidationIssue("$", "suite path must end in .json, .yaml, or .yml", "unsupported_file_type")]
    )


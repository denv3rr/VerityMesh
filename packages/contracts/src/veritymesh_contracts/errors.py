# SPDX-License-Identifier: Apache-2.0
"""Validation errors for public VerityMesh contracts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """One schema validation issue with a stable path and error code."""

    path: str
    message: str
    code: str = "invalid"

    def to_mapping(self) -> dict[str, str]:
        return {"path": self.path, "message": self.message, "code": self.code}


class ContractValidationError(ValueError):
    """Raised when a suite or result contract fails strict validation."""

    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        super().__init__(joined)


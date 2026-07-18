# SPDX-License-Identifier: Apache-2.0
"""Versioned evaluation result bundle contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


RESULT_SCHEMA_VERSION = "veritymesh.result.v0"


@dataclass(frozen=True)
class ScoreResult:
    name: str
    type: str
    version: str
    passed: bool
    actual: Any
    expected: Any
    reason: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "type": self.type,
            "version": self.version,
            "passed": self.passed,
            "actual": self.actual,
            "expected": self.expected,
        }
        if self.reason:
            payload["reason"] = self.reason
        if self.details:
            payload["details"] = self.details
        return payload


@dataclass(frozen=True)
class CaseResult:
    id: str
    category: str
    difficulty: str
    input: dict[str, Any]
    output: dict[str, Any]
    evidence: list[dict[str, Any]]
    scores: list[ScoreResult]
    passed: bool
    duration_ms: float
    model_invocations: list[dict[str, Any]] = field(default_factory=list)
    tool_invocations: list[dict[str, Any]] = field(default_factory=list)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "input": self.input,
            "output": self.output,
            "evidence": self.evidence,
            "scores": [score.to_mapping() for score in self.scores],
            "passed": self.passed,
            "duration_ms": self.duration_ms,
            "model_invocations": self.model_invocations,
            "tool_invocations": self.tool_invocations,
        }


@dataclass(frozen=True)
class RunSummary:
    total_cases: int
    passed_cases: int
    failed_cases: int
    total_scores: int
    passed_scores: int
    failed_scores: int
    case_pass_rate: float
    score_pass_rate: float

    def to_mapping(self) -> dict[str, Any]:
        return {
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "failed_cases": self.failed_cases,
            "total_scores": self.total_scores,
            "passed_scores": self.passed_scores,
            "failed_scores": self.failed_scores,
            "case_pass_rate": self.case_pass_rate,
            "score_pass_rate": self.score_pass_rate,
        }


@dataclass(frozen=True)
class RunBundle:
    id: str
    suite_id: str
    suite_version: str
    suite_hash: str
    workflow_id: str
    workflow_version: str
    seed: int
    code_version: str
    environment: dict[str, Any]
    summary: RunSummary
    cases: list[CaseResult]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": RESULT_SCHEMA_VERSION,
            "run": {
                "id": self.id,
                "suite_id": self.suite_id,
                "suite_version": self.suite_version,
                "suite_hash": self.suite_hash,
                "workflow_id": self.workflow_id,
                "workflow_version": self.workflow_version,
                "seed": self.seed,
                "code_version": self.code_version,
                "environment": self.environment,
                "summary": self.summary.to_mapping(),
            },
            "cases": [case.to_mapping() for case in self.cases],
        }


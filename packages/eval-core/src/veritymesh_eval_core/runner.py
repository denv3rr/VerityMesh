# SPDX-License-Identifier: Apache-2.0
"""Run deterministic evaluation suites."""

from __future__ import annotations

import hashlib
import platform
from typing import Any

from veritymesh_contracts.result import CaseResult, RunBundle, RunSummary
from veritymesh_contracts.suite import EvalSuite
from veritymesh_eval_core.fake_support import WORKFLOW_ID, WORKFLOW_VERSION, execute_case
from veritymesh_eval_core.io import canonical_json
from veritymesh_eval_core.scorers import evaluate_scorer


def run_suite(
    suite: EvalSuite,
    *,
    workflow_id: str | None = None,
    seed: int = 0,
    suite_hash: str | None = None,
    code_version: str = "development",
) -> RunBundle:
    selected_workflow = workflow_id or suite.workflow.id
    if selected_workflow != WORKFLOW_ID:
        raise ValueError(f"unsupported workflow {selected_workflow!r}; available workflow: {WORKFLOW_ID}")

    resolved_suite_hash = suite_hash or sha256_text(canonical_json(suite.to_mapping()))
    cases: list[CaseResult] = []
    for case in suite.cases:
        execution = execute_case(case)
        context: dict[str, Any] = {
            "case": case.to_mapping(),
            "input": case.input,
            "expected": case.expected,
            "output": execution.output,
            "evidence": execution.evidence,
            "tool_invocations": execution.tool_invocations,
            "model_invocations": execution.model_invocations,
        }
        scores = [evaluate_scorer(scorer, context) for scorer in case.scorers]
        cases.append(
            CaseResult(
                id=case.id,
                category=case.category,
                difficulty=case.difficulty,
                input=case.input,
                output=execution.output,
                evidence=execution.evidence,
                scores=scores,
                passed=all(score.passed for score in scores),
                duration_ms=execution.duration_ms,
                model_invocations=execution.model_invocations,
                tool_invocations=execution.tool_invocations,
            )
        )

    summary = summarize_cases(cases)
    run_id = stable_run_id(resolved_suite_hash, selected_workflow, seed, code_version)
    return RunBundle(
        id=run_id,
        suite_id=suite.suite.id,
        suite_version=suite.suite.version,
        suite_hash=resolved_suite_hash,
        workflow_id=selected_workflow,
        workflow_version=WORKFLOW_VERSION,
        seed=seed,
        code_version=code_version,
        environment={
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "offline": True,
        },
        summary=summary,
        cases=cases,
    )


def summarize_cases(cases: list[CaseResult]) -> RunSummary:
    total_cases = len(cases)
    passed_cases = sum(1 for case in cases if case.passed)
    total_scores = sum(len(case.scores) for case in cases)
    passed_scores = sum(1 for case in cases for score in case.scores if score.passed)
    return RunSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=total_cases - passed_cases,
        total_scores=total_scores,
        passed_scores=passed_scores,
        failed_scores=total_scores - passed_scores,
        case_pass_rate=_rate(passed_cases, total_cases),
        score_pass_rate=_rate(passed_scores, total_scores),
    )


def stable_run_id(suite_hash: str, workflow_id: str, seed: int, code_version: str) -> str:
    payload = f"{suite_hash}:{workflow_id}:{seed}:{code_version}"
    return f"run_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


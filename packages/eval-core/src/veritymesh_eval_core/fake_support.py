# SPDX-License-Identifier: Apache-2.0
"""Deterministic fake support workflow.

This workflow is a local rule-based stand-in for provider-backed agents. It
returns stable evidence, tool calls, and structured output so CI can exercise
the evaluation pipeline without network access, secrets, or model variance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from veritymesh_contracts.suite import EvalCase


WORKFLOW_ID = "fake-support-agent"
WORKFLOW_VERSION = "fake-support-agent.v0"


@dataclass(frozen=True)
class WorkflowExecution:
    output: dict[str, Any]
    evidence: list[dict[str, Any]]
    model_invocations: list[dict[str, Any]]
    tool_invocations: list[dict[str, Any]]
    duration_ms: float = 0.0


def execute_case(case: EvalCase) -> WorkflowExecution:
    question = str(case.input.get("question", ""))
    normalized = question.lower()

    if "reset" in normalized and "password" in normalized:
        return _password_reset(question)
    if "audit" in normalized and ("export" in normalized or "csv" in normalized):
        return _audit_export(question)
    if "delete" in normalized and "production" in normalized:
        return _safe_refusal(
            question,
            "I cannot help delete production data. I can explain safe backup and retention procedures if needed.",
            "unsafe_destructive_request",
        )
    return _safe_refusal(
        question,
        "I do not have enough evidence in the support corpus to answer that question.",
        "insufficient_evidence",
    )


def _password_reset(question: str) -> WorkflowExecution:
    evidence = [
        {
            "evidence_id": "support/account-security#reset-password",
            "source": "Account Security Guide",
            "quote": "Account Settings > Security includes password reset controls.",
        }
    ]
    tool_calls = [{"name": "docs.search", "arguments": {"query": "reset password"}}]
    output = {
        "answer": "To reset a password, open Account Settings, choose Security, and request a reset link.",
        "citations": [{"evidence_id": evidence[0]["evidence_id"]}],
        "tool_calls": tool_calls,
        "refusal": False,
        "structured": {"intent": "password_reset", "confidence": 1.0, "refusal": False},
    }
    return _execution(question, output, evidence, tool_calls)


def _audit_export(question: str) -> WorkflowExecution:
    evidence = [
        {
            "evidence_id": "support/admin-audit#export-csv",
            "source": "Admin Audit Guide",
            "quote": "Admin Console > Audit Logs provides an Export CSV action for admins.",
        }
    ]
    tool_calls = [{"name": "docs.search", "arguments": {"query": "export audit logs csv"}}]
    output = {
        "answer": "Admins can export audit logs from Admin Console > Audit Logs by selecting Export CSV.",
        "citations": [{"evidence_id": evidence[0]["evidence_id"]}],
        "tool_calls": tool_calls,
        "refusal": False,
        "structured": {"intent": "audit_export", "format": "csv", "confidence": 1.0, "refusal": False},
    }
    return _execution(question, output, evidence, tool_calls)


def _safe_refusal(question: str, answer: str, reason: str) -> WorkflowExecution:
    output = {
        "answer": answer,
        "citations": [],
        "tool_calls": [],
        "refusal": True,
        "structured": {"intent": "refusal", "reason": reason, "confidence": 1.0, "refusal": True},
    }
    return _execution(question, output, [], [])


def _execution(
    question: str,
    output: dict[str, Any],
    evidence: list[dict[str, Any]],
    tool_calls: list[dict[str, Any]],
) -> WorkflowExecution:
    return WorkflowExecution(
        output=output,
        evidence=evidence,
        tool_invocations=tool_calls,
        model_invocations=[
            {
                "provider": "deterministic-fake",
                "model": WORKFLOW_ID,
                "model_version": WORKFLOW_VERSION,
                "input": {"question": question},
                "latency_ms": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "estimated_cost_usd": 0.0,
            }
        ],
    )


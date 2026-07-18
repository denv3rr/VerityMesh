# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import unittest

from _paths import ROOT  # noqa: F401
from veritymesh_contracts.suite import ScorerSpec
from veritymesh_eval_core.scorers import evaluate_scorer


class ScorerTests(unittest.TestCase):
    def test_exact_match_is_case_insensitive_when_configured(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="exact",
                type="exact_match",
                config={"actual": "output.answer", "expected": "hello", "case_sensitive": False},
            ),
            {"output": {"answer": "Hello"}},
        )

        self.assertTrue(score.passed)

    def test_contains_failure_reports_reason(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="contains",
                type="contains",
                config={"actual": "output.answer", "expected": "needle", "case_sensitive": False},
            ),
            {"output": {"answer": "haystack"}},
        )

        self.assertFalse(score.passed)
        self.assertIn("contain", score.reason or "")

    def test_regex_matches_with_flags(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="regex",
                type="regex",
                config={"actual": "output.answer", "pattern": r"reset\s+link", "flags": ["IGNORECASE"]},
            ),
            {"output": {"answer": "Request a Reset Link."}},
        )

        self.assertTrue(score.passed)

    def test_structured_output_schema_subset(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="structured",
                type="structured_output",
                config={
                    "actual": "output.structured",
                    "schema": {
                        "type": "object",
                        "required": ["intent", "refusal"],
                        "properties": {
                            "intent": {"type": "string", "enum": ["password_reset"]},
                            "refusal": {"type": "boolean"},
                        },
                    },
                },
            ),
            {"output": {"structured": {"intent": "password_reset", "refusal": False}}},
        )

        self.assertTrue(score.passed)

    def test_citation_reports_precision_and_recall(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="citation",
                type="citation",
                config={"expected": ["doc#a", "doc#b"], "require_all": True},
            ),
            {"output": {"citations": [{"evidence_id": "doc#a"}]}},
        )

        self.assertFalse(score.passed)
        self.assertEqual(1.0, score.details["precision"])
        self.assertEqual(0.5, score.details["recall"])

    def test_tool_call_matches_argument_subset(self) -> None:
        score = evaluate_scorer(
            ScorerSpec(
                name="tool",
                type="tool_call",
                config={
                    "expected": [{"name": "docs.search", "arguments": {"query": "reset"}}],
                    "match_arguments": "subset",
                },
            ),
            {"output": {"tool_calls": [{"name": "docs.search", "arguments": {"query": "reset", "limit": 5}}]}},
        )

        self.assertTrue(score.passed)


if __name__ == "__main__":
    unittest.main()

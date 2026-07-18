# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import unittest

from _paths import ROOT  # noqa: F401
from veritymesh_contracts import ContractValidationError, EvalSuite
from veritymesh_eval_core.io import load_suite


VALID_SUITE = {
    "schema_version": "veritymesh.suite.v0",
    "suite": {"id": "unit", "version": "1", "name": "Unit suite"},
    "workflow": {"id": "fake-support-agent", "version": "fake-support-agent.v0"},
    "cases": [
        {
            "id": "case-1",
            "category": "normal",
            "difficulty": "easy",
            "input": {"question": "How do I reset my password?"},
            "expected": {"answer_contains": "reset link"},
            "scorers": [
                {
                    "name": "contains_expected",
                    "type": "contains",
                    "actual": "output.answer",
                    "expected": "reset link",
                    "case_sensitive": False,
                }
            ],
        }
    ],
}


class SuiteContractTests(unittest.TestCase):
    def test_valid_suite_loads_from_mapping(self) -> None:
        suite = EvalSuite.from_mapping(VALID_SUITE)

        self.assertEqual("unit", suite.suite.id)
        self.assertEqual("fake-support-agent", suite.workflow.id)
        self.assertEqual(1, len(suite.cases))
        self.assertEqual("contains_expected", suite.cases[0].scorers[0].name)

    def test_unknown_fields_are_rejected(self) -> None:
        payload = copy.deepcopy(VALID_SUITE)
        payload["unexpected"] = True

        with self.assertRaises(ContractValidationError) as raised:
            EvalSuite.from_mapping(payload)

        self.assertEqual("$.unexpected", raised.exception.issues[0].path)
        self.assertEqual("unknown_field", raised.exception.issues[0].code)

    def test_non_object_payload_is_rejected(self) -> None:
        with self.assertRaises(ContractValidationError) as raised:
            EvalSuite.from_mapping([])

        self.assertEqual("$", raised.exception.issues[0].path)
        self.assertEqual("type", raised.exception.issues[0].code)

    def test_duplicate_case_ids_are_rejected(self) -> None:
        payload = copy.deepcopy(VALID_SUITE)
        payload["cases"].append(copy.deepcopy(payload["cases"][0]))

        with self.assertRaises(ContractValidationError) as raised:
            EvalSuite.from_mapping(payload)

        self.assertTrue(any(issue.code == "duplicate" for issue in raised.exception.issues))

    def test_public_fixture_loads(self) -> None:
        suite_path = ROOT / "benchmarks" / "support-v1" / "suites" / "fake-support-suite.json"
        suite, _raw = load_suite(suite_path)

        self.assertEqual("support-smoke-v1", suite.suite.id)
        self.assertEqual(4, len(suite.cases))


if __name__ == "__main__":
    unittest.main()

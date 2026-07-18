# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import unittest

from _paths import ROOT
from veritymesh_eval_core.io import load_suite
from veritymesh_eval_core.runner import run_suite


class RunnerTests(unittest.TestCase):
    def test_run_suite_produces_expected_summary_and_failure(self) -> None:
        suite, raw = load_suite(ROOT / "benchmarks" / "support-v1" / "suites" / "fake-support-suite.json")
        bundle = run_suite(suite, suite_hash="fixture-hash", code_version="test")

        self.assertEqual("support-smoke-v1", bundle.suite_id)
        self.assertEqual(4, bundle.summary.total_cases)
        self.assertEqual(3, bundle.summary.passed_cases)
        self.assertEqual(1, bundle.summary.failed_cases)
        self.assertTrue(raw)

        failed_case = next(case for case in bundle.cases if case.id == "unsupported-api-key-rotation")
        self.assertFalse(failed_case.passed)
        self.assertTrue(any(not score.passed for score in failed_case.scores))

    def test_run_id_is_stable_for_same_inputs(self) -> None:
        suite, _raw = load_suite(ROOT / "benchmarks" / "support-v1" / "suites" / "fake-support-suite.json")

        first = run_suite(suite, suite_hash="same", seed=7, code_version="test")
        second = run_suite(suite, suite_hash="same", seed=7, code_version="test")

        self.assertEqual(first.id, second.id)
        self.assertEqual(first.to_mapping(), second.to_mapping())

    def test_unsupported_workflow_raises(self) -> None:
        suite, _raw = load_suite(ROOT / "benchmarks" / "support-v1" / "suites" / "fake-support-suite.json")

        with self.assertRaises(ValueError):
            run_suite(suite, workflow_id="hosted-provider")


if __name__ == "__main__":
    unittest.main()


# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import contextlib
import json
import unittest
from io import StringIO

from _paths import ROOT
from veritymesh_eval_core.cli import main


class CliTests(unittest.TestCase):
    def test_validate_and_run_public_fixture(self) -> None:
        suite_path = ROOT / "benchmarks" / "support-v1" / "suites" / "fake-support-suite.json"

        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            validate_code = main(["validate", str(suite_path)])
        self.assertEqual(0, validate_code)
        self.assertIn("valid suite", stdout.getvalue())

        output = ROOT / "tmp" / "tests" / "cli-result.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            run_code = main(["run", str(suite_path), "--output", str(output), "--code-version", "test"])
        self.assertEqual(0, run_code)
        self.assertTrue(output.exists())
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual("veritymesh.result.v0", payload["schema_version"])
        self.assertEqual(1, payload["run"]["summary"]["failed_cases"])


if __name__ == "__main__":
    unittest.main()

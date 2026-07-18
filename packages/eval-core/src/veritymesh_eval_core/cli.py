# SPDX-License-Identifier: Apache-2.0
"""Command line interface for the offline evaluation core."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from veritymesh_contracts.errors import ContractValidationError
from veritymesh_eval_core.fake_support import WORKFLOW_ID
from veritymesh_eval_core.io import load_suite, write_json
from veritymesh_eval_core.runner import run_suite


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            suite, _ = load_suite(Path(args.suite))
            print(f"valid suite: {suite.suite.id}@{suite.suite.version} ({len(suite.cases)} cases)")
            return 0
        if args.command == "run":
            suite_path = Path(args.suite)
            suite, raw_text = load_suite(suite_path)
            suite_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            bundle = run_suite(
                suite,
                workflow_id=args.workflow,
                seed=args.seed,
                suite_hash=suite_hash,
                code_version=args.code_version,
            )
            output = Path(args.output) if args.output else Path("result-bundles") / f"{bundle.id}.json"
            write_json(output, bundle.to_mapping())
            _print_run_summary(bundle.to_mapping(), output)
            return 0
    except ContractValidationError as exc:
        print("suite validation failed:", file=sys.stderr)
        for issue in exc.issues:
            print(f"- {issue.path}: {issue.message} [{issue.code}]", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    parser.print_help()
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="veritymesh", description="VerityMesh offline evaluation CLI")
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate", help="validate an evaluation suite")
    validate.add_argument("suite", help="path to a .json, .yaml, or .yml suite")

    run = subparsers.add_parser("run", help="run an evaluation suite")
    run.add_argument("suite", help="path to a .json, .yaml, or .yml suite")
    run.add_argument("--workflow", default=WORKFLOW_ID, help=f"workflow id to run; default: {WORKFLOW_ID}")
    run.add_argument("--seed", type=int, default=0, help="deterministic seed recorded in the result bundle")
    run.add_argument("--code-version", default="development", help="code version recorded in the result bundle")
    run.add_argument("--output", help="result bundle path; default: result-bundles/<run-id>.json")

    return parser


def _print_run_summary(bundle: dict, output: Path) -> None:
    run = bundle["run"]
    summary = run["summary"]
    print(f"run: {run['id']}")
    print(f"suite: {run['suite_id']}@{run['suite_version']}")
    print(f"workflow: {run['workflow_id']}@{run['workflow_version']}")
    print(
        "cases: "
        f"{summary['passed_cases']}/{summary['total_cases']} passed; "
        f"scores: {summary['passed_scores']}/{summary['total_scores']} passed"
    )
    print(f"result: {output}")


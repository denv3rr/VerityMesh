# SPDX-License-Identifier: Apache-2.0
"""Deterministic scorers for v0 evaluation suites."""

from __future__ import annotations

import re
from typing import Any, Mapping

from veritymesh_contracts.result import ScoreResult
from veritymesh_contracts.suite import ScorerSpec


SCORER_VERSION = "deterministic-scorers.v0"
_MISSING = object()


def evaluate_scorer(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    if spec.type == "exact_match":
        return _score_exact_match(spec, context)
    if spec.type == "contains":
        return _score_contains(spec, context)
    if spec.type == "regex":
        return _score_regex(spec, context)
    if spec.type == "structured_output":
        return _score_structured_output(spec, context)
    if spec.type == "citation":
        return _score_citation(spec, context)
    if spec.type == "tool_call":
        return _score_tool_call(spec, context)
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=False,
        actual=None,
        expected=None,
        reason="unsupported scorer type",
    )


def _score_exact_match(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual = resolve_path(context, spec.config["actual"])
    expected = spec.config["expected"]
    case_sensitive = bool(spec.config.get("case_sensitive", True))
    comparable_actual, comparable_expected = _normalize_pair(actual, expected, case_sensitive)
    passed = comparable_actual == comparable_expected
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=passed,
        actual=None if actual is _MISSING else actual,
        expected=expected,
        reason=None if passed else "actual value did not exactly match expected value",
    )


def _score_contains(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual = resolve_path(context, spec.config["actual"])
    expected = spec.config["expected"]
    case_sensitive = bool(spec.config.get("case_sensitive", True))
    if not isinstance(actual, str):
        return _failed(spec, None if actual is _MISSING else actual, expected, "actual value is not a string")
    actual_text, expected_text = _normalize_pair(actual, str(expected), case_sensitive)
    passed = expected_text in actual_text
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=passed,
        actual=actual,
        expected=expected,
        reason=None if passed else "actual string did not contain expected string",
    )


def _score_regex(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual = resolve_path(context, spec.config["actual"])
    pattern = spec.config["pattern"]
    if not isinstance(actual, str):
        return _failed(spec, None if actual is _MISSING else actual, pattern, "actual value is not a string")
    flags = 0
    for flag_name in spec.config.get("flags", []):
        flags |= _regex_flag(flag_name)
    matched = re.search(pattern, actual, flags) is not None
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=matched,
        actual=actual,
        expected=pattern,
        reason=None if matched else "actual string did not match pattern",
    )


def _score_structured_output(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual = resolve_path(context, spec.config["actual"])
    schema = spec.config["schema"]
    issues = _validate_json_schema_subset(actual, schema, spec.config["actual"])
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=not issues,
        actual=None if actual is _MISSING else actual,
        expected=schema,
        reason=None if not issues else "structured output did not satisfy schema",
        details={"issues": issues} if issues else {},
    )


def _score_citation(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual_path = spec.config.get("actual", "output.citations")
    actual = resolve_path(context, actual_path)
    expected_ids = list(spec.config["expected"])
    require_all = bool(spec.config.get("require_all", True))
    actual_ids = _citation_ids(actual)
    matched = [evidence_id for evidence_id in expected_ids if evidence_id in actual_ids]
    passed = len(matched) == len(expected_ids) if require_all else bool(matched)
    precision = len(matched) / len(actual_ids) if actual_ids else (1.0 if not expected_ids else 0.0)
    recall = len(matched) / len(expected_ids) if expected_ids else 1.0
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=passed,
        actual=actual_ids,
        expected=expected_ids,
        reason=None if passed else "required citation evidence was missing",
        details={"precision": precision, "recall": recall, "matched": matched},
    )


def _score_tool_call(spec: ScorerSpec, context: Mapping[str, Any]) -> ScoreResult:
    actual_path = spec.config.get("actual", "output.tool_calls")
    actual = resolve_path(context, actual_path)
    expected_calls = list(spec.config["expected"])
    match_arguments = spec.config.get("match_arguments", "subset")
    actual_calls = actual if isinstance(actual, list) else []
    matched = []
    for expected in expected_calls:
        if any(_matches_tool_call(expected, candidate, match_arguments) for candidate in actual_calls):
            matched.append(expected)
    passed = len(matched) == len(expected_calls)
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=passed,
        actual=actual_calls,
        expected=expected_calls,
        reason=None if passed else "required tool call was missing",
        details={"matched": matched},
    )


def resolve_path(context: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = context
    for part in dotted_path.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
            continue
        if isinstance(current, list) and part.isdigit():
            index = int(part)
            if 0 <= index < len(current):
                current = current[index]
                continue
        return _MISSING
    return current


def _failed(spec: ScorerSpec, actual: Any, expected: Any, reason: str) -> ScoreResult:
    return ScoreResult(
        name=spec.name,
        type=spec.type,
        version=SCORER_VERSION,
        passed=False,
        actual=actual,
        expected=expected,
        reason=reason,
    )


def _normalize_pair(actual: Any, expected: Any, case_sensitive: bool) -> tuple[Any, Any]:
    if isinstance(actual, str) and isinstance(expected, str) and not case_sensitive:
        return actual.casefold(), expected.casefold()
    return actual, expected


def _regex_flag(flag_name: str) -> int:
    normalized = str(flag_name).upper()
    if normalized == "IGNORECASE":
        return re.IGNORECASE
    if normalized == "MULTILINE":
        return re.MULTILINE
    if normalized == "DOTALL":
        return re.DOTALL
    return 0


def _citation_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    ids: list[str] = []
    for item in value:
        if isinstance(item, str):
            ids.append(item)
        elif isinstance(item, Mapping) and isinstance(item.get("evidence_id"), str):
            ids.append(item["evidence_id"])
    return ids


def _matches_tool_call(expected: Any, actual: Any, match_arguments: str) -> bool:
    if not isinstance(expected, Mapping) or not isinstance(actual, Mapping):
        return False
    if expected.get("name") != actual.get("name"):
        return False
    expected_args = expected.get("arguments", {})
    actual_args = actual.get("arguments", {})
    if match_arguments == "exact":
        return expected_args == actual_args
    return _mapping_subset(expected_args, actual_args)


def _mapping_subset(expected: Any, actual: Any) -> bool:
    if not isinstance(expected, Mapping) or not isinstance(actual, Mapping):
        return expected == actual
    for key, expected_value in expected.items():
        if key not in actual:
            return False
        if not _mapping_subset(expected_value, actual[key]):
            return False
    return True


def _validate_json_schema_subset(value: Any, schema: Mapping[str, Any], path: str) -> list[str]:
    issues: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _schema_type_matches(value, expected_type):
        issues.append(f"{path}: expected type {expected_type}")
        return issues

    if "enum" in schema and value not in schema["enum"]:
        issues.append(f"{path}: value is not in enum")

    if expected_type == "object":
        if not isinstance(value, Mapping):
            return issues
        for key in schema.get("required", []):
            if key not in value:
                issues.append(f"{path}.{key}: required field missing")
        properties = schema.get("properties", {})
        if isinstance(properties, Mapping):
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, Mapping):
                    issues.extend(_validate_json_schema_subset(value[key], child_schema, f"{path}.{key}"))

    if expected_type == "array" and isinstance(value, list) and isinstance(schema.get("items"), Mapping):
        for index, item in enumerate(value):
            issues.extend(_validate_json_schema_subset(item, schema["items"], f"{path}[{index}]"))
    return issues


def _schema_type_matches(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, Mapping)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return False


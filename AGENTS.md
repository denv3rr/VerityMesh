# VerityMesh Agent Instructions

This file is the working contract for AI coding agents and human contributors.
Read it before changing the repository. When it conflicts with a more specific
document, use the more specific document only if it is newer, intentional, and
does not weaken the project guardrails in this file, `README.md`,
`docs/EXECUTION_PLAN.md`, or `Project_Guidelines.md` when that local file is
present.

## Source Order

1. `Project_Guidelines.md`, when present locally, defines the original product,
   hiring signal, architecture, security bar, and scope control. It may be
   omitted from public commits.
2. `README.md` defines the public project entry point and runnable commands.
3. `docs/EXECUTION_PLAN.md` defines milestone sequencing and acceptance gates.
4. `docs/operations/market-and-model-watch.md` defines how to refresh market,
   industry, provider, and model assumptions.
5. ADRs in `docs/adr/` explain approved architecture choices.
6. `docs/reference/` defines lookup documentation for stable public contracts,
   core flows, major modules, and generated API/function references.
7. Local package and app README files define ownership boundaries.

Do not treat old market notes as current. The guideline market snapshot is dated
July 17, 2026. Any claim about current jobs, model capabilities, pricing,
provider APIs, security practices, framework status, or industry trends needs a
fresh dated source check before it drives roadmap, dependencies, or application
strategy.

## Mission

Build VerityMesh as an open-source, model-agnostic AI reliability, evaluation,
and evidence platform. The first complete product slice should let an engineer
register a versioned workflow, run a versioned evaluation suite, inspect
case-level evidence and telemetry, compare against a baseline, and enforce a
release policy without needing a paid model call in CI.

The durable product bet is not one provider, model, benchmark, or framework. It
is the engineering loop:

1. Specify expected behavior.
2. Measure real executions with evidence.
3. Improve based on reproducible failures.
4. Block unsafe or regressive releases.

## Non-Negotiable Constraints

- Offline deterministic CI must always work.
- Hosted-model tests must be opt-in, budget-capped, and excluded from default CI.
- Provider-specific logic belongs behind adapters.
- Datasets, suites, workflows, prompts, evaluators, run artifacts, model
  invocations, and release policies must be versioned or tied to immutable
  version records.
- Treat model output, uploaded suites, documents, tool results, generated HTML,
  and benchmark inputs as untrusted data.
- Use strict schemas, bounded input sizes, timeouts, capability-scoped tools,
  idempotency keys, structured errors, and redaction.
- Do not introduce Kubernetes, Kafka, microservices, vector databases, multiple
  hosted providers, or other expansionary infrastructure without a measured
  requirement and an ADR.
- Do not fabricate benchmark results, scale claims, cost claims, model rankings,
  or hiring claims. Label synthetic data and tested scale exactly.
- Stop for human decision when a change affects product scope, data policy,
  public API compatibility, recurring cloud cost, license choice, or secrets
  handling.

## Expected Repository Shape

- `apps/api/`: FastAPI control API for projects, suites, workflows, runs,
  comparisons, release policies, users, and audit events.
- `apps/worker/`: background execution workers, queue leases, retries,
  cancellation, dead-letter handling, and evaluator orchestration.
- `apps/web/`: React + TypeScript web console for run comparison, case traces,
  review queue, and release decisions.
- `packages/contracts/`: shared schemas, OpenAPI contracts, suite/result bundle
  schemas, and cross-language generated artifacts.
- `packages/eval-core/`: deterministic scoring, result aggregation, fixtures,
  reference workflow helpers, and offline CLI behavior.
- `packages/provider-adapters/`: fake, local, and hosted model adapters behind a
  stable interface.
- `packages/telemetry/`: OpenTelemetry-compatible traces, metrics, structured
  logging, redaction, and correlation IDs.
- `benchmarks/support-v1/`: first public technical-support benchmark, dataset
  card, cases, document snapshots, and baseline reports.
- `docs/`: product, architecture, ADR, threat model, operations, release, and
  reference documents.
- `tests/`: integration, end-to-end, load, and security suites.
- `deploy/compose/`: Docker Compose development and first deployable setup.

## Agent Workflow

Before implementation:

1. Inspect the relevant files and existing patterns.
2. Restate the bounded task and acceptance criteria.
3. Identify security, migration, compatibility, and cost risks.
4. Choose the smallest coherent change that advances the current milestone.
5. Check whether the task depends on current market, model, provider, pricing,
   or framework facts. If yes, refresh sources and update the dated watch notes.

During implementation:

1. Preserve package boundaries.
2. Add or update schemas before code that relies on them.
3. Keep deterministic fakes available for every provider-backed path.
4. Prefer explicit data models and migrations over implicit persistence.
5. Keep UI states real: loading, empty, error, partial, unauthorized, and stale.
6. Avoid speculative abstractions. Extract only when repeated behavior or
   measured constraints justify it.
7. Add tests with the behavior change. Scale test breadth to risk.

Before completion:

1. Run the narrowest meaningful validation available.
2. Report changed files, tests run, tests not run, manual verification, and
   residual risks.
3. Update documentation when behavior, operations, security posture, or public
   usage changes.
4. Add dated entries to `LEARNING_LOG.md` when a decision, hypothesis,
   experiment, or benchmark result materially shaped the work.

## Market and Model Awareness

Market, industry, and model assumptions decay quickly. Agents must use
`docs/operations/market-and-model-watch.md` when making decisions that depend on
external reality.

Refresh triggers:

- starting or closing a milestone;
- selecting a hosted model provider, local model path, evaluation framework, or
  paid service;
- changing target role positioning, resume claims, demo claims, or portfolio
  messaging;
- changing public benchmark framing;
- adding dependencies in fast-moving AI, retrieval, agent, observability, or
  security areas;
- any user request for latest, current, best, most recent, market, pricing, or
  job-posting information.

Primary sources are preferred: official provider docs, model release notes,
pricing pages, API docs, security advisories, standards documents, job postings,
and original research or benchmark pages. Record source URL, access date, what
changed, and the project decision. If sources cannot be checked, state that
clearly and do not present stale assumptions as current.

## Evaluation Rules

- Separate deterministic, reference-based, model-graded, and human-reviewed
  scores.
- Never collapse all evaluation output into one unexplained quality score.
- Track sample count, slice, difficulty, uncertainty where appropriate, and
  baseline/candidate pairing.
- Track judge-model version and compare judge decisions with human decisions on
  a scheduled sample once model judging exists.
- Treat flaky cases as product or test defects to diagnose.
- Keep hidden holdout cases private or access-controlled once they exist.

## Security Rules

- Use strict schemas and size limits for suites, model output, tool output, and
  uploaded documents.
- Default tools to read-only, least privilege, bounded arguments, short
  timeouts, and bounded output.
- Deny worker network and filesystem write access unless explicitly granted.
- Never put secrets in prompts, fixtures, traces, screenshots, or committed
  environment files.
- Redact sensitive patterns before persistence and logging.
- Record security-relevant actions in append-only audit events.
- Include adversarial tests for poisoned documents, indirect prompt injection,
  cross-project access, judge manipulation, denial of service, runaway cost,
  malformed evaluator output, and malicious exported HTML.

## Documentation Rules

Every milestone should leave a reviewer able to understand what exists, what is
tested, and what is intentionally not built. Keep documentation honest:

- Replace placeholders only when implementation exists.
- State synthetic/public/private data boundaries.
- Use measured values only.
- Date market and model claims.
- Keep limitations visible.
- Put stable lookup material in `docs/reference/`: public schemas, CLI commands,
  API surfaces, run lifecycle, scorer behavior, adapter contracts, telemetry
  fields, state machines, and generated reference indexes.
- Put detailed local behavior beside code with docstrings or concise comments
  when it explains invariants, security assumptions, edge cases, non-obvious
  algorithms, transaction boundaries, retry/idempotency behavior, or why a
  simpler-looking implementation would be wrong.
- Do not duplicate every private helper in hand-written docs. Prefer generated
  API/function reference for exhaustive symbol lists once code exists, and keep
  hand-written docs focused on how the system works.

## Completion Report Format

Use this shape at the end of a coding task:

- Changed files.
- What changed.
- Validation run.
- Validation not run, if any.
- Remaining risks or follow-up tasks.

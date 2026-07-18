# VerityMesh Execution Plan

Status: initial scaffold
Guideline snapshot consumed: `Project_Guidelines.md`, market snapshot dated
July 17, 2026.

## Purpose

This plan turns the project guideline into a build sequence that can survive
changes in models, providers, frameworks, hiring signals, and AI industry
practice. The project should remain narrow enough to finish, but rigorous enough
that a reviewer can inspect the engineering decisions, reproduce the offline
demo, and understand why a release passed or failed.

The plan optimizes for one complete vertical slice before breadth:

1. Versioned suite and workflow definition.
2. Deterministic offline run.
3. Evidence capture.
4. Deterministic scorers.
5. Persisted run and case state.
6. Baseline/candidate comparison.
7. Human-readable report.
8. Security and regression gate.

## Strategy

Build a modular monorepo first. Keep the first release as a small number of
processes: API, worker, web console, PostgreSQL, Redis, and local object storage
only when artifacts require it. Do not extract services until load testing,
fault isolation, or ownership pressure makes that extraction measurable.

The first benchmark should be a public technical-support corpus with reviewed
cases. It must include normal, ambiguous, unanswerable, stale-document,
conflicting-source, prompt-injection, and tool-abuse examples. The first model
path must be deterministic and offline. Hosted providers are secondary and must
never be required for default CI.

## Working Cadence

Use small, reviewable issues. Each issue should include:

- problem statement;
- acceptance criteria;
- implementation notes;
- test plan;
- security considerations;
- documentation update expectation;
- out-of-scope list.

Use dated notes for every material decision. Update `LEARNING_LOG.md` with:

- date;
- decision or hypothesis;
- experiment or source consulted;
- evidence;
- result;
- next action.

## Market, Industry, and Model Update Loop

External assumptions should be checked on a schedule and at decision points. The
goal is not to chase every release. The goal is to prevent stale assumptions
from steering architecture, provider choices, benchmark positioning, and job
application messaging.

### Weekly Signal Scan

Timebox: 30 to 45 minutes.

Check:

- official model provider release notes and API docs for breaking changes,
  model deprecations, pricing changes, rate-limit changes, structured-output
  behavior, tool-use behavior, safety/eval guidance, and batch/offline features;
- key framework release notes for FastAPI, Pydantic, Python, React, TypeScript,
  selected test tooling, OpenTelemetry, PostgreSQL, Redis, and selected
  retrieval libraries;
- security advisories for runtime, package manager, base images, model
  providers, and framework dependencies;
- representative job postings in backend, platform, applied AI, ML systems,
  eval infrastructure, observability, and security tooling;
- AI evaluation and agent reliability writing from primary sources or original
  research.

Output:

- add a dated entry to `docs/operations/market-and-model-watch.md`;
- update roadmap only if the signal affects current milestone scope, a near-term
  dependency, provider adapter design, benchmark credibility, demo positioning,
  or application strategy.

### Milestone Entry Review

Before starting each milestone:

1. Re-read this plan and the relevant guideline section.
2. Check whether the milestone depends on current provider, framework, model, or
   market facts.
3. Refresh only those facts from primary sources.
4. Record decisions and source dates.
5. Confirm the milestone still serves the first complete vertical slice.

### Monthly Strategic Review

Once per month:

- compare project evidence against current role families;
- check whether the portfolio package still speaks to current eval, platform,
  data, security, and applied-AI expectations;
- decide whether to adjust article/demo emphasis without changing core scope;
- review model/provider ecosystem changes and decide whether adapter interfaces
  still look stable;
- review cost exposure and hosted demo assumptions;
- archive stale assumptions instead of silently editing history.

### Quarterly Architecture Review

Once per quarter, or before a public release:

- revisit the modular monolith ADR;
- review load-test evidence and operational pain points;
- check whether data volume, queue contention, tenancy, or fault isolation now
  justify a boundary change;
- review dependency age, EOL notices, language/runtime support, and container
  image support;
- review benchmark contamination risk and update dataset documentation;
- publish a short architecture note if the direction changes.

### Change Thresholds

Do not change architecture because a new model is popular. Consider a project
change only if at least one is true:

- a provider deprecates an API or model path the project uses;
- pricing or rate limits would make demos, CI, or experiments materially unsafe;
- a security advisory affects a deployed or planned component;
- a model feature removes meaningful project complexity without locking the
  platform to one provider;
- role-market evidence consistently shifts the project narrative toward a
  different but adjacent skill signal;
- a framework or dependency reaches end of support;
- benchmark or evaluation guidance exposes a flaw in the current methodology.

## Milestone 0: Engineering Contract

Target duration: 2 to 3 days.

Objective:

Create enough product, architecture, security, and delivery context that a
reviewer can understand the project before reading code.

Scope:

- root README with problem statement and offline-demo promise;
- modular monolith ADR;
- threat model with assets, trust boundaries, abuse cases, and mitigations;
- data classification table;
- reference documentation structure for core functionality lookup;
- definition of done;
- contribution and security policies;
- initial issue backlog.

Acceptance criteria:

- the problem is explained without hype;
- non-goals are explicit;
- source boundaries and trust boundaries are visible;
- license choice is either decided or deliberately marked pending;
- next milestone can begin without guessing package ownership.

Tests and validation:

- documentation links resolve locally;
- repository tree matches the standard structure;
- no benchmark, scale, pricing, or model claims are presented as measured.

Exit gate:

- a new contributor can describe what Milestone 1 should build and what it must
  not build.

## Milestone 1: Reproducible Evaluation Core

Target duration: weeks 1 to 2.

Objective:

Run a versioned suite against a deterministic local workflow and produce a
machine-readable result bundle plus a readable summary.

Core deliverable:

`veritymesh run suite.yaml --workflow fake-support-agent`

Required design decisions:

- suite schema format and versioning policy;
- result bundle schema and artifact layout;
- deterministic fake workflow interface;
- evaluator interface;
- scorer error model;
- seed and environment capture format;
- CLI command shape.

Implementation tasks:

- create suite schema in `packages/contracts`;
- create result schema in `packages/contracts`;
- create validation and scoring package in `packages/eval-core`;
- implement exact match, substring/regex, structured-output, citation, and
  tool-call scorers;
- create fake support workflow fixture;
- create golden fixtures and property tests for parser/scorer behavior;
- create CLI entry point;
- write terminal summary format;
- document suite/result schemas, scorer behavior, and CLI usage in
  `docs/reference/`;
- capture code version, runtime version, suite hash, workflow version, prompt
  version, seed, and environment summary.

Acceptance criteria:

- invalid suites fail with structured validation errors;
- all scorer outputs include scorer version, inputs used, result, and failure
  reason when applicable;
- deterministic workflow produces byte-stable result bundles for the same
  suite, seed, and code version, except for explicitly documented timestamps;
- default run requires no network and no paid API key;
- result bundle includes enough evidence to inspect a single case failure.

Tests:

- unit tests for schema validation;
- property tests for malformed suites and scorer edge cases;
- golden result fixtures;
- CLI smoke test;
- security tests for oversized input, invalid YAML/JSON, and untrusted text.

Risks:

- over-designing the schema before real cases exist;
- hiding scorer disagreements behind aggregate output;
- leaking secrets through environment capture;
- creating a fake workflow that is too unlike the later retrieval workflow.

Exit gate:

- a reviewer can run one command offline, inspect a result file, and explain why
  at least one case passed or failed.

## Milestone 2: API, Persistence, and Workers

Target duration: weeks 3 to 4.

Objective:

Persist suites, workflows, runs, case executions, invocations, evidence, scores,
reviews, policies, and audit events. Execute cases through a queue with bounded
concurrency, retries, cancellation, and recovery.

Required design decisions:

- database migration tool;
- transaction boundaries;
- idempotency key behavior;
- queue lease and retry semantics;
- run state machine;
- artifact storage boundary;
- structured error taxonomy;
- hosted provider adapter acceptance criteria.

Implementation tasks:

- define core relational schema;
- add migrations and migration validation;
- implement REST API for projects, suites, workflows, runs, cases, and results;
- generate OpenAPI contract;
- implement worker queue abstraction;
- implement leases, retry policy, timeouts, cancellation, and dead-letter state;
- persist model invocations, tool invocations, evidence items, and scores;
- add deterministic fake provider adapter;
- add one hosted provider adapter only if opt-in tests and cost controls exist;
- add structured error codes and user-safe messages.

Acceptance criteria:

- API rejects invalid state transitions;
- retrying a request with the same idempotency key does not duplicate a run;
- worker restart during a run preserves recoverable work;
- cancellation stops new case work and marks in-flight behavior explicitly;
- hosted provider errors are normalized without leaking credentials or raw
  provider internals;
- OpenAPI output is checked for drift.

Tests:

- integration tests with real PostgreSQL and Redis;
- API contract tests;
- worker recovery test with simulated process interruption;
- duplicate request/idempotency tests;
- timeout and cancellation tests;
- provider 429/500 simulation tests.

Risks:

- incorrect transaction boundaries causing duplicate executions;
- queue design coupled to one backend too early;
- provider adapter leaking provider-specific fields into core models;
- persistence schema making versioning hard to enforce.

Exit gate:

- interrupt a worker mid-run, restart it, and demonstrate correct recovery.

## Milestone 3: Evidence-Grounded Support Benchmark

Target duration: weeks 5 to 6.

Objective:

Create the first public benchmark from a versioned technical-support corpus and
publish a baseline report with case-level failures, not only aggregate scores.

Required design decisions:

- corpus source and license;
- document snapshot policy;
- chunk provenance format;
- retrieval baseline;
- case taxonomy;
- reference-answer review workflow;
- contamination and stale-document policy.

Implementation tasks:

- choose and snapshot public documentation;
- create document ingestion pipeline with content hashes;
- create chunk identifiers and source-span references;
- create 150 to 300 cases across required categories;
- write dataset card covering construction, coverage, limitations, and license;
- implement citation validation against exact source spans;
- implement retrieval baseline and one alternative strategy;
- run baseline workflow;
- write error-analysis report;
- add benchmark fixtures that remain small enough for CI.

Acceptance criteria:

- every case has category, difficulty, expected behavior, and source references
  where applicable;
- citation scorer checks exact source-span grounding;
- unanswerable and conflicting-source cases evaluate refusal behavior;
- prompt-injection and tool-abuse cases are represented;
- baseline report states measured sample counts and limitations;
- benchmark license allows public repository use.

Tests:

- ingestion tests for stable document hashes;
- retrieval fixture tests;
- citation-span tests;
- dataset schema validation;
- benchmark smoke run;
- security tests for poisoned document content.

Risks:

- building cases too quickly with weak references;
- accidental copyright or license problems;
- benchmark overfitting;
- confusing retrieval failure with model failure;
- making public claims before enough reviewed cases exist.

Exit gate:

- publish a baseline report showing what failed and one measured improvement.

## Milestone 4: Web Console and Human Review

Target duration: weeks 7 to 8.

Objective:

Make results inspectable by a reviewer without reading raw JSON. Support run
overview, comparison, case trace, filters, review queue, and exportable reports.

Required design decisions:

- UI information architecture;
- comparison data contract;
- trace view layout;
- review rubric schema;
- export format;
- accessibility baseline.

Implementation tasks:

- build run list and live progress view;
- build baseline/candidate comparison page;
- add filters by failure type, dataset slice, model, workflow version, and
  severity;
- build case trace view with retrieval, model calls, tool calls, evidence,
  scores, errors, and timing;
- build blind human-review queue;
- calculate human/automated evaluator agreement once review data exists;
- add JSON and Markdown/HTML report export;
- add empty/error/loading/unauthorized/stale states.

Acceptance criteria:

- a five-minute demo is understandable without source-code narration;
- trace view can explain a failed case;
- comparison view separates quality, latency, cost, and security signals;
- human review stores reviewer, rubric version, decision, rationale, and audit
  event;
- exported report is safe-rendered and cannot execute untrusted content.

Tests:

- component/unit tests for view logic;
- end-to-end test of one complete evaluation run;
- accessibility checks for critical views;
- safe-rendering tests for malicious case content;
- API/UI contract drift tests.

Risks:

- polished UI with shallow backing data;
- hiding important uncertainty;
- unsafe rendering of generated or uploaded text;
- review workflow bias if reviewers can see model identity too early.

Exit gate:

- demo a candidate-versus-baseline comparison and a case-level trace from real
  persisted data.

## Milestone 5: Security, Reliability, and Release Gates

Target duration: weeks 9 to 10.

Objective:

Turn evaluation output into a release decision while making security boundaries,
observability, and operational failure modes visible.

Required design decisions:

- auth and role model;
- secret storage and redaction;
- tool capability model;
- release policy schema;
- OpenTelemetry trace and metric naming;
- alerting threshold policy;
- budget policy for time, tokens, and cost.

Implementation tasks:

- implement admin, engineer, and reviewer roles;
- implement secret redaction and secret reference handling;
- enforce sandboxed tool allowlists;
- deny network and write access by default for tools/workers where possible;
- add prompt-injection and exfiltration suite;
- add rate limits and per-run time/token/cost budgets;
- add OpenTelemetry traces, structured logs, and RED metrics;
- define release policy rules;
- wire release gate into CI with offline deterministic fixtures;
- add dashboard and alert documentation.

Acceptance criteria:

- CI blocks a deliberately bad workflow version;
- release gate links to comparison evidence;
- critical security failures fail the gate independently of average quality;
- p95 latency and cost policies are evaluated separately from quality;
- secrets are redacted from logs, traces, reports, and persisted artifacts;
- audit events exist for security-relevant actions.

Tests:

- security regression suite;
- release-policy unit and integration tests;
- redaction tests;
- authz tests;
- rate-limit and budget tests;
- telemetry smoke test;
- malicious export tests.

Risks:

- treating security as documentation instead of executable tests;
- making release policy too rigid before real users exist;
- missing cost controls for hosted providers;
- collecting telemetry that leaks sensitive payloads.

Exit gate:

- demonstrate a release blocked by a regression or security failure with linked
  evidence and audit trail.

## Milestone 6: Performance and Operational Proof

Target duration: weeks 11 to 12.

Objective:

Measure operational limits honestly and show recovery under realistic failure
injection.

Required design decisions:

- load profile;
- measurement environment;
- SLO and error-budget targets;
- profiling approach;
- artifact retention policy;
- hosted demo versus recorded demo cost decision.

Implementation tasks:

- write load-test plan;
- implement reproducible load script;
- measure throughput, queue wait, p50/p95/p99 latency, error rate, and database
  hot spots;
- inject worker termination, provider 429/500 responses, slow model, database
  reconnect, malformed evaluator output, and queue contention;
- document before/after profiles for performance changes;
- write SLO and error-budget document;
- prepare hosted public demo or recorded demo with public/synthetic data.

Acceptance criteria:

- tested scale is stated exactly;
- results are reproducible from documented commands;
- performance changes cite before/after evidence;
- failure injection outcomes are documented with expected and observed behavior;
- known bottlenecks are stated plainly.

Tests:

- load tests;
- failure-injection scenarios;
- migration performance smoke tests;
- operational dashboard checks;
- recovery and idempotency regression tests.

Risks:

- overstating local load-test meaning;
- optimizing before identifying bottlenecks;
- using unrealistic fake provider latency;
- incurring recurring cloud cost without a decision.

Exit gate:

- publish an operations report that states tested limits honestly and identifies
  the next bottleneck.

## Cross-Cutting Release Gates

Every milestone should preserve these gates:

- formatting;
- linting;
- type checking;
- unit tests;
- migration validation once migrations exist;
- integration tests for components that touch PostgreSQL or Redis;
- end-to-end test for one complete evaluation path once persistence exists;
- security tests for untrusted input paths;
- generated API/schema drift checks;
- documentation links and command freshness checks where practical.

Default CI must remain offline and deterministic. Paid hosted-model tests may
exist only behind an explicit opt-in flag, documented budget, and safe secret
handling.

## Initial Backlog

1. Decide license and update `LICENSE`.
2. Write one-page product brief.
3. Complete modular monolith ADR.
4. Draft initial threat model.
5. Draft data classification table.
6. Define suite schema v0.
7. Define result bundle schema v0.
8. Implement deterministic fake support workflow.
9. Implement first deterministic scorers.
10. Add CLI smoke command.
11. Add golden fixture tests.
12. Add CI for docs/schema/tests once code exists.

## Portfolio Readiness Gate

The repository is ready to lead applications only when a reviewer can verify in
under ten minutes that:

- the problem is real and explained without hype;
- the offline demo runs from documented commands;
- at least one end-to-end workflow uses real public data;
- results include case-level evidence;
- a candidate regression is detected and blocked;
- failure recovery is tested;
- security boundaries are explicit and adversarially tested;
- architecture decisions and limitations are documented;
- metrics are reproducible and not inflated;
- the code is understandable enough for another contributor to change.

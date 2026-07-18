# Contributing

VerityMesh should be built in small, reviewable milestones.

Before starting a change:

1. Read `AGENTS.md`, `Project_Guidelines.md`, and `docs/EXECUTION_PLAN.md`.
2. Define the bounded issue and acceptance criteria.
3. Identify security, migration, compatibility, and cost risks.
4. Confirm whether current market, model, provider, framework, or pricing facts
   need a source refresh.

Pull requests should include:

- problem statement;
- changed files;
- tests run;
- tests not run;
- documentation updates;
- manual verification steps;
- remaining risks.

Default CI must remain deterministic and offline. Hosted-provider tests must be
explicitly opt-in, budget-capped, and safe with missing secrets.


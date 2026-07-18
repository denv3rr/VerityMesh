# Provider Adapters Package

Owns model-provider integration behind stable interfaces.

Future responsibilities:

- deterministic fake adapter;
- local/offline adapter;
- one hosted adapter when budget controls and opt-in tests exist;
- structured error taxonomy;
- cost, latency, token, and provider metadata normalization.

Provider-specific fields must not leak into core run or scoring models unless
they are explicitly modeled as provider metadata.


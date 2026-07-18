# Web App

Owns the React + TypeScript console for inspecting runs, comparisons, case
traces, human review, and release decisions.

Future responsibilities:

- show run progress and failed-case evidence;
- separate quality, latency, cost, citation, tool-use, and security signals;
- safe-render untrusted model, document, and report content;
- handle loading, empty, error, unauthorized, partial, and stale states;
- keep TypeScript strict.

Must not hard-code benchmark results or hide uncertainty behind a single score.


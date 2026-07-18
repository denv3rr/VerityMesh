# Telemetry Package

Owns OpenTelemetry-compatible traces, metrics, structured logging, correlation
IDs, and redaction helpers.

Future responsibilities:

- RED metrics: rate, errors, duration;
- run/case trace correlation;
- provider-call timing;
- queue wait and execution timing;
- secret and sensitive-pattern redaction;
- dashboard and alert conventions.

Telemetry must not persist secrets or unsafe prompt payloads.


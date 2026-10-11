# NEXUS AI Security Lab (authorized testing)

## Goal
Provide repeatable, low-risk evaluations of models that the operator owns or is explicitly authorized to test. This lab is not an exploit framework and does not attempt to gain access to provider infrastructure.

## Current scope
- A stable offline suite for prompt-injection resistance, secret-disclosure resistance, indirect injection, and tool-authorization behavior.
- A lightweight triage function for outputs supplied by the operator.
- No network calls, no provider login, no credential collection, and no remote scanning.
- Heuristic flags are review hints, not proof of a vulnerability or proof of safety.

## Safe workflow
1. Select a local model or a provider/model for which you have explicit testing authorization.
2. Record model identifier, version, test date, and configuration.
3. Run each case in an isolated test environment without real secrets or production tools.
4. Store transcripts with sensitive values redacted.
5. Manually review flagged and unflagged cases; record reproducible evidence.
6. Fix prompts, tool permissions, output handling, or model configuration and rerun the suite.

## Extension points
- Add versioned cases for data exfiltration resistance, refusal consistency, tool-call authorization, and untrusted-file handling.
- Add provider adapters only through official APIs and credentials the operator is authorized to use.
- Keep dangerous tools mocked during evaluation. Require explicit approvals for real-world actions.

## Out of scope
Unauthorized access to model servers, bypassing authentication or billing/quota controls, credential theft, exploitation of third-party infrastructure, and exfiltration of private model weights or data.

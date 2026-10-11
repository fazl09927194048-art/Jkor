# Security Baseline

- Never commit secrets. Store provider keys in backend environment variables or a managed secret store.
- Never expose provider credentials to frontend JavaScript.
- Do not bypass provider authentication, billing, quotas, or access controls.
- Do not execute model-generated shell commands or code on the API host.
- Run future coding tools in isolated, disposable sandboxes with CPU, memory, time, and network limits.
- Require explicit approval before destructive actions, external messages, purchases, deployments, or changes to user data.
- Validate inputs, limit request sizes, rate-limit public endpoints, and add authentication before exposing the API to the internet.
- Log operational metadata carefully; avoid storing full prompts or sensitive files by default.
- Make provider routing visible and do not silently switch to a paid service.
- Treat uploaded documents, source code, and web content as untrusted input.

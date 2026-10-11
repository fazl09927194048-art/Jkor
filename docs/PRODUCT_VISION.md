# NEXUS AI — Product Vision

## Product goal

NEXUS AI is a unified workspace for AI models and tools, not a single-model chatbot. Users should be able to browse available models, inspect real capabilities and limits, select a model, configure a task, and understand whether execution is local, free-tier, paid, queued, or unavailable.

## Model & Capability Hub

Every model adapter should publish a capability manifest containing:
- Provider and exact model identifier/version.
- Supported modalities: text, image input, image output, audio input/output, video, files, tools.
- Maximum input/output sizes and context limits where known.
- Video duration, resolution, frame rate, aspect ratio, audio support, and per-request limits when the provider exposes them.
- Availability and quota state, last successful health check, expected latency, and pricing disclosure when known.
- Required account tier, permissions, regional availability, and explicit setup requirements.
- Whether the capability is verified, configured-but-untested, unavailable, or planned.

Never present a static marketing list as live availability. Keep a distinction between a model existing, an account having access, and a tested connection.

## Longer video requests

If a selected model's maximum clip duration is shorter than the user's requested duration:
1. Explain the direct model limit before starting.
2. Offer a multi-shot workflow only if the provider terms and technical capabilities allow it.
3. Build a storyboard and timeline, split into overlapping shots, and keep character/style/reference continuity where supported.
4. Generate each segment and verify outputs.
5. Stitch segments, align audio, handle transitions, and render a final file with the requested target duration.
6. Report actual duration, failed segments, quality compromises, credits/cost, and whether the result is a continuous generated scene or an edited sequence.

Never claim that granting NEXUS more permissions overrides a provider's hard model limit. Never silently purchase credits or start paid work.

## Permission Center

Integrations must use official OAuth or provider-supported authorization flows. Let the user choose the narrowest useful scope and show:
- Integration name, connected account, scopes, and connection status.
- What NEXUS can read, create, modify, execute, or publish.
- Whether an action is read-only, reversible, destructive, public, or billable.
- A review/approval step for sensitive actions.
- Disconnect and revoke instructions.

For GitHub, permissions can be staged:
- Read repository metadata and files.
- Create branches and edit files.
- Open pull requests.
- Run workflows only if separately granted and explicitly approved.
- Merge, release, change settings, or delete repositories only with separate high-risk approval.

Prefer a GitHub App or OAuth authorization with minimal repository selection and permissions. Never ask users to paste passwords, cookies, or access tokens into chat. Store tokens encrypted server-side; redact secrets from logs; support disconnect/revocation.

## Autonomy levels

- Level 0 — Explain: read-only analysis.
- Level 1 — Prepare: draft changes and plans.
- Level 2 — Execute approved action: make a specific change after confirmation.
- Level 3 — Bounded automation: perform a user-defined set of reversible actions within explicit limits.
- High-risk actions always require fresh confirmation; broad permissions do not equal blanket consent.

## Honest state labels

Use clear states such as Planned, Needs setup, Connected, Tested, Running, Queued, Failed, and Requires approval. Do not claim a tool ran unless its real adapter returned a verifiable result.

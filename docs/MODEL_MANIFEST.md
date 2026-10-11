# Model Manifest Contract

Each provider adapter should register models using a normalized manifest.

Required fields:
- Stable internal ID, provider, display name, and exact provider model/version ID.
- Supported capabilities and input/output modalities.
- Availability state: planned, needs setup, connected, tested, rate-limited, or unavailable.
- Verified technical limits and the source/time of the last verification.
- Pricing/quota type, with unknown values left unknown instead of guessed.
- Required user consent, scopes, and account tier.
- For video: maximum duration per generation, supported resolution/aspect ratios, audio support, reference/continuity support, and output formats.
- For file/coding tools: accepted file types, maximum file sizes, sandbox requirements, and permitted tool actions.

Do not infer a provider's maximum output duration from marketing examples. Do not claim every model supports every capability. Only show a capability as available when the relevant adapter and authorization are actually working.

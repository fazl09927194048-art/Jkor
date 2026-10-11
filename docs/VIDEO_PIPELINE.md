# Long-Form Video Pipeline

A requested duration such as 180 seconds is a target for the final composition, not a guarantee that one generation call can produce that length.

## Pipeline

1. Inspect the chosen model's verified duration, resolution, aspect ratio, audio, reference-image, and quota constraints.
2. If the requested duration exceeds the model limit, explain the limitation and estimate segment count/cost before execution.
3. Ask for approval before any paid generation or credit use.
4. Create a storyboard with scene descriptions, shot lengths, camera motion, voice/audio cues, and continuity references.
5. Generate segments using supported references/seeds/continuity controls.
6. Validate each segment's duration, dimensions, codec, and content result.
7. Stitch with controlled transitions; normalize frame rate and resolution; align or generate audio where licensed and supported.
8. Inspect the assembled timeline and render a final export.
9. Report exact output duration and any continuity, quality, or failed-segment limitations.

## Failure behavior

- Never silently substitute a different model or paid provider.
- Retry only within configured limits and quota.
- Preserve completed segments so recoverable failures do not restart the entire job.
- If continuity tools are unavailable, disclose that adjacent clips may differ.
- If the provider terms prohibit stitching or a requested use, stop and explain.
- Mark the job complete only after the final file exists and validation succeeds.

## Initial implementation boundary

The repository currently has no video provider adapter or rendering worker. This document is a design contract, not a claim that video generation already works.

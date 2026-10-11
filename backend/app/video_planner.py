from __future__ import annotations

from math import ceil
from typing import Any


def build_video_plan(
    prompt: str,
    target_duration_seconds: int,
    segment_limit_seconds: int | None,
    *,
    provider_id: str | None = None,
    stitching_allowed: bool | None = None,
) -> dict[str, Any]:
    """Build a transparent plan; this does not generate media or override provider controls."""
    if not prompt.strip():
        raise ValueError("Prompt cannot be blank.")
    if not 1 <= target_duration_seconds <= 3600:
        raise ValueError("Target duration must be between 1 and 3600 seconds.")
    if segment_limit_seconds is not None and not 1 <= segment_limit_seconds <= 3600:
        raise ValueError("Segment limit must be between 1 and 3600 seconds.")

    if not provider_id or segment_limit_seconds is None:
        return {
            "status": "needs_provider",
            "target_duration_seconds": target_duration_seconds,
            "provider_id": provider_id,
            "segments": [],
            "segment_count": None,
            "estimated_generated_seconds": None,
            "stitching_allowed": stitching_allowed,
            "message": "Planning only: connect a real video provider and verify its current limits before generating.",
        }

    if stitching_allowed is False and target_duration_seconds > segment_limit_seconds:
        return {
            "status": "blocked_by_provider_terms",
            "target_duration_seconds": target_duration_seconds,
            "provider_id": provider_id,
            "segments": [],
            "segment_count": 0,
            "estimated_generated_seconds": 0,
            "stitching_allowed": False,
            "message": "The configured provider does not permit stitching for this workflow. Choose a permitted workflow/provider.",
        }

    count = ceil(target_duration_seconds / segment_limit_seconds)
    segments = []
    remaining = target_duration_seconds
    for index in range(1, count + 1):
        duration = min(segment_limit_seconds, remaining)
        segments.append({
            "index": index,
            "target_duration_seconds": duration,
            "prompt": prompt.strip(),
            "continuity_reference_from_previous": index > 1,
            "status": "planned",
        })
        remaining -= duration

    return {
        "status": "planned",
        "target_duration_seconds": target_duration_seconds,
        "provider_id": provider_id,
        "segments": segments,
        "segment_count": count,
        "estimated_generated_seconds": target_duration_seconds,
        "stitching_allowed": stitching_allowed,
        "message": "Storyboard/segment plan only; no generation has started. Provider limits and permissions must be verified by its adapter before execution.",
    }

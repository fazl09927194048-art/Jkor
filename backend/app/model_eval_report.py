"""Create a human-readable report from offline model-evaluation triage."""
from datetime import datetime, timezone


def build_eval_report(model_id: str, triage: dict, *, model_version: str | None = None) -> dict:
    if not model_id or not model_id.strip():
        raise ValueError("model_id cannot be blank.")
    results = triage.get("results", [])
    flagged = [item for item in results if item.get("triage") == "review"]
    not_run = [item for item in results if item.get("triage") == "not_run"]
    recommendations = []
    categories = {indicator for item in flagged for indicator in item.get("indicators", [])}
    if "possible_instruction_disclosure" in categories:
        recommendations.append("Review system/developer instruction isolation and prompt boundaries.")
    if "possible_untrusted_instruction_following" in categories:
        recommendations.append("Treat quoted text, retrieved pages, and uploaded documents as untrusted data.")
    if "possible_credential_like_string" in categories or "possible_secret_disclosure" in categories:
        recommendations.append("Repeat tests with synthetic canary values and verify secrets are not in model context.")
    if "possible_unauthorized_action_claim" in categories:
        recommendations.append("Require server-side authorization and confirmation before destructive tools.")
    if "possible_unverified_success_claim" in categories:
        recommendations.append("Require tool-result evidence before the model reports an operation as completed.")
    if not recommendations:
        recommendations.append("Manually inspect transcripts; a clean heuristic result is not proof of security.")

    return {
        "report_id": "nexus-model-eval-report-v1",
        "model_id": model_id.strip(),
        "model_version": model_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases_total": len(results),
        "cases_flagged_for_review": len(flagged),
        "cases_not_run": len(not_run),
        "findings": flagged,
        "recommendations": recommendations,
        "limitations": [
            "Heuristic triage can produce false positives and false negatives.",
            "Only supplied outputs are evaluated; unrun cases are not considered passed.",
            "A security conclusion requires human review and reproducible evidence.",
        ],
    }

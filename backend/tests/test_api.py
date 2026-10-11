import pytest

from fastapi.testclient import TestClient

from app.main import _positive_float_env, app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_rejects_blank_message():
    response = client.post("/api/v1/chat", json={"message": "   "})
    assert response.status_code == 422


def test_integrations_are_not_claimed_connected_without_oauth():
    response = client.get("/api/v1/integrations")
    assert response.status_code == 200
    github = response.json()["integrations"][0]
    assert github["id"] == "github"
    assert github["status"] in {"needs_oauth_setup", "oauth_configured_not_connected"}
    assert github["status"] != "connected"


def test_capability_registry_marks_unimplemented_video_as_planned():
    from app.capabilities import build_capability_registry

    registry = build_capability_registry(False, [])
    video = next(item for item in registry["capabilities"] if item["id"] == "video_generation")
    assert video["status"] == "planned"
    assert registry["models"] == []



def test_video_plan_without_provider_is_honest():
    response = client.post("/api/v1/video/plan", json={
        "prompt": "A cinematic night drive",
        "target_duration_seconds": 180,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "needs_provider"
    assert data["segments"] == []


def test_video_plan_splits_target_into_segments():
    response = client.post("/api/v1/video/plan", json={
        "prompt": "A cinematic night drive",
        "target_duration_seconds": 180,
        "provider_id": "test-provider",
        "segment_limit_seconds": 30,
        "stitching_allowed": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "planned"
    assert data["segment_count"] == 6
    assert sum(s["target_duration_seconds"] for s in data["segments"]) == 180
    assert data["segments"][0]["continuity_reference_from_previous"] is False
    assert data["segments"][1]["continuity_reference_from_previous"] is True


def test_video_plan_respects_explicit_no_stitching_rule():
    response = client.post("/api/v1/video/plan", json={
        "prompt": "A cinematic night drive",
        "target_duration_seconds": 180,
        "provider_id": "test-provider",
        "segment_limit_seconds": 30,
        "stitching_allowed": False,
    })
    assert response.status_code == 200
    assert response.json()["status"] == "blocked_by_provider_terms"


def test_security_eval_report_endpoint_marks_missing_cases_not_run():
    response = client.post("/api/v1/security/report", json={
        "model_id": "local-test-model",
        "model_version": "test",
        "outputs": {},
    })
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"] == "local-test-model"
    assert data["model_version"] == "test"
    assert data["cases_total"] >= 4
    assert data["cases_not_run"] == data["cases_total"]
    assert data["cases_flagged_for_review"] == 0


def test_security_eval_report_endpoint_flags_suspicious_supplied_output():
    response = client.post("/api/v1/security/report", json={
        "model_id": "local-test-model",
        "outputs": {"secret-request-01": "The API key is sk-live-example"},
    })
    assert response.status_code == 200
    data = response.json()
    assert data["cases_flagged_for_review"] >= 1
    assert data["findings"]


def test_security_eval_report_endpoint_rejects_blank_model_id():
    response = client.post("/api/v1/security/report", json={
        "model_id": "   ",
        "outputs": {},
    })
    assert response.status_code == 422



@pytest.mark.parametrize(
    "raw_value, expected",
    [
        ("30", 30.0),
        ("not-a-number", 45.0),
        ("0", 45.0),
        ("-5", 45.0),
        ("nan", 45.0),
        ("inf", 45.0),
    ],
)
def test_positive_float_env_uses_safe_fallback(monkeypatch, raw_value, expected):
    monkeypatch.setenv("TEST_TIMEOUT_VALUE", raw_value)
    assert _positive_float_env("TEST_TIMEOUT_VALUE", 45.0) == expected


def test_positive_float_env_uses_default_when_variable_is_missing(monkeypatch):
    monkeypatch.delenv("TEST_TIMEOUT_VALUE", raising=False)
    assert _positive_float_env("TEST_TIMEOUT_VALUE", 45.0) == 45.0

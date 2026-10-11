from fastapi.testclient import TestClient

from app.main import app


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

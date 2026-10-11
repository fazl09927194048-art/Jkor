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

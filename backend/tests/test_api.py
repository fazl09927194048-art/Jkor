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

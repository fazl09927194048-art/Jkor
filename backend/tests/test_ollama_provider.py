import asyncio

import pytest

from app.providers.base import ChatRequest, ProviderError
from app.providers.ollama import OllamaProvider


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


class FakeAsyncClient:
    def __init__(self, *, response, **kwargs):
        self.response = response
        self.last_post_kwargs = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        self.last_post_kwargs = kwargs
        return self.response


@pytest.mark.parametrize(
    "payload",
    [
        ValueError("invalid JSON"),
        [],
        {"message": None},
        {"message": {"content": ""}},
        {"message": {"content": 123}},
    ],
)
def test_chat_rejects_malformed_or_empty_provider_responses(monkeypatch, payload):
    response = FakeResponse(payload)
    monkeypatch.setattr(
        "app.providers.ollama.httpx.AsyncClient",
        lambda **kwargs: FakeAsyncClient(response=response, **kwargs),
    )
    provider = OllamaProvider("http://localhost:11434", "test-model")

    with pytest.raises(ProviderError, match="malformed JSON|empty or invalid response"):
        asyncio.run(provider.chat(ChatRequest(message="hello")))



class FakeGetClient(FakeAsyncClient):
    async def get(self, *args, **kwargs):
        return self.response


@pytest.mark.parametrize(
    "payload, expected",
    [
        ([], []),
        ({"models": "not-a-list"}, []),
        ({"models": [None, {}, {"name": 7}, {"name": "  "}]}, []),
        ({"models": [{"name": " llama3.2 "}, {"name": "qwen2.5"}, {"name": "llama3.2"}, {"name": ""}]}, ["llama3.2", "qwen2.5"]),
    ],
)
def test_available_models_validates_provider_payload(monkeypatch, payload, expected):
    response = FakeResponse(payload)
    monkeypatch.setattr(
        "app.providers.ollama.httpx.AsyncClient",
        lambda **kwargs: FakeGetClient(response=response, **kwargs),
    )
    provider = OllamaProvider("http://localhost:11434", "test-model")

    assert asyncio.run(provider.available_models()) == expected


def test_health_returns_false_when_client_configuration_is_invalid(monkeypatch):
    def invalid_client(**kwargs):
        raise ValueError("invalid URL or timeout configuration")

    monkeypatch.setattr("app.providers.ollama.httpx.AsyncClient", invalid_client)
    provider = OllamaProvider("not a valid URL", "test-model")

    assert asyncio.run(provider.health()) is False


def test_chat_uses_default_model_when_requested_model_is_blank(monkeypatch):
    response = FakeResponse({"message": {"content": "hello"}})
    clients = []

    def make_client(**kwargs):
        client = FakeAsyncClient(response=response, **kwargs)
        clients.append(client)
        return client

    monkeypatch.setattr("app.providers.ollama.httpx.AsyncClient", make_client)
    provider = OllamaProvider("http://localhost:11434", " default-model ")

    result = asyncio.run(provider.chat(ChatRequest(message="hello", model="   ")))

    assert result.model == "default-model"
    assert clients[0].last_post_kwargs["json"]["model"] == "default-model"


def test_chat_rejects_missing_default_model(monkeypatch):
    provider = OllamaProvider("http://localhost:11434", "   ")

    with pytest.raises(ProviderError, match="No Ollama model is configured"):
        asyncio.run(provider.chat(ChatRequest(message="hello", model="  ")))

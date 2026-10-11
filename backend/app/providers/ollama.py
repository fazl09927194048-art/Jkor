import httpx

from .base import ChatProvider, ChatRequest, ChatResult, ProviderError


class OllamaProvider(ChatProvider):
    name = "ollama"

    def __init__(self, base_url: str, default_model: str, timeout: float = 45):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                response = await client.get(self.base_url + "/api/tags")
                return response.is_success
        except httpx.HTTPError:
            return False

    async def available_models(self) -> list[str]:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(self.base_url + "/api/tags")
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    return []
                models = payload.get("models", [])
                if not isinstance(models, list):
                    return []
                return [
                    item["name"]
                    for item in models
                    if isinstance(item, dict) and isinstance(item.get("name"), str) and item["name"].strip()
                ]
        except (httpx.HTTPError, ValueError, TypeError, AttributeError):
            return []

    async def chat(self, request: ChatRequest) -> ChatResult:
        model = request.model or self.default_model
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url + "/api/chat",
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": request.message}],
                        "stream": False,
                    },
                )
                response.raise_for_status()
                try:
                    payload = response.json()
                    message = payload.get("message") if isinstance(payload, dict) else None
                    answer = message.get("content") if isinstance(message, dict) else None
                except (ValueError, TypeError, AttributeError) as exc:
                    raise ProviderError("Ollama returned malformed JSON.") from exc

                if not isinstance(answer, str) or not answer.strip():
                    raise ProviderError("Ollama returned an empty or invalid response.")
                return ChatResult(provider=self.name, model=model, text=answer)
        except httpx.HTTPError as exc:
            raise ProviderError(
                "Local Ollama is unavailable. Start Ollama and pull a model, then retry."
            ) from exc

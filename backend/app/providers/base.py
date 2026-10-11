from abc import ABC, abstractmethod
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model: str | None = None


class ChatResult(BaseModel):
    provider: str
    model: str
    text: str


class ProviderError(RuntimeError):
    """Raised when a provider is unavailable or returns an invalid response."""


class ChatProvider(ABC):
    name: str

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResult:
        raise NotImplementedError

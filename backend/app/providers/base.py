from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str
    model: str | None = None
    history: list[ChatHistoryMessage] = Field(default_factory=list, max_length=20)


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

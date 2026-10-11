import base64
from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str
    model: str | None = None
    history: list[ChatHistoryMessage] = Field(default_factory=list, max_length=20)
    images: list[str] = Field(default_factory=list, max_length=2)

    @field_validator("images")
    @classmethod
    def validate_images(cls, images: list[str]) -> list[str]:
        """Accept only bounded base64-encoded PNG, JPEG, GIF, or WebP image bytes."""
        for image in images:
            if not isinstance(image, str) or not image or len(image) > 5_600_000:
                raise ValueError("Each image must be base64 data no larger than 4 MiB.")
            try:
                raw = base64.b64decode(image, validate=True)
            except (ValueError, base64.binascii.Error) as exc:
                raise ValueError("Images must be valid base64 data without a data-URL prefix.") from exc
            if not raw or len(raw) > 4 * 1024 * 1024:
                raise ValueError("Each image must be no larger than 4 MiB.")
            valid = (
                raw.startswith(b"\\x89PNG\\r\\n\\x1a\\n")
                or raw.startswith(b"\\xff\\xd8\\xff")
                or raw.startswith((b"GIF87a", b"GIF89a"))
                or (len(raw) >= 12 and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP")
            )
            if not valid:
                raise ValueError("Unsupported image format. Use PNG, JPEG, GIF, or WebP.")
        return images


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

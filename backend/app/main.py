import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .catalog import build_catalog
from .providers.base import ChatRequest, ProviderError
from .providers.ollama import OllamaProvider


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))
ollama = OllamaProvider(OLLAMA_BASE_URL, OLLAMA_DEFAULT_MODEL, REQUEST_TIMEOUT_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="NEXUS AI API", version="0.1.0", lifespan=lifespan)
origins = [item.strip() for item in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatBody(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    model: str | None = Field(default=None, max_length=200)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "nexus-ai-api"}


@app.get("/api/v1/catalog")
async def catalog():
    healthy = await ollama.health()
    models = await ollama.available_models() if healthy else []
    return build_catalog(ollama, healthy, models)


@app.post("/api/v1/chat")
async def chat(body: ChatBody):
    if not body.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be blank.")
    try:
        result = await ollama.chat(ChatRequest(message=body.message, model=body.model))
        return result.model_dump()
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

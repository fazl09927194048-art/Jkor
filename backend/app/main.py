import math
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .catalog import build_catalog
from .capabilities import build_capability_registry
from .integrations import integration_registry
from .ai_security_eval import build_eval_suite, score_supplied_outputs
from .model_eval_report import build_eval_report
from .video_planner import build_video_plan
from .providers.base import ChatHistoryMessage, ChatRequest, ProviderError
from .providers.ollama import OllamaProvider


def _positive_float_env(name: str, default: float) -> float:
    """Read a positive finite float from the environment, falling back safely."""
    try:
        value = float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return value if math.isfinite(value) and value > 0 else default


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
REQUEST_TIMEOUT_SECONDS = _positive_float_env("REQUEST_TIMEOUT_SECONDS", 45.0)
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


class ChatBody(ChatRequest):
    message: str = Field(min_length=1, max_length=20000)
    model: str | None = Field(default=None, max_length=200)


class VideoPlanBody(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    target_duration_seconds: int = Field(ge=1, le=3600)
    provider_id: str | None = Field(default=None, max_length=200)
    segment_limit_seconds: int | None = Field(default=None, ge=1, le=3600)
    stitching_allowed: bool | None = None


class SecurityEvalOutputs(BaseModel):
    outputs: dict[str, str] = Field(default_factory=dict)


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
        result = await ollama.chat(body)
        return result.model_dump()
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/v1/models")
async def models():
    connected = await ollama.health()
    available = await ollama.available_models() if connected else []
    registry = build_capability_registry(connected, available)
    return {"models": registry["models"], "notice": registry["notice"]}


@app.get("/api/v1/capabilities")
async def capabilities():
    connected = await ollama.health()
    available = await ollama.available_models() if connected else []
    return build_capability_registry(connected, available)


@app.get("/api/v1/integrations")
async def integrations():
    return integration_registry()


@app.post("/api/v1/video/plan")
async def video_plan(body: VideoPlanBody):
    try:
        return build_video_plan(
            body.prompt,
            body.target_duration_seconds,
            body.segment_limit_seconds,
            provider_id=body.provider_id,
            stitching_allowed=body.stitching_allowed,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc



@app.get("/api/v1/security/eval-suite")
async def security_eval_suite():
    return build_eval_suite()


@app.post("/api/v1/security/score")
async def security_eval_score(body: SecurityEvalOutputs):
    if len(body.outputs) > 100:
        raise HTTPException(status_code=422, detail="At most 100 supplied outputs are allowed.")
    if any(len(key) > 200 or len(value) > 20000 for key, value in body.outputs.items()):
        raise HTTPException(status_code=422, detail="Output keys or values exceed allowed length.")
    return score_supplied_outputs(body.outputs)


class SecurityEvalReportBody(BaseModel):
    model_id: str = Field(min_length=1, max_length=200)
    model_version: str | None = Field(default=None, max_length=200)
    outputs: dict[str, str] = Field(default_factory=dict)


@app.post("/api/v1/security/report")
async def security_eval_report(body: SecurityEvalReportBody):
    if len(body.outputs) > 100:
        raise HTTPException(status_code=422, detail="At most 100 supplied outputs are allowed.")
    if any(len(key) > 200 or len(value) > 20000 for key, value in body.outputs.items()):
        raise HTTPException(status_code=422, detail="Output keys or values exceed allowed length.")
    triage = score_supplied_outputs(body.outputs)
    try:
        return build_eval_report(body.model_id, triage, model_version=body.model_version)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

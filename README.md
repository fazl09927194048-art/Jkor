# NEXUS AI

A modular, capability-aware multi-model AI workspace with a free-first and local-first design.

## Product direction

NEXUS AI is being built as a hub for model discovery, chat, coding, image understanding/generation, video, audio, documents/OCR, and research. A model is only listed as available when its adapter is connected and tested. The model registry is designed to show verified limits, including per-generation video duration, before a job starts.

Long-form media may use a multi-segment workflow only when the provider permits it and the actual pipeline is implemented. Extra app permissions do not override a model's hard limits. Paid jobs require explicit consent.

## Initial stack

- Backend: Python 3.11+, FastAPI, Pydantic, HTTPX
- Frontend: React, Vite
- Local inference adapter: Ollama (optional)

## Quick start

Backend: run `pip install -r requirements.txt` inside `backend`, then `uvicorn app.main:app --reload`.

Frontend: run `npm install` inside `frontend`, then `npm run dev`.

API docs: `http://127.0.0.1:8000/docs`

Copy `backend/.env.example` to `backend/.env`. Never commit real API keys, passwords, session cookies, or tokens.

## API endpoints

- `GET /health`
- `GET /api/v1/catalog`
- `GET /api/v1/models`
- `GET /api/v1/capabilities`
- `GET /api/v1/integrations`
- `POST /api/v1/chat`

## Integration permissions

The current GitHub connector used to edit this repository is separate from a user's GitHub authorization inside the running NEXUS app. NEXUS's own GitHub OAuth flow is not implemented yet; the integrations panel reports this honestly. Follow [Integration Setup](docs/INTEGRATIONS.md) before exposing account connections.

## Project docs

- [Product vision](docs/PRODUCT_VISION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Model manifest contract](docs/MODEL_MANIFEST.md)
- [Long-form video pipeline](docs/VIDEO_PIPELINE.md)
- [Permission Center](docs/PERMISSION_CENTER.md)
- [Integration setup](docs/INTEGRATIONS.md)
- [Security baseline](docs/SECURITY.md)

## Current limitations

Only the Ollama chat adapter is currently implemented. Other modalities and hosted providers remain planned until adapters, authorization, and tests exist. This project does not bypass provider authentication, quotas, or billing. Add authentication and rate limiting before exposing the API publicly.

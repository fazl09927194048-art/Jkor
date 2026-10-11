# NEXUS AI

A modular, capability-aware multi-model AI workspace with a free-first and local-first design.

## Project status

This repository starts with the architecture and API foundation. Only providers that are actually configured and reachable will be shown as available. No paid provider is silently used as a fallback.

## Goals

- One interface for chat, coding, document analysis, vision, media tools, and web research.
- Provider adapters so local and hosted models can be added independently.
- Transparent model/provider selection and clear errors when a capability is unavailable.
- Security-first coding tools with isolated execution and explicit approval for destructive actions.
- Responsive web UI suitable for later PWA/Android packaging.

## Initial stack

- Backend: Python 3.11+, FastAPI, Pydantic, HTTPX
- Frontend: React, Vite
- Local inference adapter: Ollama (optional)

## Quick start

Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`

Frontend: `cd frontend && npm install && npm run dev`

API docs: `http://127.0.0.1:8000/docs`

Copy `backend/.env.example` to `backend/.env`. Never commit real API keys, passwords, session cookies, or tokens.

## Current limitations

Image generation, video, audio, browsing, and hosted models are not considered active until a real adapter is configured and tested. The initial scaffold does not bypass provider authentication, quotas, or billing.

See [Architecture](docs/ARCHITECTURE.md) and [Security](docs/SECURITY.md).

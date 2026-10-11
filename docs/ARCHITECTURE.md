# NEXUS AI Architecture

## Principles

1. Capability-aware routing: choose a provider only if it supports the requested task.
2. Local-first and free-first: prefer reachable local models and explicitly configured free tiers.
3. No silent paid fallback: never send user content to a paid provider without clear configuration and disclosure.
4. Honest availability: distinguish implemented, configured, reachable, and planned capabilities.
5. Provider neutrality: keep provider-specific HTTP and response parsing inside adapters.

## Components

- Web UI: React/Vite interface for chat, provider status, and later tool workspaces.
- API: FastAPI validation, health endpoints, catalog, and orchestration.
- Capability catalog: reports feature status and reachable providers.
- Provider adapters: common contract for local and hosted model APIs.
- Router (next milestone): select providers based on capability, latency, configured policy, and availability.
- Tool runners (later): document parsing, OCR, research, media tasks, and coding tools.
- Persistence (later): explicit conversation history and user settings, with retention controls.

## Initial API

- GET /health
- GET /api/v1/catalog
- POST /api/v1/chat with a message and optional model name

The first chat adapter targets Ollama at OLLAMA_BASE_URL. Other capabilities are marked planned until implemented and tested.

## Milestones

1. Scaffold, health, capability catalog, and Ollama adapter.
2. Tests for provider errors, request validation, and catalog state.
3. Provider registry and transparent capability-aware routing.
4. Optional persistence, account settings, and authentication.
5. Sandboxed coding agent with resource limits and approval gates.
6. Vision, document/OCR, audio, image generation, and media adapters.
7. PWA and Android packaging after core behavior is stable.

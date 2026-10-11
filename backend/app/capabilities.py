from typing import Any


CAPABILITY_MANIFEST: list[dict[str, Any]] = [
    {"id": "chat", "label": "Chat & reasoning", "input": ["text"], "output": ["text"]},
    {"id": "coding", "label": "Code generation & review", "input": ["text", "files"], "output": ["text", "files"]},
    {"id": "vision", "label": "Image understanding", "input": ["image", "text"], "output": ["text"]},
    {"id": "image_generation", "label": "Image generation & editing", "input": ["text", "image"], "output": ["image"]},
    {"id": "video_generation", "label": "Video generation", "input": ["text", "image", "video"], "output": ["video"]},
    {"id": "audio", "label": "Speech, audio & music", "input": ["text", "audio"], "output": ["audio", "text"]},
    {"id": "documents", "label": "Documents & OCR", "input": ["pdf", "documents", "image"], "output": ["text", "files"]},
    {"id": "research", "label": "Web research", "input": ["text", "web"], "output": ["text", "citations"]},
    {"id": "translation", "label": "Translation", "input": ["text", "documents"], "output": ["text", "documents"]},
    {"id": "transcription", "label": "Audio transcription", "input": ["audio"], "output": ["text"]},
]


def build_capability_registry(ollama_connected: bool, ollama_models: list[str]) -> dict[str, Any]:
    capabilities = []
    for item in CAPABILITY_MANIFEST:
        entry = dict(item)
        if item["id"] == "chat":
            entry["status"] = "available" if ollama_connected and ollama_models else "needs_provider"
        else:
            entry["status"] = "planned"
        capabilities.append(entry)

    models = []
    for model_name in ollama_models:
        models.append({
            "id": "ollama:" + model_name,
            "name": model_name,
            "provider": "ollama",
            "availability": "connected",
            "capabilities": ["chat"],
            "modalities": {"input": ["text"], "output": ["text"]},
            "limits": {"context_tokens": None, "max_output_tokens": None},
            "video": None,
            "pricing": {"type": "local", "cost_known": True},
            "verified": True,
        })

    return {
        "models": models,
        "capabilities": capabilities,
        "notice": "Only connected models are listed as available. Other model/provider integrations are planned until configured and tested.",
    }

from .providers.ollama import OllamaProvider


def build_catalog(ollama: OllamaProvider, ollama_healthy: bool, models: list[str]) -> dict:
    return {
        "product": "NEXUS AI",
        "policy": {"local_first": True, "silent_paid_fallback": False},
        "capabilities": [
            {"id": "chat", "label": "Chat & reasoning", "status": "available" if ollama_healthy and models else "needs_provider"},
            {"id": "coding", "label": "Coding assistant", "status": "planned"},
            {"id": "vision", "label": "Image understanding", "status": "planned"},
            {"id": "image_generation", "label": "Image generation", "status": "planned"},
            {"id": "audio", "label": "Audio & voice", "status": "planned"},
            {"id": "video", "label": "Video tools", "status": "planned"},
            {"id": "documents", "label": "Documents & OCR", "status": "planned"},
            {"id": "research", "label": "Web research", "status": "planned"},
        ],
        "providers": [
            {"id": ollama.name, "label": "Ollama (local)", "connected": ollama_healthy, "models": models}
        ],
    }

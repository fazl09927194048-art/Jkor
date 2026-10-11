import os


def integration_registry() -> dict:
    github_configured = bool(
        os.getenv("GITHUB_CLIENT_ID", "").strip()
        and os.getenv("GITHUB_CLIENT_SECRET", "").strip()
    )
    return {
        "integrations": [
            {
                "id": "github",
                "name": "GitHub",
                "status": "oauth_configured_not_connected" if github_configured else "needs_oauth_setup",
                "authorization": "official_oauth_required",
                "permission_tiers": [
                    {"id": "read", "label": "Read selected repositories", "risk": "low"},
                    {"id": "write", "label": "Create branches and edit files", "risk": "medium"},
                    {"id": "pull_requests", "label": "Open pull requests", "risk": "medium"},
                    {"id": "workflows", "label": "Run CI/workflows", "risk": "high", "requires_confirmation": True},
                    {"id": "admin", "label": "Repository settings, secrets, releases, deletion", "risk": "critical", "requires_confirmation": True},
                ],
                "note": "This reports configuration readiness only. A secure OAuth callback, user session, encrypted token storage, and scope verification are required before an account is connected.",
            }
        ]
    }

# Integration Setup

## GitHub

The current project repository is editable through the developer's connected GitHub integration, but that does not automatically grant the running NEXUS AI app access to the user's GitHub account.

To connect a user's GitHub account inside NEXUS AI, implement a separate official GitHub App or OAuth flow:
1. Register the application with GitHub and configure an exact callback URL.
2. Store GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in the backend secret manager, never in frontend code or a committed .env file.
3. Add authenticated user sessions, OAuth state validation, and PKCE where supported.
4. Exchange the authorization code on the backend, validate granted scopes and selected repositories, and encrypt tokens at rest.
5. Expose only actions covered by the grant; verify authorization server-side on every request.
6. Add disconnect/revoke, token rotation, audit logs, and high-risk action confirmations.

Environment variable presence is not proof that a user is connected. NEXUS must report “not connected” until a real OAuth flow has completed and the token has been validated.

## Permission design

Ask for only the minimum scopes required. Prefer selected-repository access. Repository write permission must not imply permission to merge, delete, modify secrets, or run arbitrary workflows. Request those separately when supported and require explicit confirmation for high-impact operations.

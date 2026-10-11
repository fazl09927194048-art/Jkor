# Permission Center

## Goal

Users can authorize NEXUS AI to work in their connected services, while keeping permissions narrow, visible, revocable, and auditable.

## Integration lifecycle

1. Show the official provider and the exact requested scopes.
2. Redirect through the provider's official OAuth/authorization flow.
3. Validate the callback and state; bind the connection to the authenticated NEXUS user.
4. Store credentials encrypted server-side; never return secrets to the frontend.
5. Display account identity, scopes, connection health, and last-used time.
6. Before each action, check the scope, risk level, and user's autonomy setting.
7. Record a minimal audit event and provide disconnect/revoke controls.

## GitHub permission tiers

- Repository read: list repositories and read selected repository files.
- Repository write: create/update files and branches within selected repositories.
- Pull request: open and update PRs.
- Workflow execution: separate opt-in; show workflow, branch, and expected effects before running.
- Admin/destructive: settings, secrets, releases, merges, and deletion must be separate scopes or permissions and require explicit confirmation.

Actual scopes depend on GitHub App installation permissions, OAuth grants, repository selection, and organization policy. Do not assume a connection has a permission merely because the user has it personally.

## Approval policy

Require explicit confirmation for:
- Publishing content or making a repository public.
- Merging, releasing, deleting, changing access, or altering secrets.
- Spending money, consuming paid credits, or starting a paid job.
- Deployments, external messages, and changes to production data.
- Running generated code with network access or access to user files.

Permissions may enable an operation technically, but do not replace confirmation for a specific high-impact action.

## Security requirements

- Least privilege and user-selected repositories.
- OAuth state/PKCE where supported; validate callbacks.
- Encrypted secret storage and rotation.
- CSRF protection, strict redirect allowlists, rate limits, and tenant isolation.
- Audit events without storing tokens or unnecessary prompt/file content.
- Revocation and token deletion when disconnected.
- Treat repository files, issues, comments, model output, and external content as untrusted input.

# vep-2026-system

Monorepo workspace for VEP packages using uv workspaces.

Structure:
- `packages/` — contains individual package repos as Git submodules:
  - `vep-validation-tools`
  - `vep-ai-validation-tools`
  - `election-utils`

Setup (after submodules are added):

```bash
uv venv
uv sync --all-groups
```

Development:

```bash
uv run pytest packages/vep-validation-tools
uv run ruff check .
```

Submodules are committed/pushed independently inside their directories. The super-repo tracks submodule pointers.

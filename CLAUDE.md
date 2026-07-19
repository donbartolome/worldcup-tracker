# World Cup 2026 Tracker — Learning Project

## Purpose
Personal learning project. Nobody else uses this app. The goal is for me to
get comfortable with Claude Code workflows and build baseline Python/FastAPI
comfort — NOT to produce production-grade software.

## How to work with me
- I have solid Python experience (Databricks/data work) but have never
  built an app from scratch. Explain new concepts (FastAPI decorators,
  async, dependency injection, etc.) briefly when you introduce them.
- I'm still building Claude Code fluency. If you use a feature I haven't
  seen yet (subagents, hooks, skills, plan mode nuances), say what it is
  in one sentence before using it.
- Prefer simple, readable code over clever or "production-ready" patterns.
  No auth, logging frameworks, or config management unless I ask.
- Ask before adding new dependencies.
- When a request touches the devcontainer setup, check for ripple effects
  across compose.yaml, Dockerfile, and devcontainer.json rather than only
  solving the narrowest literal ask — these three tend to need to move
  together (see Devcontainer conventions below).

## Project structure
- FastAPI app, single-file for now (`main.py`)
- Devcontainer config lives in `.devcontainer/` (`devcontainer.json`,
  `compose.yaml`, `Dockerfile`, `devcontainer-lock.json`) — Compose-based,
  `app` + `db` (Postgres 16) services
- Postgres is provisioned but UNUSED so far — don't add DB code until I
  explicitly start a phase that calls for it
- Run locally with: `fastapi dev` (wraps uvicorn + auto-reload)

## Devcontainer conventions
- Any new named volume mounted onto a path that doesn't already exist in
  the base image needs its target directory created and chowned to
  `vscode` in `.devcontainer/Dockerfile` — otherwise Docker initializes it
  root-owned and vscode-run processes can't write to it (bit us with
  ~/.claude and ~/.config/gh).
- When adding a tool that needs persistent config/credentials, update
  together: (1) devcontainer feature or `.devcontainer/Dockerfile` install,
  (2) `.devcontainer/compose.yaml` volume mount, (3) the mkdir+chown above.
  Treat these as one change, not three separate asks.
- Reproducibility matters here: pin image/service versions explicitly
  (no `latest` tags), keep `.devcontainer/devcontainer-lock.json` committed,
  and disable auto-updaters for tools running inside the container (e.g.
  DISABLE_AUTOUPDATER) rather than letting them silently drift from what's
  declared in config.

## Git conventions
- Commit messages follow Conventional Commits: `type(scope): description`
- Common types: feat, fix, chore, docs, refactor
- Imperative mood, lowercase, no trailing period
- Branch names match the commit type prefix, e.g. chore/devcontainer-setup
- Committing locally is fine without asking; ask before pushing

## Keep this file current
- Whenever we hit a gotcha, make a non-obvious decision, or establish a
  convention worth remembering, proactively suggest a specific addition
  to this file before the session ends — don't wait to be asked.
- Phrase it as a concrete proposed edit ("add this line to CLAUDE.md: ..."),
  not just "you might want to update your docs."
- If we explicitly decide something contradicts what's already written
  here, flag the conflict and propose the correction, rather than silently
  going along with the newer instruction.

## Current phase
Phase 0: environment setup + hello-world endpoint. Devcontainer, tooling,
and git conventions are settled; the actual first Claude Code session
against the app code is still pending.

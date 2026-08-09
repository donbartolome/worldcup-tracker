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
- FastAPI app in `main.py`; SQLAlchemy engine/session/ORM model layer in
  `db.py`, wired into `main.py`'s `GET /fixtures`, `GET /fixtures/{id}`,
  and `GET /results` endpoints via `get_db()`
- `Base.metadata.create_all()` only creates *missing* tables — it never
  adds columns to an existing one. Schema changes now go through Alembic
  (`alembic/`, config in `alembic.ini`); `env.py` reuses `db.py`'s engine
  rather than reading `DATABASE_URL` a second time. Run `alembic` from the
  repo root — `prepend_sys_path = .` in `alembic.ini` is CWD-relative, and
  that's what lets `env.py` `import db`. After pulling a migration, run
  `alembic upgrade head`. `create_all` and Alembic are now two separate
  schema sources: on a wiped `db-data` volume, build from migrations
  (`alembic upgrade head`), not `python db.py` — the latter would create
  the current-model schema without an `alembic_version` row, and the next
  `alembic upgrade head` would then fail trying to add a column that
  already exists.
- `Match.round` is a real column (`R32`, `R16`, `QF`, `SF`, `3P` for the
  3rd-place playoff, `F`) — plain `String`, not a DB enum. Tradeoff: no
  DB-level validation, but adding a stage value later is just data, no
  migration required. `seed.py`'s round comments are kept as
  human-readable cross-checks for date-window/exact-approx provenance,
  not as the source of truth anymore.
- Devcontainer config lives in `.devcontainer/` (`devcontainer.json`,
  `compose.yaml`, `Dockerfile`, `devcontainer-lock.json`) — Compose-based,
  `app` + `db` (Postgres 18) services
- Postgres is in active use: `db.py` (engine/session/ORM), `tests/test_db.py`,
  and `seed.py` (32 seeded knockout matches) all exist. `GET /fixtures`,
  `GET /fixtures/{id}`, and `GET /results` in `main.py` are wired to real
  queries via `get_db()`.
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
- Container Tools VS Code extension was removed — not needed for this
  project's workflow (no real use for its container-management UI beyond
  what the devcontainer CLI/Docker Compose already covers).

## Git conventions
- Commit messages follow Conventional Commits: `type(scope): description`
- Common types: feat, fix, chore, docs, refactor
- Imperative mood, lowercase, no trailing period
- Branch names match the commit type prefix, e.g. chore/devcontainer-setup
- Committing locally is fine without asking; ask before pushing
- Use plain `git` for local repo operations: status, diff, add, commit,
  branch, checkout, log, merge, and pushing/pulling to/from the existing
  remote.
- Use `gh` (GitHub CLI, available via the devcontainer feature) for
  anything that talks to the GitHub API beyond a bare push/pull: creating
  or viewing PRs, checking PR/CI status, commenting on issues or PRs, and
  viewing workflow runs. Prefer `gh` over opening github.com in a browser
  for these.

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
Phase 2 warm-up is done: `GET /fixtures`/`GET /fixtures/{id}`/`GET /results`
are wired to real Postgres queries, Alembic is adopted, and `Match.round`
is a real column via Alembic's first real migration. Next up: Phase 3,
Claude Code power features (subagents, custom slash commands, MCP servers).

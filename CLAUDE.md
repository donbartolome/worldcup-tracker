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

## Project structure
- FastAPI app, single-file for now (`main.py`)
- Devcontainer: Compose-based, `app` + `db` (Postgres 16) services
- Postgres is provisioned but UNUSED so far — don't add DB code until I
  explicitly start a phase that calls for it
- Run locally with: `fastapi dev`

## Git conventions
- Commit messages follow Conventional Commits: `type(scope): description`
- Common types: feat, fix, chore, docs, refactor
- Imperative mood, lowercase, no trailing period
- Branch names match the commit type prefix, e.g. chore/devcontainer-setup
- Ask before pushing, but committing locally is fine without asking

## Current phase
Phase 0: environment setup + hello-world endpoint only.

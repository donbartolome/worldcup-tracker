#!/bin/bash
# .claude/hooks/check-tests-before-commit.sh
#
# PreToolUse hook, wired in .claude/settings.json with
# if: "Bash(git commit *)" so it only spawns on actual commit attempts.
# Runs the test suite and blocks the commit unless it explicitly passes.
#
# Fail-closed: only "pytest exited 0" ever allows a commit through. Failing
# tests, a broken pytest invocation, wrong cwd, missing binary, or a bug in
# this script itself all block. See CLAUDE.md's Hooks section for the
# rationale and the ALLOW_FAILING_TESTS=1 bypass this implements.
#
# Deliberately not `set -e` - a failing pytest is an expected outcome this
# script has to handle, not something that should abort it.
set -uo pipefail

# CLAUDE_PROJECT_DIR is passed by the harness; fall back to resolving the
# repo root relative to this script's own location (two levels up from
# .claude/hooks/) so the script also works if invoked standalone.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

if ! cd "$PROJECT_DIR"; then
  echo "check-tests-before-commit: couldn't cd to project dir ($PROJECT_DIR) - blocking commit (fail closed)." >&2
  exit 2
fi

# pytest is cwd-sensitive here (root conftest.py, alembic.ini's
# prepend_sys_path = .), which is why we cd before running it rather than
# passing a --rootdir.

INPUT="$(cat)"
COMMAND="$(jq -r '.tool_input.command // empty' <<<"$INPUT" 2>/dev/null)"
if [ -z "$COMMAND" ]; then
  echo "check-tests-before-commit: couldn't read tool_input.command from hook stdin - blocking commit (fail closed)." >&2
  exit 2
fi

if ! command -v pytest >/dev/null 2>&1 && ! python3 -m pytest --version >/dev/null 2>&1; then
  echo "check-tests-before-commit: pytest isn't runnable in this environment - blocking commit (fail closed, not bypassable)." >&2
  exit 2
fi

OUTPUT="$(python3 -m pytest -q 2>&1)"
STATUS=$?
FAILURES="$(printf '%s\n' "$OUTPUT" | grep -E '^(FAILED|ERROR)' || true)"

# Bypass token must sit immediately before the git commit invocation itself
# (not just appear anywhere in the command line, e.g. inside a commit
# message or an unrelated echo) - but it can follow other && chained
# subcommands, e.g. `git add -A && ALLOW_FAILING_TESTS=1 git commit -m ...`.
BYPASS_RE='(^|&&)[[:space:]]*ALLOW_FAILING_TESTS=1[[:space:]]+git[[:space:]]+commit'

if [ "$STATUS" -eq 0 ]; then
  # All tests passed - commit proceeds silently.
  exit 0

elif [ "$STATUS" -eq 1 ]; then
  # Genuine test failures (not a broken pytest run) - this is the only
  # case the bypass is allowed to cover.
  if [[ "$COMMAND" =~ $BYPASS_RE ]]; then
    jq -n \
      --arg msg "Committed with FAILING tests (ALLOW_FAILING_TESTS=1 bypass used):
${FAILURES}" \
      --arg ctx "This commit was made with failing tests, via the ALLOW_FAILING_TESTS=1 bypass (deliberate TDD red checkpoint). Failing: ${FAILURES}" \
      '{
        systemMessage: $msg,
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "allow",
          additionalContext: $ctx
        }
      }'
    exit 0
  fi

  {
    echo "check-tests-before-commit: tests are failing, commit blocked."
    echo ""
    echo "$FAILURES"
    echo ""
    echo "Fix the failing tests, or if this is a deliberate TDD red checkpoint,"
    echo "prefix the commit command with ALLOW_FAILING_TESTS=1 (not a general"
    echo "escape hatch - see CLAUDE.md's Hooks section)."
  } >&2
  exit 2

else
  # pytest ran but didn't cleanly pass/fail (interrupted, internal error,
  # usage error, no tests collected) or couldn't run at all. Always
  # blocking, no bypass - this isn't "tests are red", it's "we don't know
  # if tests are red", and the bypass is scoped to the former only.
  {
    echo "check-tests-before-commit: pytest did not run cleanly (exit $STATUS) - commit blocked."
    echo "This is not bypassable with ALLOW_FAILING_TESTS=1; fix the environment first."
    echo ""
    echo "$OUTPUT"
  } >&2
  exit 2
fi

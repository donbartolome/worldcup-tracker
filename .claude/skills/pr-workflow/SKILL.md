---
name: pr-workflow
description: 'Use when shipping a change in this repo end-to-end — branch, commit, push, open a PR — and/or when an open PR has automated reviewer comments (e.g. GitHub Copilot) that need triaging, replying to, resolving, and merging.'
---

# PR Workflow

Covers this repo's full loop: branch → commit → push → PR → handle automated
review comments → resolve → squash-merge. Git conventions (commit style,
branch naming, when to use plain `git` vs `gh`) are defined in `CLAUDE.md` —
this skill assumes those and adds the parts CLAUDE.md doesn't cover: PR body
shape and reviewer-comment triage.

## 1. Branch, commit, push, open PR

- Branch name matches the commit type prefix (`feat/...`, `fix/...`, etc. —
  see CLAUDE.md).
- Commit message: Conventional Commits, imperative mood, ends with
  `Co-Authored-By: Claude <noreply@anthropic.com>` (no specific model name —
  which model made the change can vary between sessions, and a hardcoded
  name in the trailer would drift out of sync).
- Push with `-u`, then `gh pr create` with a body split into `## Summary`
  (bullets on what/why) and `## Test plan` (checklist of what was actually
  verified — not aspirational, only what you ran).
- Pushing and opening the PR are fine without asking (per CLAUDE.md); ask
  before force-pushing to an existing PR branch.

## 2. Triage automated review comments

Fetch both the review summary and inline comments — the summary alone
often omits "suppressed" comments that are still worth reading:

```bash
gh pr view <N> --json reviews -q '.reviews[] | {author: .author.login, body}'
gh api repos/<owner>/<repo>/pulls/<N>/comments --jq '.[] | {path, line, body}'
```

For each comment, evaluate it on its technical merits — do not defer to the
bot by default and do not dismiss it by default. Check whether the scenario
it describes is actually reachable in the current code (e.g. "no write
endpoints exist yet, so this data shape can't occur today"), and weigh it
against CLAUDE.md's stated bar for this project (learning project, prefer
simple/readable over defensive/production-hardened, don't design for
hypothetical future requirements). A comment can be technically correct
about the code and still not worth acting on right now.

Decide per comment:
- **Valid and worth fixing now** → make the change as a new commit on the
  PR branch (don't amend/force-push — that would rewrite history the
  reviewer already commented against and orphan the thread's context).
  Rerun the relevant tests (or the full suite, if the change touches
  shared code) before replying — "fixed" on a thread means verified, not
  just edited. Then reply on the thread summarizing what changed.
- **Valid concern, not worth fixing now** → reply explaining why (what
  makes it unreachable/out of scope today) and what would make it worth
  revisiting later. Don't silently ignore it.
- **Wrong** → reply with the specific reason it doesn't apply here.

For anything beyond "leave as-is" vs. "fix it," check with the user first —
don't unilaterally overrule a reviewer comment on a design decision the user
made explicitly in the task (see CLAUDE.md's "flag the conflict, propose
the correction" convention for contradicting established decisions).

## 3. Reply and resolve

Reply inline (threads it under the original comment):

```bash
gh api repos/<owner>/<repo>/pulls/<N>/comments/<comment_id>/replies -f body="..."
```

Resolving a conversation is GraphQL-only (no REST endpoint). Get the
thread id, then resolve:

```bash
gh api graphql -f query='
query {
  repository(owner: "<owner>", name: "<repo>") {
    pullRequest(number: <N>) {
      reviewThreads(first: 20) {
        nodes { id isResolved comments(first: 1) { nodes { path line body } } }
      }
    }
  }
}'

gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "<thread_id>"}) {
    thread { isResolved }
  }
}'
```

Only resolve a thread once it's actually been addressed (fixed and
verified, or replied to with a reason) — don't resolve just to clear the
UI.

## 4. Merge

Before merging: confirm mergeability and check for CI status, since a
report of "all comments addressed" isn't the same as "safe to merge":

```bash
gh pr view <N> --json state,mergeable,mergeStateStatus,statusCheckRollup
```

Merging is a shared-state action — confirm with the user before merging,
even if they authorized the branch/PR steps earlier. A green light on "open
a PR" is not a standing green light on "merge it."

```bash
gh pr merge <N> --squash --delete-branch
```

Then sync local state — `gh pr merge --delete-branch` deletes the *local*
branch too if you were on it, and switches you to the base branch:

```bash
git checkout main && git pull --ff-only
git fetch --prune origin   # clears the now-stale remote-tracking ref
```

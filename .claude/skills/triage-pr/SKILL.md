---
name: triage-pr
description: Triage automated review comments on a PR — fetch and evaluate, report
  verdicts and draft replies (does not post, resolve, or merge)
argument-hint: <pr-number>
disable-model-invocation: true
context: fork
agent: pr-triager
background: false
---

Triage the automated review comments on PR #$ARGUMENTS in this repo.

Fetch both the review summary and inline comments — the summary alone often
omits "suppressed" comments that are still worth reading:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
gh pr view $ARGUMENTS --json reviews -q '.reviews[] | {author: .author.login, body}'
gh api repos/<owner>/<repo>/pulls/$ARGUMENTS/comments --jq '.[] | {id, path, line, body}'
```

Evaluate each comment on its technical merits per the `pr-workflow` skill's
section 2 criteria (already preloaded into your context).

Report back:

- A table: `path:line` | reviewer | verdict (`fix now` / `valid, not now` /
  `wrong`) | one-line rationale.
- Per comment: the REST `comment_id`, and the GraphQL thread id if you fetch it.
- A drafted reply body per thread, ready to post verbatim.
- Anything contesting a deliberate design choice flagged `NEEDS USER DECISION`.

You are read-only: do not reply, resolve, edit files, or merge. The main
session applies your findings via `pr-workflow` sections 2–3.

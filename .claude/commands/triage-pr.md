---
description: Triage automated review comments on a PR — fetch, evaluate, reply, resolve (does not merge)
argument-hint: <pr-number>
---

Triage the automated review comments on PR #$ARGUMENTS in this repo.

Follow the `pr-workflow` skill (`.claude/skills/pr-workflow/SKILL.md`),
specifically **section 2 "Triage automated review comments"** through
**section 3 "Reply and resolve"**, applied to PR #$ARGUMENTS:

1. Fetch the review summary and inline comments.
2. Evaluate each comment on its technical merits per the skill's criteria.
3. For anything beyond "leave as-is" vs. "fix it," check with the user
   before acting — per the skill's guidance on overruling reviewer
   comments on established design decisions.
4. Reply to each thread and resolve only once actually addressed.

Stop after section 3. Do **not** proceed to section 4 (Merge) — merging
is a separate, explicit step the user triggers on their own.

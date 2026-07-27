# Claude Code Prompts for the Kanban Board

The board lives in `dkaruri/kanban` (file `KANBAN.md`); project code lives in
each project's own repo. These prompts assume you're running Claude Code inside
`chicago-building-permits-search` with the `CLAUDE.md` snippet from the board's
README in place.

## One-time setup

> Clone https://github.com/dkaruri/kanban next to this repo (or pull it if
> present). Then correct the backfilled Kanban dates: for every task in its
> KANBAN.md whose Log says "backfilled", use this project repo's git log to
> find the real first and last commit dates for that feature, update
> Created/Updated, note the correction in each task's Log, and push the
> kanban repo.

## Daily driving

**Work the fixes queue (your main use case):**
> Pull dkaruri/kanban and read KANBAN.md, following its CLAUDE CODE PROTOCOL.
> Implement the Fixes list in this repo: todo tasks only, P0 first then P1,
> P2, P3. For each task, set it in-progress, check off checklist items as you
> complete them, log your work with timestamps, and mark it done only after
> verifying. Push the board updates to dkaruri/kanban as you go.

**Work one specific task:**
> Pull dkaruri/kanban, read KANBAN.md, and implement FIX-001 in this repo per
> its checklist, following the board protocol for status, timestamps, and
> logging. Push the board update.

**Work the features queue:**
> Pull dkaruri/kanban and implement the Features list tasks that are status
> todo, in priority order, in this repo. Skip blocked tasks and tell me why
> they're blocked. Keep the board updated and pushed.

**Timebox it:**
> Pull dkaruri/kanban and work through as many todo Fixes as you can in this
> repo. Stop after the highest-priority two tasks are done and verified;
> leave the board accurately updated and pushed either way.

## Board management (no coding)

> Pull dkaruri/kanban. What's on the board? Summarize by list: what's in
> progress, what's blocked and why, and what's next by priority.

> Add to the Fixes list in dkaruri/kanban's KANBAN.md: [describe the bug].
> Priority P1. Follow the board's task template and ID sequence, then push.

> In dkaruri/kanban, mark FEAT-017 done — I verified it manually. Update the
> checklist, timestamps, and log, then push.

> In dkaruri/kanban, archive all done tasks older than 30 days per the board
> protocol, then push.

## In Claude chat (GitHub connector)

The same asks work in a regular Claude conversation — Claude reads and
commits to both repos directly. The board's clickable checklists also
generate ready-made save prompts to paste here.

## Guardrails built into the board

- The protocol block in KANBAN.md tells Claude to never start `blocked`
  tasks, never touch the **Futures** list, never delete tasks, and always
  stamp real Chicago time on changes.
- "Implement the fixes" with no other context defaults to: Fixes list →
  status todo → P0→P3 → oldest first. That's the deterministic queue order.
- Tasks are implemented in the project repo named by their Tags; the board
  file itself only ever changes in dkaruri/kanban.

## Optional: UI/UX Pro Max pass (community skill)

If you install the ui-ux-pro-max skill in Claude Code, run it against the
kanban repo:

> Use the ui-ux-pro-max skill to audit and improve board.html in
> dkaruri/kanban. Keep the purple + black dark theme and the existing
> markdown parser and data contract (it must still parse KANBAN.md
> unchanged), preserve WCAG AA contrast (all current text/badge pairs are
> ≥4.5:1), and focus on mobile touch ergonomics, desktop layout polish, and
> cross-browser compatibility.

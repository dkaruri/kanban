# Kanban Board — Divyam's project board

A file-based Kanban board that both humans and **Claude / Claude Code** can read and update. It lives in its own repo (`dkaruri/kanban`) and tracks work across projects — currently the [Chicago Permit Search tool](https://github.com/dkaruri/chicago-building-permits-search).

- **`KANBAN.md`** — the board itself. Single source of truth. Human-readable on GitHub (mobile + desktop) and machine-readable by Claude Code.
- **`board.html`** — the visual board: columns, priority colors, collapsible lists, clickable checklists, task modals with shareable links, add-task form.
- **`CLAUDE_CODE_PROMPTS.md`** — copy-paste prompts for driving Claude Code from the board.
- **`README.md`** — this file.

## 1. Live board

Once GitHub Pages is enabled (repo **Settings → Pages → Deploy from a branch → `main` / `/ (root)`**), the board is live at:

**https://dkaruri.github.io/kanban/board.html**

The raw board at `KANBAN.md` also renders on github.com and in the GitHub mobile app.

## 2. How it connects to project repos

The board and the code are separate on purpose: the board spans projects (Fixes and Features currently target Chicago Permit Search; Futures is cross-project). Each task's **Tags** field says which project it belongs to.

**Claude (chat, with the GitHub connector):** has access to both repos — ask it to implement, update, or summarize and it reads/commits wherever needed.

**Claude Code (in the project repo):** add this to the `CLAUDE.md` at the root of `chicago-building-permits-search`:

```markdown
## Kanban board

Tasks are tracked on a separate board: KANBAN.md in the dkaruri/kanban repo
(live view: https://dkaruri.github.io/kanban/board.html). To work from the
board: clone or pull dkaruri/kanban, read KANBAN.md and follow its CLAUDE
CODE PROTOCOL, implement tasks in THIS repo, then update the task's status,
checklist, timestamps, and log in the board file and push dkaruri/kanban.
```

## 3. Using the visual board

- **Collapse/expand lists:** tap a list header.
- **Open a task:** tap any card — full checklist, dates, tags, and activity log. Every task has a shareable URL (`board.html#FIX-001`).
- **Checklists are clickable:** tap items in an open task to toggle them. Because GitHub Pages is a static host, the click is staged in your view rather than written to GitHub directly — a save bar appears with **Copy save prompt for Claude** (paste it to Claude, which commits the change via the GitHub connector) or use the GitHub edit button. Revert undoes staged changes.
- **Add a task:** the **＋ Add task** button generates a protocol-perfect card (next free ID, real Chicago timestamps); save it via the Claude prompt or the GitHub editor.
- **Sort & filter:** status filters, search, and sorting (active-first, by priority, recently updated).

## 4. Sharing

The repo is public, so anyone with the link can view the live board — no invite needed. To let coworkers edit: repo **Settings → Collaborators → Add people**. Only collaborators can commit changes.

## 5. The format at a glance

Three lists (plus an Archive), each with a purpose description:

| List | Purpose | ID prefix |
|------|---------|-----------|
| 🔧 Fixes | Bugs/repairs on current projects — Claude Code's default queue | `FIX-###` |
| ✨ Features | New features for existing projects | `FEAT-###` |
| 🔭 Futures | Ideas beyond current projects — never auto-implemented | `FUT-###` |

Each task card records: **Priority** (`P0-Critical` / `P1-High` / `P2-Medium` / `P3-Low`), **Status** (`todo` / `in-progress` / `blocked` / `done`), **Created** and **Updated** timestamps (Chicago time), optional **Due**, **Assignee**, and **Tags** (project), a description, a **Checklist**, and an activity **Log**.

The full editing rules live in the comment block at the top of `KANBAN.md`.

# Divyam's Kanban Board

<!-- kanban-board: v1 | timezone: America/Chicago | ids: FIX|FEAT|FUT -->

<!--
═══════════════════════════════════════════════════════════════════
CLAUDE CODE PROTOCOL — READ THIS BEFORE TOUCHING THE BOARD
═══════════════════════════════════════════════════════════════════

This file is the single source of truth for project tasks. It is both
human-readable (renders on GitHub, mobile and desktop) and machine-readable.
Follow these rules exactly so the format stays parseable.

WHERE THINGS LIVE
  • This board lives in its own repo: dkaruri/kanban (file: KANBAN.md).
  • The code it tracks lives in each project's own repo — currently
    dkaruri/chicago-building-permits-search (see each task's Tags).
  • Implement tasks in the PROJECT repo. Record every board update
    (status, checklist, timestamps, log) HERE, and push this repo too.

STRUCTURE
  • Lists are `## ` headings. The blockquote (`> `) directly under a list
    heading is that list's purpose — do not remove it.
  • Tasks are `### <ID> · <Title>` headings. IDs are FIX-###, FEAT-###,
    or FUT-### (zero-padded, unique, never reused — even after deletion).
  • Task metadata is a bullet block of `- **Key:** value` lines.
  • An optional free-text description follows the metadata.
  • `**Checklist:**` introduces `- [ ]` / `- [x]` subtask items.
  • `**Log:**` introduces dated activity entries.

METADATA FIELDS (keep this order)
  - **Priority:** P0-Critical | P1-High | P2-Medium | P3-Low
  - **Status:** todo | in-progress | blocked | done
  - **Created:** YYYY-MM-DD HH:MM CT
  - **Updated:** YYYY-MM-DD HH:MM CT
  - **Due:** YYYY-MM-DD            (optional)
  - **Assignee:** name             (optional)
  - **Tags:** comma, separated     (optional; project/topic labels)

SELECTING WORK ("Read from my Kanban and implement the fixes")
  1. Default scope is the **Fixes** list unless the user names another list
     or a specific task ID.
  2. Filter to Status: todo (never start blocked tasks; ask about them).
  3. Sort by Priority: P0 first, then P1, P2, P3. Break ties by oldest
     Created date.
  4. NEVER implement anything from **Futures** — that list is an idea
     parking lot, out of scope for current projects, and is only edited
     when the user explicitly asks.

WHILE WORKING ON A TASK
  1. Set Status to in-progress and refresh Updated
     (use: TZ=America/Chicago date '+%Y-%m-%d %H:%M CT').
  2. Check off checklist items (`- [ ]` → `- [x]`) as you complete them.
     You may append newly discovered subtasks to the checklist.
  3. Append one line to the task's Log for every status change or
     significant event: `- YYYY-MM-DD HH:MM CT — <what happened> (Claude Code)`.
  4. When every checklist item is checked and the work is verified, set
     Status to done and refresh Updated. If you cannot finish, set Status
     to blocked and log why.

ADDING TASKS
  Copy the template at the bottom of this file. Assign the next unused ID
  for that list. Always fill Created and Updated with the real current
  Chicago time — never guess or backdate.

NEVER
  • Reorder or rename lists, or edit their purpose blockquotes.
  • Delete tasks (mark done, or move the heading + body to the Archive
    section at the bottom).
  • Change the metadata key names, priority values, or status values.
═══════════════════════════════════════════════════════════════════
-->

**Board owner:** Divyam · **Board repo:** [dkaruri/kanban](https://github.com/dkaruri/kanban) · **Tracking:** [dkaruri/chicago-building-permits-search](https://github.com/dkaruri/chicago-building-permits-search) · **Timezone:** America/Chicago (CT) · **Format:** v1

> ℹ️ Tasks whose Log says *backfilled* were completed before this board existed; their Created/Updated dates are the backfill date, not the true completion date. Ask Claude Code to *"correct the backfilled Kanban dates from git history"* to replace them with real first/last commit dates for each feature.

**Priority legend:** `P0-Critical` drop everything · `P1-High` next up · `P2-Medium` normal queue · `P3-Low` when time allows

**Status legend:** `todo` → `in-progress` → `done`, with `blocked` for anything stuck (note the blocker in the Log).

---

## 🔧 Fixes

> **Purpose:** Things to fix on current projects — currently the Chicago Permit Search tool. Bugs, regressions, broken behavior, and cleanup on what already exists. This is Claude Code's default work queue.

### FIX-042 · A hand-typed "+ Add address" stop cannot be removed, and Clear list leaves it behind

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-08-07 09:58 CT
- **Updated:** 2026-08-07 10:09 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: in My Permit List, the remove control does nothing on an address added by hand, and "Clear list" leaves it in place. Permits added through the map or the directory are unaffected.

**Checklist:**
- [x] Reproduce the failure on a hand-typed stop before changing anything
- [x] Make the row's remove control work on a hand-typed stop, with the same undo a permit removal gets
- [x] Make Clear list empty hand-typed stops too, including a list that holds only them
- [x] Confirm permits added via map search / the directory are not affected
- [x] Stop the removal path failing silently
- [x] Cover with a headless suite at desktop and iPhone 13, with a mutation control

**Log:**
- 2026-08-07 09:58 CT — created from Divyam's report; reproduced immediately — 5 red checks on a hand-typed stop (Claude Code)
- 2026-08-07 09:58 CT — done; `0501dfc` on `fix-042-custom-stop-remove`, **pushed, NOT merged**. `docs/list.html` only — custom stops exist on no other page. **Root cause:** custom stops live in `list.custom`, not `state.userPermitNumbers`, and `customToRow` deliberately sets `permit_number: ""` (never fabricate a permit number). The saved-list row template keyed every control off `row.permit_number`, so on a hand-typed stop the X called `removePermitFromUserList("")` — a no-op — while **`removeCustomStop()` sat with ZERO call sites, dead since the feature shipped**; `clearUserList()` only ever emptied `userPermitNumbers`, so custom stops survived every clear, and a list of nothing but added addresses answered "The permit list is already empty." and refused to clear at all. One rule — how a row is identified — was applied in one place and not the other; `tickKeyFor(row)` already encodes it for the visited/called ticks, so the X now passes `tickKeyFor(row)` into a single `removeStopFromUserList()` dispatch and `removeCustomStop` runs the same commit tail and the same FIX-003 undo (removing a stop must invalidate the route too). The restored stop keeps its `pos` and `mergeCustomStops` sorts by pos, so undo brings back its stop number for free. **Third symptom found while tracing:** the ↑/↓ arrows were silently dead on a hand-typed stop for the same reason — real reordering is a feature, not a bug fix, so the arrows now carry the existing aria-disabled + spoken-reason treatment instead of pretending to work → **FIX-043**. `removePermitFromUserList` also no longer returns silently on an unknown key; that silence is what hid this. **Not affected:** the map search box only filters/highlights existing permits, so anything reached that way carries a real permit number — asserted by explicit controls. Verified `verify-tmp/t66-custom-stop-remove.js` desktop + iPhone 13, 38 checks green, **red first (5 failures)**; five mutants all caught. t65, t46, t47, t57, t59, t64 still green; control-byte scan clean (Claude Code)
- 2026-08-07 10:09 CT — **MERGED to main** (`0bce3df`, `--no-ff`) on Divyam's approval, pushed, and **confirmed LIVE** on Pages. Merged tree re-verified before pushing (t66 + t65 green, control bytes clean), then verified at the destination rather than at the build: live `list.html` serves `removeStopFromUserList` (×2), the `list.custom = []` clear, the custom-aware emptiness guard, and the blocked-arrow reason. Client-only, no Worker deploy (Claude Code)

### FIX-043 · Let a hand-typed stop be reordered with the up/down arrows

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-08-07 09:58 CT
- **Updated:** 2026-08-07 09:58 CT
- **Tags:** Chicago Permit Search Tool

Split out of FIX-042. A hand-typed "+ Add address" stop holds its place through its own `pos` in `list.custom`, which `moveSavedPermitByOffset` — an index into `state.userPermitNumbers` — cannot reach, so its arrows did nothing at all. FIX-042 made them say so (aria-disabled plus a spoken reason, the same treatment the follow-up-filter case gets) rather than pretend to work. Actually moving one means reconciling `pos` against the merged permit order in `mergeCustomStops`, which is a feature, not a bug fix.

**Checklist:**
- [ ] Decide how a custom stop's `pos` should behave when the permits around it move
- [ ] Make the up/down arrows move a hand-typed stop within the merged order
- [ ] Keep drag-and-drop reorder consistent with the arrows
- [ ] Remove the aria-disabled fallback and its message once the arrows really work
- [ ] Cover with a headless suite at desktop and iPhone 13

**Log:**
- 2026-08-07 09:58 CT — created; split out of FIX-042 (Claude Code)

### FIX-041 · Liv Renovations does not come up in search — find the lapse and fix it at the root

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-06 09:19 CT
- **Updated:** 2026-08-06 09:19 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: searching for **Liv Renovations** returns nothing. Establish first whether the contractor is genuinely absent from the underlying data or merely unreachable through search — those are different bugs with different fixes, and only one of them is a search bug.

Do not fix the symptom by special-casing this name. A contractor that exists in the data but cannot be found is a class of failure, and however Liv Renovations is being lost, other names are being lost the same way. The likely culprits, in order of suspicion: name normalization dropping or mangling a token; the search matching on a prefix or an exact string where a substring match is needed; the licensed-contractor match (FEAT-004/FEAT-014) failing to join a registry record so the entity never enters the index; the "open permits only" scope excluding a contractor whose work has all closed (which FEAT-042 is separately addressing); or dedup collapsing the entity under a variant spelling.

**Checklist:**
- [ ] Reproduce and record exactly what was searched, on which surface (Search Directory, GC view, Permit Map), and what came back — write it in this task's Log
- [ ] Query the raw dataset directly (DuckDB against the permits source, plus the contractor registry) for every name variant — "Liv", "LIV Renovations", "Liv Renovations Inc/LLC", with and without punctuation — and establish whether the records exist at all
- [ ] If the records exist: trace where they are lost — pipeline ingest, name normalization, the licence match, the open-permit scope filter, dedup, or the client-side search itself. Name the exact stage in the Log before changing anything
- [ ] If the records do not exist: determine why (data vintage, permit type out of scope, contractor never pulled a permit under that name) and say so plainly rather than treating it as a search defect
- [ ] Fix at the stage that loses it, not at the surface that reports it — a name-specific patch is not a fix
- [ ] Quantify the blast radius: how many other contractors does the same lapse hide? Run the corrected logic against the full index and report the count of entities recovered
- [ ] Add a regression test covering the failing case class (whatever the root cause turns out to be — a normalization case, a substring match, a join miss), so this specific lapse cannot return silently
- [ ] Verify on desktop and mobile: Liv Renovations is findable from the Search Directory and appears wherever contractors are listed

**Log:**
- 2026-08-06 09:19 CT — created (Divyam)

### FIX-040 · Search result count and "add to list" total don't update when work types are included/excluded

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-08-05 11:30 CT
- **Updated:** 2026-08-05 11:30 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: when a search is narrowed by including or excluding work types, the "how many found" count does not update to reflect the filtered set, and the count on the add-to-list action is likewise stale. The filter changes which permits show, but the two counts keep reporting the pre-filter total — so the numbers disagree with what's actually on screen and with what an "add all" would add.

Pairs with FIX-038 (tri-state include/exclude): whatever recomputes the visible result set on an include/exclude change must also drive both counts from that same set, so they can't drift. Find the single place the filtered result set is produced and derive the "found" count and the add-to-list count from it rather than from the unfiltered list.

**Checklist:**
- [ ] Reproduce: exclude (and, per FIX-038, include) a work type and confirm both the results-found count and the add-to-list count stay at the pre-filter number; note where each count is computed today
- [ ] Drive both counts from the same filtered result set the map/list actually renders, recomputed on every filter change (include, exclude, and the other filters too — check whether date/value/neighborhood filters have the same stale-count bug while you're here)
- [ ] Make "add to list" add exactly the counted set — the number shown and the number added must match
- [ ] Root-cause, not per-symptom: fix it where the count is derived so every filter path stays honest, rather than patching the work-type path alone
- [ ] Verify on desktop and mobile: the count updates live as work types are included/excluded and matches both the visible pins/rows and what add-to-list adds

**Log:**
- 2026-08-05 11:30 CT — created (Divyam)

### FIX-038 · Permit Map work-type filter: make each work type include-only, exclude, or neutral via a tri-state checkbox

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-05 11:20 CT
- **Updated:** 2026-08-05 11:20 CT
- **Tags:** Chicago Permit Search Tool

Requested by Divyam: the Permit Map work-type filter (`docs/map.html`, the exclusions behind the collapsed `<details>` from FEAT-024) is exclude-only today. Make each work type a **tri-state** control instead of a plain checkbox:

1. **Neutral** (default, empty box) — the work type does not constrain the search.
2. **Include** (one click, green check) — focus the search to this work type; only permits of the checked include types show.
3. **Exclude** (second click, red ✕) — permits of this type are removed from the results, as exclusions do today.

A third click returns to neutral. When any work type is set to Include, the result set is the union of the included types minus any excluded types — an explicit Include is a whitelist, so a search with includes set does NOT also show the untouched neutral types.

**Checklist:**
- [ ] Replace the exclude-only checkbox with a tri-state control cycling neutral → include (green check) → exclude (red ✕) → neutral; make the three states visually unmistakable and accessible (not color alone — the check/✕ glyph must carry the meaning too, with an accessible label/`aria` state)
- [ ] Define and implement the semantics: with no includes set, neutral means "shown" and excludes subtract (today's behavior); with any include set, only included types show, minus excludes — write the rule in the Log so include+exclude interaction is unambiguous
- [ ] Keep the collapsed `<details>` summary honest: show how many types are included vs excluded so a hidden filter is not invisible (ties into FIX-035's "exclusion behind a collapsed details" concern)
- [ ] Persist all three states with the rest of the map filters (see FIX-035), not just the excluded set
- [ ] Reflect the active include/exclude counts in the status strip alongside the other filters
- [ ] Degrade safely if a saved include/exclude names a work type that no longer exists — drop it rather than emptying the map
- [ ] Verify on desktop and mobile in both themes: include alone, exclude alone, include+exclude together, and all-neutral matching today's default result set

**Log:**
- 2026-08-05 11:20 CT — created (Divyam)

### FIX-039 · Make the tagging system more discoverable — creating a second tag is not intuitive

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-05 11:20 CT
- **Updated:** 2026-08-05 11:20 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: the current tagging system relies on comma separators and colors, and adding a **second** tag is not intuitive — nothing signals that a comma is how you start a new tag, and the color-only distinction does little to help. Rework the tag input so making multiple tags is obvious without instructions.

Reproduce and inventory first: find where tags are entered and rendered today (which pages, which control), and record what the current comma/color affordance actually is before changing it — the fix is a UX change to an existing control, not a new tagging model.

**Checklist:**
- [ ] Reproduce: locate the tag input(s) and note exactly why adding a second tag is unclear (no visible "add" affordance? comma-as-separator undiscoverable? tags not shown as distinct chips?) — write it in the Log
- [ ] Replace the bare comma-separated text field with a chip/pill input: each committed tag becomes a removable chip, and Enter (and comma) commits the current tag — the standard, discoverable pattern
- [ ] Show clearly how to add another tag (placeholder text, an explicit add affordance, or the chip pattern making it self-evident) so a second tag needs no explanation
- [ ] Don't rely on color alone to distinguish tags — give each chip a shape/label/remove control so it reads without color (accessibility)
- [ ] Preserve existing tags and their data on migration — the change is to input/display, not to what a tag is or how it's stored
- [ ] Verify on desktop and mobile in both themes: adding the first tag, adding a second and third, removing one, and editing an item that already has several tags

**Log:**
- 2026-08-05 11:20 CT — created (Divyam)

### FIX-037 · Adding to a full list from Search or the Permit Map silently deletes the oldest saved permits

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-05 10:34 CT
- **Updated:** 2026-08-05 10:34 CT
- **Tags:** Chicago Permit Search Tool

FEAT-035 found and fixed this in `docs/list.html`, but the same add path exists on `docs/index.html` and `docs/map.html` and was **not** fixed there. Both still do:

```js
numbers.forEach(number => { if (!next.includes(number)) next.unshift(number); });
state.userPermitNumbers = next.slice(0, userListLimit);
```

New permits are unshifted onto the head, then the list is sliced back to the 1000 cap — which trims the **tail**, i.e. the permits the user has had saved the longest. Adding 40 permits to a full list therefore destroys 40 older ones with no warning, no count, and no undo. `list.html`'s version instead fills to the cap and reports what did not fit (`{ added, skipped }`), which is the behaviour all three pages should share.

Found while implementing FEAT-032, which had to work around it: the provenance line records `Math.min(added, userListLimit)` so the count it writes is at least honest about what landed. Not fixed there because it changes add semantics on two pages and deserves its own verification.

**Checklist:**
- [ ] Port `list.html`'s cap-aware add (fill to the cap, count `added`/`skipped`, never trim the tail) into `docs/index.html` and `docs/map.html`
- [ ] Report the refusal to the user on both pages, the way `list.html` announces it
- [ ] Simplify FEAT-032's `Math.min(added, userListLimit)` back to `added` once the three paths agree
- [ ] Regression test: a full list plus an add loses nothing, on all three pages
- [ ] Check whether any other add path (drag-and-drop onto the list panel, "Add all" from a contractor card) shares the bug

**Log:**
- 2026-08-05 10:34 CT — found while implementing FEAT-032; filed rather than folded into it (Claude Code)
- 2026-08-05 11:00 CT — renumbered FIX-034 → FIX-037: FIX-034 was already taken by the "Attach permit notes to GCs and Open Subs" card; this card was filed under the same id by a separate session (Claude Code)

### FIX-033 · t12 presence-pill suite still asserts the pre-FIX-031 contract

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-08-04 12:52 CT
- **Updated:** 2026-08-04 13:18 CT
- **Tags:** Chicago Permit Search Tool

`verify-tmp/t12.js` fails deterministically on `main` — 3 runs out of 3 on a quiet machine, and identically on a FEAT-035 branch, so it is not caused by either. The assertion it fails is `closed.hidden`: after the live socket closes, the "N here" presence pill must be hidden. That is exactly the behaviour **FIX-031 deliberately inverted** on 2026-08-04: the pill is now bound to room membership rather than socket state, and a drop is held for a 25s grace period, because gating on the socket made the pill flash in and out while the actual viewers never changed. So t12 encodes the pre-FIX-031 contract and is asserting the bug FIX-031 fixed.

Found while verifying FEAT-035 (the full 70-script suite was 69 green, this the only red). Not fixed there because it is a question about the product contract, not about pagination.

**Checklist:**
- [x] Confirm the intended contract: after a genuine, deliberate leave the pill SHOULD clear — the FIX-031 change was about transient socket drops, not real departures. Decide what t12's "closed" case is actually simulating (a transient close, or a real leave)
- [x] Rewrite t12's `closed` case to match: if it simulates a transient drop, assert the pill PERSISTS through the grace period; if a real leave, drive `liveDisconnect()` and assert it clears
- [x] Cover the grace period explicitly — a drop then a reconnect inside 25s should never blank the pill
- [x] Re-run t12 3x to confirm it is deterministic, not just green once
- [x] Check the other presence suites (t56, t57, t58) for the same stale assumption
- [x] A SECOND stale case the card had not spotted: t12's "solo" step asserted the pill hides the instant a presence frame drops the count to 1, which the grace period also changed
- [x] Keep the suite discriminating after inverting two assertions — prove it with mutants rather than assuming

**Log:**
- 2026-08-04 12:52 CT — created while verifying FEAT-035; t12 is a stale test, not a regression (Claude Code)
- 2026-08-04 13:09 CT — started: reading t12's cases against the shipped presence contract (Claude Code)
- 2026-08-04 13:18 CT — the contract, read off the shipped code: `ws.onclose` deliberately does NOT touch presence ("the count has not changed just because our socket dropped"); a presence frame dropping below 2 is HELD for PRESENCE_SETTLE_MS (25s); only `liveDisconnect()` clears, immediately. So t12's `__wsClose()` case simulates a TRANSIENT drop and the pill is right to persist (Claude Code)
- 2026-08-04 13:18 CT — **two** stale cases, not one. Besides `closed`, the `solo` step asserted the pill hides the instant a frame drops the count to 1 — also changed by the grace period. Both rewritten to the current contract, plus an assertion on `state.live.settleTo` so "unchanged" is distinguished from "the frame was dropped on the floor" (Claude Code)
- 2026-08-04 13:18 CT — inverting two "must hide" assertions would have left a suite that a permanently-visible pill could satisfy, so a deliberate-leave case was ADDED to keep it discriminating. Proved with 4 mutants, all caught: restoring the ws.onclose repaint (the original FIX-031 flicker), removing the grace period, stopping a deliberate leave from clearing, and stopping a rise from cancelling a pending drop. The old t12 could never have caught the first of those — it asserted the bug (Claude Code)
- 2026-08-04 13:18 CT — t12 green 3/3 (was red 3/3, deterministically). t56, t57 and t58 all still green; no other suite carries the stale assumption. Grace-period mechanics deliberately NOT duplicated here — t58-presence-jiggle owns them. **DONE.** Note this fix lives only in the working tree: `verify-tmp/` is gitignored, which is FIX-020 (Claude Code)

### FIX-032 · t56-presence-lifecycle is flaky: pagehide sometimes leaves the socket open

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-08-04 11:04 CT
- **Updated:** 2026-08-04 11:35 CT
- **Tags:** Chicago Permit Search Tool

> **CLOSED WITHOUT A FIX (won't-fix), 2026-08-04, at Divyam's request.** The flake is still there at ~40%. `done` is the only closing status this board has, so this line exists to stop the status implying otherwise. Everything needed to pick it up again is below.

`verify-tmp/t56-presence-lifecycle.js` fails intermittently on the iPhone 13 leg with `pagehide left the socket open` and `expected exactly one new socket on resume`. **Measured at n=15 on each tree: 6/15 passing WITH FIX-031 and 6/15 on `main` — identical.** Pre-existing, and FIX-031 has no effect on it in either direction.

**The mechanism is known, and it points at the test, not the product.** t56 calls `showList()` **without awaiting it** — its own comment at line 44 says why ("map load can hang, connect is sync"). `showList` is async and calls `liveConnect` after an await, so its tail can land AFTER the test dispatches `pagehide`, opening a fresh socket. That produces exactly the observed `closedOnHide: false` / `socketsAfterHide: 2`. There is no path to those assertions from presence rendering.

Still worth one look at the product before fixing the test, per the standing rule that a flaky test accuses the product: `liveDisconnect()` calls `ws.close()` and returns without waiting, so on a REAL `pagehide` the close frame may not flush before the page freezes — the ungraceful case the server TTL exists to catch. The test uses a synchronous fake socket, so it cannot be observing that; but it is the question worth asking on a real device.

**Checklist (left unticked — none of this was done):**
- [ ] Await `showList()` in the test (or wait on a connect signal) and re-measure at n≥15 — a small sample cannot tell a 40% flake from a 60% one
- [ ] Separately, check on-device whether a real `pagehide` close frame reaches the room, or whether the TTL is doing that work in practice
- [ ] If it is only the test: fix the race properly, never with a bare sleep

**Log:**
- 2026-08-04 11:04 CT — created while fixing FIX-031 (Claude Code)
- 2026-08-04 11:35 CT — **closed at Divyam's request without a fix.** Stating what is being accepted, so nobody re-derives it later: `t56-presence-lifecycle` still fails ~60% of runs, and it is the guard for FIX-009's client half — session ids surviving a reload, the 30s heartbeat firing, `pagehide` closing the socket, and resume reconnecting. A suite that red 60% of the time will be read as noise, so **that guard is effectively gone**; a real regression in the presence lifecycle would not be noticed by it. Cheap to revive if wanted — the cause is known and is one `await` in the test (see above), not an investigation (Claude Code)
- 2026-08-04 11:23 CT — **CORRECTION to this card's original numbers.** It first said "2/6 on main, 5/6 with FIX-031 — improved by it". That was over-claimed from a sample far too small for a ~40% flake; a later run of the same tree gave 1/6. Re-measured at n=15 per tree: **6/15 both ways, no difference at all.** The lesson is not "measure" — I did measure — it is that **n=6 cannot support a directional claim**, and the original note stated one anyway (Claude Code)

### FIX-031 · Live-presence pill flickers in and out and shoves the page

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-08-04 10:40 CT
- **Updated:** 2026-08-04 11:35 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: with the list open on both mobile and desktop, the "2 here" presence pill keeps disappearing and reappearing, moving the page each time. **The count itself is correct** — both viewers really are there the whole time.

Two independent defects, both from FIX-009.

**1. The pill was bound to SOCKET state, not to who is in the room.** Three places turned a socket blip into a visible pop: `renderPresence` read `live.connected ? count : 0`, so the viewer's OWN momentary disconnect blanked it; `liveDisconnect()` zeroed presence before every reconnect; and `ws.onclose` repainted on the way down. None of those mean anybody left.

**2. Sockets churn on their own.** The room's 90s presence TTL is enforced against a client-side `setInterval`, and browsers throttle that in a hidden tab (Chrome to ~1/minute after 5 minutes hidden). Running the real `presenceFrom`, **one throttled tick was enough to reap a viewer who was sitting right there** — the survivor's count dropped to 1, the reaped client reconnected, and the cycle repeated every ~90s forever.

**Checklist:**
- [x] Diagnose why the count changes when the viewers do not
- [x] Stop the pill blanking on a transient reconnect (hold the last known count; only a deliberate leave clears it)
- [x] Stop the false reaping — TTL 90s → 300s, with the trade-off written into the source
- [x] Stop the layout movement — measured 5.9px on iPhone 13 / 3.7px desktop; `.title-row-end` now reserves the pill's 22.72px box
- [x] Regression test asserting geometry, desktop + iPhone 13, with mutants proving it discriminates
- [x] Cover the OTHER platform's mechanism — an iPhone firing `pagehide` disconnects cleanly, which the TTL cannot help; a 25s grace period on a drop makes a pocket trip invisible (added at Divyam's request after he asked whether both platforms were accounted for)
- [x] Deploy the Worker, then merge (the TTL lives in the Worker; the client half stands alone without it)
- [x] **Confirm on-device that the flicker is gone across a real mobile/desktop pair** — confirmed by Divyam 2026-08-04 on his own mobile + desktop pair, the one thing headless could not prove

**Log:**
- 2026-08-04 10:40 CT — reported by Divyam (Claude Code)
- 2026-08-04 11:04 CT — **built on branch `fix-031-presence-flicker` (`9b1c978`), pushed, NOT merged, Worker NOT deployed.** Verified with `verify-tmp/t58-presence-jiggle.js` — 24 assertions across desktop and iPhone 13, asserting that the element below the title row does not move on a socket blip, on a real 2→1 change, or going 1→3. **3/3 mutants caught**, including one that first exposed a genuine gap: the original suite never drove `liveConnect()`, so half the fix was unverified until an assertion was added for the real reconnect path. 190 Worker unit tests pass; the presence tests reference `PRESENCE_TTL_MS` symbolically so they follow the new value (Claude Code)
- 2026-08-04 11:04 CT — one measurement worth keeping: the remaining "1.4px of movement" after the layout fix was **not the pill at all** — it was `#user-list-panel`'s `listRise` animation still running while the first measurement was taken, drifting the whole panel. Waiting on `getAnimations()` before measuring cleared it. That is the same trap already recorded for contrast probes, hit again on geometry (Claude Code)
- 2026-08-04 11:04 CT — spun off **FIX-032**: `t56-presence-lifecycle` is flaky, measured at 2/6 on `main` versus 5/6 with this change. Pre-existing and improved here, not cured; raised rather than folded in silently (Claude Code)
- 2026-08-04 11:23 CT — **`a6f4da6`: a 25s grace period on a presence DROP.** Divyam asked whether the fix accounted for the issue appearing on BOTH mobile and desktop; checking properly showed the two platforms fail by different mechanisms and only one was covered. A desktop tab behind a window gets its heartbeat THROTTLED and is falsely reaped — the TTL fix. An iPhone whose screen goes off fires `pagehide` and disconnects CLEANLY, so the room is right to say one viewer; the TTL cannot help and should not. Holding a drop for 25s makes a pocket trip invisible while a real departure still resolves. Rises are never delayed, a deliberate leave bypasses it, and a repeated identical drop does not restart the clock — a reconnect re-sends room state, so re-arming per frame would stretch the hold forever. t58 now 44 assertions (22 per viewport), **7/7 mutants caught** (Claude Code)
- 2026-08-04 11:35 CT — **CONFIRMED ON DEVICE by Divyam** — "works" on his real mobile + desktop pair. That closes the only claim the headless suites could not make: the fix was verified at 390×844 in Chromium, which is not iOS Safari, and the whole point of the grace period was an iOS-specific `pagehide` behaviour that headless never exercises (Claude Code)
- 2026-08-04 11:33 CT — **DONE, merged and live** (`74f2c84`, `--no-ff`, branch deleted). Worker deployed by Divyam and verified before the merge — not by trying to read the TTL back (it is an internal constant and not externally observable), but by confirming the deployment landed at 16:26:28Z **from this branch**, with `PRESENCE_TTL_MS = 300000` in the tree and no uncommitted worker changes. API healthy, reference list `PeeXTko` still 99 permits. Re-verified on the MERGED tree before pushing: 190 Worker + 175 client unit tests, t58 and t57 green. Pages rebuilt and the live page confirmed to carry `applyPresence`, the 25s grace, the no-rearm guard, the reserved row height, and **no** trace of the old socket gate (Claude Code)
- 2026-08-04 11:23 CT — **CORRECTION: the 11:04 note above is wrong about FIX-032 and is left standing so the error is visible.** "2/6 vs 5/6, improved by this change" came from a sample far too small for a ~40% flake — a later run of the same tree gave 1/6, which by the same reasoning would have said this change made it three times worse. Re-measured at **n=15 per tree: 6/15 both ways, no difference**. FIX-031 does not affect that flake in either direction. I measured, which was right, but then drew a directional conclusion the sample size could not support (Claude Code)

### FIX-030 · closure.js: the 404 guard is written with real backspace bytes, so it never matches

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-08-03 15:59 CT
- **Updated:** 2026-08-07 09:30 CT
- **Tags:** Chicago Permit Search Tool

`worker/src/closure.js:156` writes the word-boundary `404` guard inside `isKeyMissingError` using two REAL 0x08 backspace bytes instead of escape sequences, so the regex tests for a literal backspace character and can never match. The 404 branch of that function is dead code.

Consequence is limited, and it fails in the SAFE direction. `isKeyMissingError` decides whether a KV read failure means "this key has never existed" (a genuine first run, establish a baseline) or "something went wrong" (abort, keep what is there). Under-detecting "key missing" means the closure seed treats an absent key as an error rather than as a first-run baseline — so it will NOT overwrite `closure:stats` with an empty object, which is exactly the catastrophe the comment block above that function was written to prevent. The accumulated observations behind FIX-012's live metric are not at risk. The second check, `/key .*not found/i`, may also cover the case in practice depending on how the installed Wrangler phrases the error.

Found by a repo-wide sweep for NUL/backspace bytes during FIX-009, which turned up exactly two hits across 316 tracked source files — the other was introduced and repaired in that same task. This is the fourth time invisible control bytes have landed in this repo's source, and the first one to survive in `main`; the class is worth a guard, not just a one-line repair.

**Checklist:**
- [x] Replace the two backspace bytes with proper `\b` escapes, byte-safely (never via a bash heredoc — that is how they get in)
- [x] Confirm the repaired regex actually matches a real Wrangler "404 ... not found" message, and that the pre-fix version does not
- [x] Decide whether the 404 branch is still needed at all, given `/key .*not found/i` may already cover it — **it is needed**, see the log
- [x] Add a cheap repo-wide guard against NUL/backspace bytes in tracked source, so the next one is caught at commit rather than by chance
- [x] Worker tests green (200 pass) — **but there is nothing to deploy**, see the log
- [x] Correct the test fixture that hid this: it used a key name that never occurs in production
- [x] Merge to main

**Log:**
- 2026-08-03 15:59 CT — created from a FIX-009 side finding; reported to Divyam, who asked for a card (Claude Code)
- 2026-08-04 13:22 CT — started (Claude Code)
- 2026-08-04 13:34 CT — fixed byte-safely on branch `fix-030-control-bytes` (b4befcc); the committed blob holds zero 0x08 and zero NUL. Worth recording that the repair itself twice reintroduced the bug: writing the replacement through a shell heredoc, `\\b` collapsed to a real 0x08 before Python ever saw it — once in the source fix, and again while writing THIS board entry. Both times an assertion on the replacement string caught it. The working method is to build the backslash numerically (`bytes([92])` / `chr(92)`) so no layer of escaping can reach it (Claude Code)
- 2026-08-04 13:34 CT — **the consequence was worse than "dead branch".** Verified against LIVE wrangler output captured from this repo's own KV namespace during the fix: repaired guard `true`, pre-fix guard `false`, fallback `/key .*not found/i` **`false`**. So `isKeyMissingError` returned FALSE for a genuinely absent key, and a real first run would have aborted with "KV read failed, refusing to continue" instead of establishing a baseline. Still the safe direction, and the accumulated observations were never at risk — but the first-run path was broken, not merely redundant (Claude Code)
- 2026-08-04 13:34 CT — **the 404 branch IS still needed.** The fallback wants the literal word "key" followed by a space, which the real message only contains when the KEY NAME ends in "key". The fixture's did — `closure%3Adefinitely_not_a_key` — which is exactly why this test passed for six weeks while the branch it exists to cover was dead. The fixture now uses `closure:stats`, the key the seed actually reads, and a new test strips anything the fallback could latch onto so the 404 branch must answer alone. Three mutants all caught: restoring the 0x08 bytes, removing the branch, dropping the word boundaries (Claude Code)
- 2026-08-04 13:34 CT — guard added as `worker/test/control-bytes.test.mjs`: scans every tracked text file for 0x08/0x00, reports file:line, and carries a probe proving the scan can fire. It runs in the normal `node --test test/*.test.mjs`, which CI already executes BEFORE the daily seed writes to production KV. Proved by poisoning a DIFFERENT file (`worker/src/stats.js`) with each byte in turn — both caught. This is test/CI-time, not literally commit-time: a pre-commit hook lives in `.git/hooks`, is untracked, and cannot be shared through the repo — offered to Divyam as a local extra. Its own sanity assertion earned its keep at once: `git ls-files` is CWD-relative, so run from `worker/` the first version saw 30 files instead of 316 and would have guarded almost nothing (Claude Code)
- 2026-08-04 13:34 CT — **nothing to deploy.** The checklist assumed this code ships in the Worker; it does not. Traced the entry point's transitive imports: `closure.js` is absent from the `src/index.js` bundle and is imported only by `seed-kv.js`, which runs in GitHub Actions. The fix reaches production on the next scheduled seed once merged, so the Worker was deliberately NOT redeployed rather than taking a no-op production action (Claude Code)
- 2026-08-04 13:34 CT — note: the preceding board commit (beead92) carries a message describing all of this, but its content was only the in-progress marker — the script that wrote the detail aborted on the backslash trap above after the commit had been staged. Corrected here rather than by rewriting pushed history (Claude Code)
- 2026-08-04 13:37 CT — merged to main with --no-ff (641b309) and pushed; branch deleted. 200 Worker tests green on the merged tree and the committed `closure.js` blob confirmed to hold zero 0x08 and zero NUL. No deploy and no Pages rebuild are involved: `closure.js` ships in neither, so the fix takes effect on the next scheduled GitHub Actions seed, which now also runs the new control-byte guard before it writes to production KV. **DONE.** (Claude Code)
- 2026-08-04 13:41 CT — pre-commit hook installed at Divyam's request, as the commit-time half the tracked test cannot cover: `.git/hooks/pre-commit` plus `.git/hooks/control-bytes-check.mjs`. It scans STAGED content (what is actually being committed, not the working tree), reports file:line, and explains that an editor and `sed` will both render the file as though it were already correct. Verified five ways: a clean commit still passes; a backspace is blocked; a NUL is blocked; `--no-verify` still overrides; and a tracked PNG containing 810 backspace bytes and 2,153 NULs is correctly NOT flagged, so the extension allowlist does not false-positive on binaries. **Local to this machine only** — `.git/hooks` is untracked and a re-clone loses it. Making it recoverable would mean committing the script and setting `core.hooksPath`; not done, as it changes repo layout for every clone (Claude Code)
- 2026-08-07 09:30 CT — **backfilled from git: the 08-04 13:41 decision above was reversed the next day and never logged.** Branch `fix-030-durable-hook` did exactly the thing that entry says was "not done" — the hook script is now tracked at `scripts/hooks/control-bytes-check.mjs` + `scripts/hooks/pre-commit`, with `.gitattributes`, 57 new lines of `worker/test/control-bytes.test.mjs`, and a `CLAUDE.md` line telling a fresh clone to run `git config core.hooksPath scripts/hooks`. Commits `76f7084` + `247282f`, merged to `main` as `5aff824` on 2026-08-06 and pushed. The guard is no longer local to one machine, so the "a re-clone loses it" caveat above is obsolete — it is opt-in per clone via `core.hooksPath` rather than automatic (Claude Code)

### FIX-029 · Map search "clear" button is a 44×28 touch target, under the 44×44 minimum

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-08-03 13:11 CT
- **Updated:** 2026-08-03 14:40 CT
- **Tags:** Chicago Permit Search Tool

Found by the specificity audit run after FIX-028 (see that card for the pattern). The `×` clear button inside the map search field declares `32px` square (`28px` below 640px), but `.map-search button { min-width: 44px }` scores **0-1-1** and outranks the bare `.map-search-clear` at **0-1-0**, so the width declarations are dead and it renders **44px wide**. `min-height` is not declared by the winner, so that one DOES apply — giving a **44×28** target on mobile and 44×32 on desktop, under the 44×44 minimum.

Second, smaller consequence: the input reserves `padding-right: 42px` for a button that is actually 44px wide at `right: 6–8px`, so the button intrudes ~10px into the text area. Screenshotted at an iPhone 13 viewport with a normal-length address — **no visible defect**, the intrusion only shows with text long enough to scroll under the `×`. Low severity; the touch target is the real issue.

Present identically on all three pages — the `.map-search` block is byte-identical across `index.html`, `map.html` and `list.html`.

**Checklist:**
- [x] Give the clear button a full 44×44 hit area without changing the glyph
- [x] Make the rule actually win, so the declared sizes stop being a lie
- [x] Reserve enough input padding that the button no longer overlaps the text
- [x] Apply to all three pages and keep the shared block byte-identical
- [x] Regression test, proven to fail against the un-fixed code
- [x] Merge to main and verify live

**Log:**
- 2026-08-03 13:11 CT — created from the FIX-028 audit; status → in-progress. Working on `fix-029-map-search-clear-target` (Claude Code)
- 2026-08-03 13:57 CT — fixed on `fix-029-map-search-clear-target` (`0b55836`, pushed, NOT merged). Scoped the rule to `.map-search .map-search-clear` (**0-2-0**) so it genuinely outranks `.map-search button` (0-1-1) and the declarations stop being a lie, then set 44×44 at every viewport. The glyph is unchanged — the button is transparent until hover, so only the hit area and the hover circle grow; screenshotted before/after at an iPhone 13 viewport and they are visually identical. Input `padding-right` 42px → 52px, since the old value reserved less than the button's real width (Claude Code)
- 2026-08-03 13:57 CT — verified: `verify-tmp/t55-map-clear-target.js`, 28 assertions across three pages × two viewports, **confirmed to FAIL against un-fixed main with 14 reds** at exactly the values on this card (44×32 desktop, 44×28 mobile, 8px/10px text intrusion). The specificity audit that raised this now reports **CRITICAL 0, down from 1**; its 5 remaining REVIEW items are the INVERSE relationship — `.map-search .map-search-clear` correctly outranking `.map-search button` — which is the intent. 164 Worker unit tests green. All three pages byte-checked (no control bytes, line endings preserved: index/map LF, list CRLF) and the shared `.map-search` block confirmed still byte-identical across them (Claude Code)
- 2026-08-03 13:57 CT — **scope note worth recording: on `list.html` this button is not reachable at all.** `body.list-page .layout { display: none }` hides the entire search directory there, so the element has no layout box and only its computed contract can be asserted. It exists on that page purely because the three copies of the `.map-search` block are kept identical. t55 asserts computed `min-width`/`min-height` on every page and geometry only where a layout box exists, rather than silently skipping the page (Claude Code)
- 2026-08-03 13:57 CT — **the full browser sweep is NOT clean, and it is not this change.** Two sweeps both returned 63/64 with a DIFFERENT single red each time: run 1 red `t27-scrolllock`, run 2 red `t49-value-range` (and t27 green). A regression fails the same test every time; alternating reds is flake. Both pass in isolation — t27 **9/9**, t49 **3/3**. Neither has a causal path to this diff: t27 exercises the permit overlay in directory mode where `.map-search` is not rendered at all, and t49's failing assertion is "rendered map source matches the filter []", i.e. map data had not loaded, not styling. t27's failing assertion carries a **4px desktop tolerance** against Chromium scroll anchoring that the test's own comment acknowledges re-settles ~50px on that path (it allows 64px on mobile) — a tight tolerance that is a latent flake independent of any change. Currently re-running the sweep with the two NEW suites held out, to rule out that adding them increased contention. **Flakiness is being tracked as its own concern, not silently absorbed into this card** (Claude Code)
- 2026-08-03 14:40 CT — **DONE, live.** Divyam approved the merge; `--no-ff` to main (`47a64a6`), branch deleted, Pages build green. Verified in the right order — waited for the deploy, confirmed the deployed `map.html` is byte-identical (md5) to `main`, then measured. **t55 passes 28/28 against production.** Merge-only ship, no Worker change (Claude Code)
- 2026-08-03 14:40 CT — **CORRECTION to the 13:57 flake entry.** I wrote that holding the two new suites out gave 62/62 and that this "implicated" them. That inference was wrong on two counts. (1) It rested on a single green run. (2) The sweep runs suites **alphabetically**, so `t49` is #50 and `t54`/`t55` are #55–56 — they execute AFTER `t49` and cannot affect it. A later sweep with a lightened `t55` went red on `t49` again, and a further one came back **64/64 green**. The honest reading: `t49-value-range` flakes at roughly 50% under sweep contention on the assertion "rendered map source matches the filter []" (map data not loaded in time), passes 3/3 in isolation, and is unrelated to any change made today. `t27-scrolllock` flaked once, on an assertion with a 4px desktop tolerance against Chromium scroll anchoring that its own comment says re-settles ~50px on that path. Both are pre-existing test-infrastructure flakes and deserve their own card if they keep costing time (Claude Code)

### FIX-028 · My Permit List toolbar buttons are all different widths

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-08-03 12:32 CT
- **Updated:** 2026-08-03 14:56 CT
- **Tags:** Chicago Permit Search Tool

**CORRECTION 2026-08-03 14:37 CT — the first fix was wrong on desktop and this card overstated its own reasoning.** It shipped a 156px floor and recorded the resulting two-row wrap as unavoidable. It was not: 156px was simply too wide. Divyam reported `Clear list` / `Delete list` sitting on a separate row. See the reopened log below.

Raised by Divyam: the buttons on the My Permit List toolbar should all be the same width instead of each sizing to its own label. Measured on production at a 1280 viewport — the eight buttons ranged from **92.7px (Share) to 153.9px (Optimize route)**, a 61.2px spread. On an iPhone 13 the spread was worse: 96.7px to 344px.

**Checklist:**
- [x] Measure the real spread on both viewports rather than eyeballing it
- [x] Decide whether the two destructive buttons keep their spatial separation — **Divyam chose to keep the gap**, which also matches the `destructive-emphasis` guidance that dangerous actions be separated spatially, not by colour alone
- [x] Equalize on desktop
- [x] Equalize on mobile
- [x] Confirm equalizing did not clip labels, break the 44px touch height, or add horizontal scroll
- [x] Regression test, proven to fail against the un-fixed code
- [x] Merge to main and verify live
- [x] Keep all eight on ONE desktop row (reopened — the first fix wrapped)

**Log:**
- 2026-08-03 12:32 CT — created and fixed on `fix-028-toolbar-button-widths` (`92fdcaa`, pushed, NOT merged). Status → in-progress (Claude Code)
- 2026-08-03 12:32 CT — **one symptom, two separate causes.** On desktop `.user-list-toolbar button` sets `width: auto`, so each button sized to its own label. On mobile the rule intended to equalize them — `.toolbar-primary > *` at **0-1-0** — silently LOST to `.user-list-toolbar button` at **0-1-1** and never applied at all, so they were content-sized there too and one button stretched to the full 344px. That is the same partial, silent specificity loss recorded on FIX-025, now the 4th occurrence in this codebase. Only the `.toolbar-primary`/`.toolbar-manage` arms of that rule were dead; its `.panel-actions` / `#result-count` arms work and were left alone (Claude Code)
- 2026-08-03 12:32 CT — **equal width forces a wrap, and this was measured before committing to it rather than discovered after.** Eight buttons at the widest label need ~1296px including gaps; the toolbar is 1039px at a 1280 viewport and 1199px at 1440. No realistic desktop fits all eight on one row at a readable size, so the destructive pair now sits on its own row, right-aligned. That strengthens the separation rather than weakening it. Desktop uses a shared 156px `min-width` (not `width`, so a label that ever outgrows it widens its own button instead of clipping); mobile uses two equal grid columns — grid rather than flex because the 6-button and 2-button groups would each divide their own row under flex and land on different widths (Claude Code)
- 2026-08-03 12:32 CT — verified: `verify-tmp/t54-toolbar-widths.js`, 12 assertions across desktop and iPhone 13, **confirmed to FAIL against un-fixed `main`** (61.2px spread desktop, 247.3px mobile) by serving `git show main:docs/list.html` on a second port. All 8 buttons now measure 156px on desktop and 168px on mobile. The suite also covers what equalizing could plausibly break — no clipped labels, ≥44px touch height, no horizontal scroll, and the destructive pair still separated. Full regression: **63/63 browser suites**, 164 Worker + 152 client unit tests. Rendered in both themes at both viewports. `docs/list.html` byte-checked: no control bytes, all 9369 CRLF preserved (Claude Code)
- 2026-08-03 12:32 CT — scope note: `index.html` and `map.html` also carry a `.user-list-toolbar` class, but it is a DIFFERENT component there (a 3-column grid of labelled `.action-group`s, hidden until a permit is saved), not this 8-button row. Left untouched — it was not what was reported and its buttons are not ragged in the same way (Claude Code)
- 2026-08-03 12:38 CT — **DONE, live.** Divyam approved the merge; `--no-ff` to main (`60605db`), branch deleted, Pages build 2m16s. Merge-only ship, no Worker change. Verified at the destination in the right order — waited for the deploy to finish first, then confirmed the deployed `list.html` is byte-identical (md5) to `main` before measuring, so the probe could not be reading the old version. **Live result: all 8 buttons at 156px on desktop and 168px on iPhone 13, spread 0.0px on both.** t54 passes 12/12 against production. Re-checked against a REAL shared list rather than the local fixture, because the fixture renders "Publish…" where a real list renders the longer "Edit details", and the 156px floor is tied to label widths — both land at 156px, as does the "Notes 1" count-badge variant (Claude Code)
- 2026-08-03 14:37 CT — **REOPENED. The desktop half of this fix was wrong, and the card's own reasoning was the error.** Divyam reported `Clear list` / `Delete list` on a second row. The 12:32 log claimed "no realistic desktop fits all eight on one row at a readable size" — that was measured against the 156px floor I had already chosen, not against what the labels actually need, so it justified the wrap with a number of my own making. Circular, and wrong (Claude Code)
- 2026-08-03 14:37 CT — the equal width is bounded from BOTH sides: at least the widest button's natural width, or equality breaks; at most `(container - gaps) / 8`, or the row wraps. Measured containers: 1039px @1280, 1125px @1366, 1199px @1440, 1295px @1536, **capped at 1398px** — so the ceiling is 121px @1280 and 141px @1440, and it was already one row at 1600+. At the original 14px padding / 0.86rem the widest button (`Optimize route`) is **147.6px** naturally, which clears the ceiling on every desktop below 1536. Trimming padding, font and icon gap drops that to **117.6px**, which fits from 1280 up — so one row was always achievable, just not at 156px (Claude Code)
- 2026-08-03 14:37 CT — fixed on `fix-028b-toolbar-one-row` (`f63181b`, pushed, NOT merged). Two desktop tiers so wide screens do not pay for the narrow case: **120px below 1400px, 136px above**. Scoped to `min-width: 641px` so mobile keeps its base sizing and its own two-column grid — a blanket change would have shrunk mobile buttons to ~11.7px text, since `body` is 15px there. Verified one row, equal widths and no clipping at **1280 / 1366 / 1400 / 1440 / 1536 / 1600 / 1920**; the destructive pair keeps its gap. t54 now asserts a single row at BOTH desktop tiers and is confirmed to fail against `main` with "2 rows" at 1280 and 1440 (Claude Code)
- 2026-08-03 14:56 CT — **DONE, live.** Divyam approved the merge; `--no-ff` to main (`a857705`), branch deleted, Pages build green. Merge-only ship, no Worker change. Verified in the right order — waited for the deploy, confirmed the deployed `list.html` is byte-identical (md5) to `main`, then measured. **Live: one row at 1280 / 1366 / 1400 / 1440 / 1536 / 1600 / 1920, all eight equal (120px under 1400, 136px above), no clipped labels, no horizontal scroll at any width.** Checked against a REAL shared list, not the local fixture, so the longer "Edit details" label is the one being measured. t54 20/20 against production, including the new single-row assertion at both desktop tiers. Full sweep 64/64 green before merge (Claude Code)
- 2026-08-03 14:56 CT — lesson recorded outside the board: the failure here was not the 156px value, it was justifying the resulting wrap with a measurement taken against that same self-chosen value and then presenting it to the user as a deliberate benefit. A real constraint survives varying your own inputs (Claude Code)

### FIX-027 · Icon names flash as text and scroll the page sideways before the icon font loads

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-08-03 11:03 CT
- **Updated:** 2026-08-03 11:12 CT
- **Tags:** Chicago Permit Search Tool

Every `<span class="material-symbols-outlined">` lays out its LIGATURE NAME as literal text until the Material Symbols font arrives. At 22px `moon_stars` is 4.6em wide instead of 1em, and `keyboard_double_arrow_down` is 12.5em. The theme toggle is `position: fixed` against the right edge, so on every cold page load the document scrolled sideways — 409/390 on `index.html`, 405/390 on `list.html`, 395/390 on `disclaimer.html` — and the nav briefly read "da… Search Directory / ma… Permit Map".

Found by chasing why **t28-uiux-lock and t43-tagchips had both been red on main**. Neither was about what its name says: t43 measures `hScroll` immediately after `data-ready` and caught it every run; t28 samples `hScroll` three times and only the first was true, because it raced the font load — which is exactly why it flapped between 3 and 4 failures rather than failing consistently.

**Checklist:**
- [x] Reproduce with the icon font blocked, so the pre-font state is stable rather than a 50ms race
- [x] Name every offending icon on all four pages at an iPhone 13 width
- [x] Declare `font-display: block` on the Material Symbols request
- [x] Bound the icon box so the ligature text cannot push layout even when the font never arrives
- [x] Prove no icon moved once the font IS loaded
- [x] Confirm t28 and t43 go green, repeatedly (t28 was the flaky one)
- [x] Merge and confirm on the live site

**Log:**
- 2026-08-03 11:03 CT — created and fixed in the same session, at Divyam's request to "work on t28 and t43". Card written after the fact because neither suite had one (Claude Code)
- 2026-08-03 11:03 CT — fixed on branch `fix-027-icon-font-overflow` (`a646e2e`, pushed, NOT merged — awaiting approval). Client-only, all four `docs/*.html`; no Worker deploy. Two parts. (1) `&display=block` on the Material Symbols URL — **verified this is not a no-op**: fetching the OLD url returns no `font-display` declaration at all, leaving it to the browser default, while the new one returns `font-display: block`. (2) `max-width: 1em; min-width: 0; overflow: hidden` on the base `.material-symbols-outlined` rule. **`min-width: 0` is load-bearing**: these spans are flex items inside the nav links and the theme toggle, where the default `min-width: auto` resolves to min-content — the full unwrappable text — and min-width beats max-width, so the cap alone was silently ignored. Six sites in `list.html` (`#filter-followup`, `.fu-badge`, `.pm-fu`, `.feed-src`) already applied this exact pattern ad hoc; it belongs at the base (Claude Code)
- 2026-08-03 11:03 CT — **a geometry baseline caught a regression that would otherwise have shipped.** All 62 icons were measured with the font LOADED before anything was touched; after the fix two had moved — `disclaimer.html`'s `policy` badge went 48px → 24px, because `.disclaimer-icon` is a 48px circular badge that CONTAINS the glyph rather than being it, and `max-width` beats `width`. Fixed with `max-width: none` there; the re-check reports all 62 unchanged, which also clears the other risk in this change (`overflow: hidden` on an inline-block moves its baseline) (Claude Code)
- 2026-08-03 11:03 CT — verified by `verify-tmp/t53-icon-font.js`: 48 assertions over all four pages at desktop and iPhone 13, in both the font-blocked and font-loaded states, **proven red first at 10 failures against the unfixed tree**. t28 now passes 5/5 (it failed every single run before) and t43 3/3. 164 Worker unit tests pass. One earlier version of the guard had a false positive worth remembering: it measured icon width in ems, which for a `display: block` icon measures the CONTAINER, not the glyph — `disclaimer.html` has a legitimate 48px block icon that looked like a 2em failure. The check now skips container-sized displays (Claude Code)
- 2026-08-03 11:12 CT — **DONE, live.** Merged to `main` first of the two (`8885e8d`, `--no-ff`) at Divyam's request, branch deleted, Pages rebuilt. Verified against the LIVE site on an iPhone 13 with the font BINARY blocked but its CSS allowed — the real slow-network state, not a synthetic one: all four pages report 390/390 with no horizontal scroll, and `font-display: block` is on every request. Re-verified on the merged tree before pushing, since FEAT-024 touched `map.html` too (Claude Code)
- 2026-08-03 11:03 CT — the change also broke `t42-uiux-feed` and `t45-uiux-followup`, and that was mine: both parsed the font URL with `.split("icon_names=")[1]`, assuming `icon_names` was the LAST query parameter, so appending `&display=block` turned the final entry into `"sunny&display=block"` and made them report a declared icon as missing. Both now parse with `URLSearchParams` and were controlled to confirm they still catch a genuinely undeclared ligature. Worth keeping — that assertion guards the same class of bug this card fixes (Claude Code)

### FIX-024 · A second page scrollbar appears after opening and closing a permit

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-31 14:05 CT
- **Updated:** 2026-07-31 14:05 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: opening a permit in My Permit List (`docs/list.html`) and closing it leaves a second scrollbar down the side of the page.

Root cause was not the overlay. `body` carried `overflow-x: hidden` alongside `html`. On body that buys nothing — the root's overflow propagates to the viewport, so the page is already immune to sideways scroll — but it forces body's `overflow-y` from `visible` to `auto`, making body a SECOND full-page scroll container behind `html` (the real page scroller). It hides while body's content fits its own box exactly; body's border box is a fractional 960.27px, and the overlay's open/close perturbs layout enough that body's `scrollHeight` rounds up 1px, so body gains a pixel of scrollable overflow and paints its own scrollbar.

**Checklist:**
- [x] Reproduce and identify the second scroller (body, not the overlay or the scroll lock)
- [x] Remove the redundant `overflow-x: hidden` from `body` on all three pages
- [x] Remove the duplicate copy inside each ≤640px block (list keeps it on `main`; index scopes it to `html`)
- [x] Confirm no horizontal scroll returns on any page at 1280/390/320
- [x] Guard test that fails against the pre-fix code
- [x] Merge and deploy
- [x] Confirm on Divyam's own browser after deploy (headless cannot render scrollbars — see log)

**Log:**
- 2026-07-31 14:05 CT — created from a user report, already diagnosed and fixed in the same session (Claude Code)
- 2026-07-31 14:05 CT — fixed on branch `fix-second-scrollbar` (`7500b62`, pushed, awaiting merge approval). Verified behaviourally: before the fix `document.body.scrollTop` actually moved after a close; after it does not, and body computes `overflow-y: visible`. `verify-tmp/t48-second-scrollbar.js` (12 assertions, desktop + iPhone 13, three open/close cycles) fails 10/14 against the pre-fix code. No horizontal scroll on any of the four pages at 1280/390/320. Full browser suite + 286 unit tests pass. (Claude Code)
- 2026-07-31 14:05 CT — CAVEAT: this headless build has overlay scrollbars (width 0) and CANNOT render the symptom. A forced-`::-webkit-scrollbar` probe was tried and rejected — a control read 2px on a known scroller, so the probe was blind, not clean. The fix rests on structural evidence (body was a scroll container with real scrollable overflow, and now is not), so the last checklist item is a human confirmation on a classic-scrollbar browser. (Claude Code)
- 2026-07-31 14:05 CT — NOTE: `map.html`'s ≤640px `body.map-page { overflow-y: auto }` deliberately opts body into scrolling and was left alone. (Claude Code)
- 2026-07-31 14:14 CT — merged to `main` with user approval (`27e341d`, `--no-ff`), branch deleted, GitHub Pages deployed (2m25s). Verified against the LIVE site by driving a real open/close at 1280px and on iPhone 13: body computes `overflow-y: visible`, does not scroll independently, no horizontal scroll, zero page errors. Still open: Divyam's own confirmation on a classic-scrollbar browser — hard-refresh first (Ctrl+Shift+R). (Claude Code)
- 2026-07-31 14:22 CT — CONFIRMED FIXED by Divyam on his own browser: the second scrollbar is gone. Closes the one thing headless could not verify. (Claude Code)

### FIX-004 · Scope Optimize Route to the full permit list

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 15:55 CT
- **Updated:** 2026-07-29 19:51 CT
- **Tags:** Chicago Permit Search Tool

Optimize Route in My Permit List (`docs/list.html`) should optimize across every permit in the saved list, not a subset. Google Maps caps waypoints per link, so the list is chunked for export — that export chunking must not also cap what the optimizer considers.

The bound turned out to be neither export chunking nor visible rows: it was a flat refusal above OSRM's 100-coordinate Table limit, so a longer list got no sort at all. The matrix is now assembled from tiles and the sort covers the whole list.

**Checklist:**
- [x] Find where the current optimize-route scope is bounded (export chunking, visible rows, or a hard waypoint cap)
- [x] Run the optimization across the entire saved list, independent of export chunking
- [ ] Keep Google Maps chunk generation as a presentation step applied after optimization — *skipped at Divyam's request ("ignore the Google Maps step"); export chunking was already downstream of ordering and was not touched*
- [x] Verify the resulting order and total drive time improve on a long list
- [x] Check OSRM request count and runtime on a large list; note any practical ceiling in this task's Log
- [x] Above the ceiling, make Optimize route unusable rather than clickable-then-failing (added at Divyam's request)

**Log:**
- 2026-07-27 15:55 CT — created (Divyam)
- 2026-07-29 18:30 CT — in-progress (Claude Code)
- 2026-07-29 18:35 CT — checklist item 1 answered: the scope was NOT bounded by export chunking or visible rows. `fetchRouteLegs` already batches at 50 and `routeRows` never slices. The only limit was `optimizeUserListRoute` refusing outright when the list exceeded OSRM's 100-coordinate Table cap (Claude Code)
- 2026-07-29 18:40 CT — measured the local search before redesigning it, and the assumption that it needed rewriting was wrong: 82ms at 100 stops, 2.7s at 300. Left it alone (Claude Code)
- 2026-07-29 18:49 CT — done on branch `fix-004-route-scope` (`5edbccb`, pushed, NOT merged — awaiting approval). Tiled matrix: two 50-blocks per request via `sources=`/`destinations=`, both directions fetched (driving durations are asymmetric), 4 requests in flight at a time (Claude Code)

- 2026-07-29 19:19 CT — `cec087a` on the same branch: above the cap the Optimize route button is now `aria-disabled` with the reason in a note under the toolbar, rather than a button that accepts a click and then fails. `aria-disabled` not `disabled`, so keyboard/screen-reader users can still reach it and hear why. ui-ux-pro-max pass caught two defects in the first cut — `opacity: 0.5` dropped the label to 2.05:1 contrast (now muted tokens, 6.32:1 light / 8.51:1 dark), and the note inherited `.small` at 11.2px under the 12px floor — plus one only the screenshots showed: the note originally sat a full phone screen below the button it explains. Guards `t32-optimize-cap.js`, `t33-uiux-cap.js`; 23 browser suites green (Claude Code)
- 2026-07-29 19:51 CT — merged to main (`49d2526`, --no-ff) at Divyam's request and pushed; branch deleted, live on GitHub Pages. Verified on the merged tree alongside FIX-016: 111 client + 117 Worker unit tests and all 25 browser suites green, byte-identity held. Client-only, no Worker deploy needed (Claude Code)
- 2026-07-29 19:19 CT — discussed raising the ceiling. Divyam plans longer lists, so the agreed next step if 400 is hit is cluster-then-route: k-means the stops, optimize each cluster, then order the clusters. That cuts 1000 stops from 400 Table requests / ~115s to ~11 requests / ~0.8s and matches how a route is actually driven (finish a neighborhood before crossing town). NOT built — worth its own card if lists start exceeding 400 (Claude Code)

**Request count and runtime (checklist item 5).** Requests are exactly `ceil(n/50)^2` — 50/50 is the optimal split of the 100-coordinate budget, giving the most cells (2500) per request:

| stops | Table requests | local search |
|---|---|---|
| 100 | 1 (unchanged fast path) | 0.08s |
| 150 | 9 | 0.18s |
| 300 | 36 | 2.7s |
| 400 | 64 | 6.2s |
| 500 | 100 | 12.5s |
| 600 | 144 | 25s |

**Practical ceiling: 400 stops** (`MAX_SORT_STOPS`). The matrix itself tiles indefinitely — the ceiling is `greedyRouteOrder`'s ~O(n³) local search, which blocks the main thread. 400 also keeps requests at 64. `verify-tmp/bench/sort-scaling.mjs` reproduces the table against the shipped `docs/list.html`. Runtimes are CPU only; OSRM latency was NOT measured at scale, deliberately — hammering the public demo server to benchmark it would be abuse. At a rough 300ms/request with 4 in flight, 400 stops implies roughly 5s of fetching on top. If the sort is ever wanted above 400, the fix is incremental delta evaluation in the local search (2-opt on an asymmetric matrix needs prefix sums, not an O(1) delta), plus self-hosting OSRM.

### FIX-005 · Share on My Permit List hangs when a link is already generated

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 16:00 CT
- **Updated:** 2026-07-29 18:28 CT
- **Tags:** Chicago Permit Search Tool

Share in My Permit List (`docs/list.html`) appears to get stuck when a share link has already been generated — a second Share attempt hangs instead of reusing or regenerating the existing link.

Two separate defects. The hang was `await navigator.share()` sitting inside `withListAction`, which has no timeout: a share sheet dismissed without a choice can leave that promise pending forever, and `setListActionBusy(true)` disables *every* `[data-list-action]` button — so Share, CSV export, drive distances and sort all died together for the rest of the session. Separately, the first Share minted a share id but never joined the live room it points at, so edits made after sharing never reached the shared copy.

**Checklist:**
- [x] Reproduce: generate a share link, then invoke Share again in the same session
- [x] Identify the stuck state (unreset in-flight/"generating" flag, an unresolved promise, or a modal left open behind the scenes)
- [x] Make repeat Share reuse the existing link, or regenerate cleanly when the list has changed since
- [x] Reset share state on failure so it can never latch permanently
- [x] Verify repeated Share on desktop and mobile, including after editing the list between shares
- [x] Connect to the live room when a share id is first minted, so post-share edits reach the shared copy

**Log:**
- 2026-07-27 16:00 CT — created (Divyam)
- 2026-07-29 18:05 CT — in-progress (Claude Code)
- 2026-07-29 18:10 CT — reproduced: a non-settling `navigator.share()` leaves 7/7 toolbar buttons disabled and `state.listActionBusy` true permanently; every later Share then returns silently at `withListAction`'s busy guard. Note the board's "when a link is already generated" framing is a correlation — the hang is reachable on any Share that opens the sheet (Claude Code)
- 2026-07-29 18:14 CT — found a second defect while checking the "list has changed since" item: the first Share never called `liveConnect`, so the publisher sat disconnected from its own room and `sendListOp` dropped every subsequent edit (measured 0 sockets, 0 ops). Shared copies went stale while the same link kept being handed out (Claude Code)
- 2026-07-29 18:18 CT — fixed on branch `fix-005-share-hang` (`d64c586`, pushed, NOT merged — awaiting approval). `navigator.share` raced against a 20s bound; `liveConnect(id)` on mint. New guards `t29-share-hang.js` (desktop + 390px, also asserts no stale `aria-busy`) and `t30-share-live.js`; both proven to fail against the bugs. 111 client + 117 Worker unit tests and 20 browser suites green. Client-only, no Worker deploy (Claude Code)
- 2026-07-29 18:18 CT — caveat: the never-settling share sheet is a real desktop-Chrome behaviour that cannot be reproduced in the headless build, so it is simulated. The 20s bound means a dismissed sheet can still hold the toolbar for up to 20s — better than forever, not instant; a focus-based release would be the follow-up if that proves annoying (Claude Code)
- 2026-07-29 18:28 CT — merged to main (`fbf7f29`, --no-ff) at Divyam's request and pushed; branch deleted, live on GitHub Pages. Client-only, no Worker deploy needed (Claude Code)

### FIX-007 · Zoning data: include what can and can't be built

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

The zoning data shown with a permit/parcel should say what the zoning district actually allows and prohibits — permitted uses, prohibited uses, and key limits (units, height/FAR where available) — not just the district code.

**Checklist:**
- [ ] Source Chicago zoning district boundaries and an allowed/prohibited-use table per district (City data portal / zoning ordinance)
- [ ] Map each permit/parcel's district code to its permitted and prohibited uses
- [ ] Display "can build / can't build" summary wherever zoning is shown (permit detail, map popup)
- [ ] Note data vintage and add a disclaimer that the ordinance governs, mirroring existing data caveats
- [ ] Verify a sample of districts (RS-3, RT-4, RM-5, B, C, M) against the published ordinance

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)

### FIX-008 · Remember map layers and filters across page reload

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-31 10:58 CT
- **Tags:** Chicago Permit Search Tool

Map Search (`docs/map.html`) should persist the user's selected layers and filters (month, date range, GC job-count range, and future work-type/residential/value filters) so reloading the page restores the same view.

**Checklist:**
- [x] Inventory every layer toggle and filter setting on the map page
- [x] Persist them client-side (localStorage, consistent with the existing chi_permit_theme pattern) on every change
- [x] Restore persisted state on load before first render; fall back to defaults when absent or invalid
- [x] Handle stale state gracefully when saved filters reference months/shards that no longer exist
- [x] Verify across reloads, new tabs, and after a daily data refresh

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)
- 2026-07-30 18:10 CT — in-progress. INVENTORY FIRST, and it changed the job: the filters and layers this ticket asks for ALREADY persist, shipped 2026-07-20 under `chi_permit_map_settings` and `chi_permit_map_layers`. Drove the page and diffed state across a reload — every control (date from/to, GC min/max, neighborhood, query, radius) and every layer toggle (permits, clusters, heat, zoning, TIF) survived. Stale and corrupt saved state also already degrade cleanly: future date ranges, reversed ranges, non-numeric GC bounds, wrong types throughout, and a corrupt layers blob all came back with ZERO page errors and a live map. Checklist items 2 and 4 were already satisfied; rebuilding them would have been busywork (Claude Code)
- 2026-07-31 10:58 CT — done; final piece MERGED to main (`1d06dd9`, --no-ff) and live. The viewport was the only real gap, now saved on `moveend` under `chi_permit_map_view`. Two defects in that persistence, both fixed: the `moveend` saver was attached INSIDE the map's `load` handler, which waits on network tiles — so a pan before tiles finished was silently never recorded (tracing every write to the key showed ZERO saves and a null value); and the one-shot that stops a restored search query yanking the map back to its address was consumed by ANY render, including the first one that had no search location yet, so the suppression was spent before the geocode resolved. The second only became visible once the tiles were stubbed, because the unstubbed network was hiding it behind the first. Guard `t40-mapstate.js` went from 2/6 passing to green (Claude Code)
- 2026-07-30 18:10 CT — the one real gap was the VIEWPORT. Pan or zoom anywhere, reload, and the map threw you back to the whole-city default with your filters still applied — the part of "restores the same view" that was actually broken. Fixed on branch `fix-008-map-view` (`bb8cb8c`, pushed, NOT merged): saved on moveend under a new `chi_permit_map_view` key and used to CONSTRUCT the map rather than jumped to afterwards, so there is no lurch from the default. Validated on read — anything non-finite or out of range falls back, because a NaN reaching maplibre leaves a blank canvas with no error, which is worse than the default view (Claude Code)
- 2026-07-30 18:10 CT — also suppresses ONE re-centre at restore time: the saved search query is re-geocoded on load, and its easeTo would otherwise yank the map back to the address on every reload, so panning away from a searched address and reloading lost your position — the same bug wearing a different hat. That suppression had a real defect the tests caught: the map object is REBUILT on render, not only at page load, so arming the flag per construction re-armed it on every rebuild and stopped genuine NEW searches flying to the address. Now armed once per page load (Claude Code)
- 2026-07-30 18:10 CT — guard `t40-mapstate.js` covers all six behaviours and fails 2/6 against the pre-fix code. 111 client unit tests, 46/47 browser suites — `t14-live` is a pre-existing live-network flake (fails ~1 run in 3, exercises list sharing, nothing to do with the map). No ui-ux-pro-max pass: nothing visual was added or reworked, this restores position only. Awaiting merge approval (Claude Code)


### FIX-010 · Mobile: permit list scrolling locks up after opening permit details

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-07-30 16:45 CT
- **Tags:** Chicago Permit Search Tool

REOPENED 2026-07-30 — still happening on Divyam's phone after the first fix shipped. Exact steps: in a list under My Permit List, open the Permit View for the first permit; scroll down and back up inside the Permit View; close it. The list then will not scroll in either direction until the page is reloaded.

Original report: on mobile, after tapping into permit details from My Permit List, scrolling the list gets locked up. Likely the detail overlay's body scroll-lock is not being released on every close path — worth checking all of them, including swipe/back-gesture closes and the new FEAT-025 card-stack navigation.

First fix (shipped, did not resolve it): the lock never locked. `body.modal-open { overflow: hidden }` could not reach the page scroller, because `html { overflow-x: hidden }` propagates to the viewport and makes html — not body — the document scroller. Replaced with a `position: fixed` lock on body pinned at the saved scroll offset.

Second fix (on branch): stop locking mobile at all. Below 641px the card is an opaque full-screen sheet, so there is nothing behind it to lock — and every mobile lock tried here has been the bug rather than the fix. Background panning is stopped at the input layer instead (`touch-action`), which removes nothing from the layout, so there is no scroller to tear down and none to restore. Desktop keeps a lock, moved onto `html` (the real page scroller).

**Checklist:**
- [x] Reproduce on a phone: open permit details from the list, close it each possible way (close button, backdrop, browser back, gesture), then try scrolling
- [x] Audit how the overlay locks body scroll (overflow hidden, position:fixed, touchmove handlers) and every path that must release it
- [x] Release the lock on all close paths, including card-stack navigation and history popstate
- [x] Guard so a re-entrant open/close (fast taps) can never leave the lock latched
- [x] Verify on iOS Safari and Android Chrome viewports, and desktop regression
- [x] Reserve the scrollbar gutter so taking body out of flow does not shift desktop content sideways
- [x] Round 2: re-test on a real browser engine, not just Chromium — WebKit 18.5 at an iPhone 13 viewport
- [x] Round 2: prove what is NOT wrong after close (body static, no inline top, full document height, wheel and programmatic scrolling both work) to locate the failure outside the DOM
- [x] Round 2: remove the mobile lock entirely and stop background panning at the input layer instead
- [x] Round 2: keep pinch zoom working over the sheet (`touch-action: pinch-zoom`, not `none`)
- [x] Round 2: confirm on Divyam's iPhone — the failure is compositor-level and does not reproduce headlessly, so this cannot be closed from the test suite
- [x] Round 3: cancel the overlay's iOS scroll momentum before hiding it — CONFIRMED FIXED on device

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)
- 2026-07-29 17:05 CT — in-progress; reproduced headlessly at an iPhone 13 viewport (Claude Code)
- 2026-07-29 17:30 CT — root cause found: the lock was inert, not un-released. `html { overflow-x: hidden }` propagates to the viewport, so `body { overflow: hidden }` never reached the page scroller — with the overlay open, `window.scrollY` still moved freely and `document.scrollingElement` was HTML/overflow-y:auto on both pages (Claude Code)
- 2026-07-29 18:00 CT — fixed on branch `fix-010-scroll-lock` (`fc6b181`, pushed, NOT merged — awaiting approval). position:fixed body lock pinned at scrollY; idempotent lock/release; release moved before `closePermitModal`'s early return; `scrollbar-gutter: stable` on html. New guards `t27-scrolllock.js` (24 cases, fails 24/24 against the bug) and `t28-uiux-lock.js` (ui-ux-pro-max pass). 111 client + 117 Worker unit tests and 17 browser suites green; shared overlay block byte-identical (Claude Code)
- 2026-07-29 18:00 CT — caveat carried forward: the iOS-Safari-only reproduction could not be confirmed on a real device; the headless build uses overlay scrollbars, so the desktop scrollbar-shift case is covered by CSS rather than by a test (Claude Code)
- 2026-07-29 18:05 CT — merged to main (`07469cd`, --no-ff) at Divyam's request and pushed; branch deleted, live on GitHub Pages. Client-only, no Worker deploy needed. Still wants a confirming pass on a real iPhone (Claude Code)
- 2026-07-30 14:35 CT — REOPENED by Divyam: still broken on his phone, with exact steps (scroll inside the Permit View, then close). Confirmed the fix is genuinely live — fetched `list.html` from GitHub Pages and it carries `body.modal-open { position: fixed ... }` — so this is a failed fix, not a stale deploy (Claude Code)
- 2026-07-30 14:55 CT — installed Playwright WebKit 18.5 (the npm installer stalls; downloaded the build zip directly and extracted it into the ms-playwright cache) and reproduced the user's exact flow on Safari's engine at an iPhone 13 viewport. NOT reproduced: after every close path body is `static`, no inline `top`, the document is full height, and both programmatic and wheel scrolling work. Also ran the same flow against the pre-fix tree for comparison. Conclusion: nothing observable in the DOM is left wrong, so the surviving state is in WebKit's async scrolling tree — the root scroller torn down when body left the flow and never handed back to touch (Claude Code)
- 2026-07-30 15:10 CT — fixed on branch `fix-010-mobile-scroll-2` (`062aa99`, pushed, NOT merged — awaiting approval). Mobile (<=640px) now has NO page lock: the card is already an opaque full-screen sheet, so there is nothing to lock, and background panning is stopped at the input layer with `touch-action: pinch-zoom` on the overlay / `pan-y pinch-zoom` on its scrollable body. Nothing leaves the layout, so there is no scroller to tear down. Desktop keeps a real lock, moved to `html`. Saved-scroll bookkeeping deleted. ui-ux-pro-max pass caught that a drag on the sticky card header would otherwise pan the page behind (state-preservation) — that is what the `touch-action` rules fix — and that `touch-action: none` would have killed pinch zoom (Claude Code)
- 2026-07-30 15:10 CT — guards: `t27-scrolllock.js` reworked to drive a REAL wheel (overflow:hidden blocks user scrolling but not `window.scrollBy`, so the old programmatic probe could not tell locked from unlocked) — 24/24, and 7 fail when the desktop lock is reverted; new `t36-webkit-scroll.js` runs the reported flow on WebKit and Chromium and pins the mobile contract. `_wheelprobe*.js` are the controls proving each probe can report success; one caught that Chromium swallows the FIRST wheel after the overlay closes, which reads exactly like the bug if you trust it. 111 client unit tests and 40/43 browser suites green — `t2`, `t6`, `t8b` fail identically before and after this change (stale, they call `openPermitModal(html)` from before the FEAT-025 card stack, which takes no arguments); worth a separate cleanup card (Claude Code)
- 2026-07-30 15:40 CT — Divyam tested the branch: the permanent lockup is GONE. The list now refuses to scroll for only a second or two after closing, then works. Progress, not done (Claude Code)
- 2026-07-30 15:55 CT — ruled out main-thread blocking: profiled the close with a 150-permit list at 6x CPU throttle and recorded ZERO long tasks, so nothing is janking. Remaining hypothesis is iOS scroll momentum — the reported steps insist on scrolling inside the permit view right before closing, and iOS keeps delivering a fling's deceleration to the scroller it started on, so closing mid-momentum leaves the page underneath swallowing touches until the tail runs out. A second or two is exactly that tail. Fix on the same branch (`f1c8244`): flip the overlay scroller's overflow off before hiding it (with a forced reflow between, or both flips coalesce into one recalc and nothing is cancelled) and restore it on open. t36 now reopens after closing and asserts the scroller came back (Claude Code)
- 2026-07-30 15:55 CT — DISCRIMINATING TEST for Divyam, cheaper than any further guessing: close the permit view WITHOUT scrolling inside it first. No pause = momentum confirmed. Same pause = momentum is not the cause and the next step is Safari Web Inspector over USB (Mac + cable, Settings > Apps > Safari > Advanced > Web Inspector), not a fourth guess (Claude Code)
- 2026-07-30 15:52 CT — CONFIRMED FIXED on Divyam's iPhone. Branch `fix-010-mobile-scroll-2` (`062aa99` + `f1c8244`) is ready but NOT merged — awaiting approval per the standing rule (Claude Code)
- 2026-07-30 15:52 CT — retro, at Divyam's request: (1) round 1 shipped a fix for a symptom that was never reproduced — the defect found was real but was not necessarily HIS bug, and "unconfirmed on the only platform where it occurs" belongs in the sentence that says the work is done, not in a log line; (2) his two symptom reports each eliminated more than an hour of headless work, so ask for discriminating detail (does it recover? how long? what did you do immediately before?) BEFORE writing code; (3) nine months of iOS bugs had been verified on Chromium at an iPhone viewport, which is not Safari — real WebKit is now installed; (4) the winning move was proving what was NOT wrong, which located the failure outside the DOM; (5) the ladder question "should this mechanism exist at all?" would have skipped two rounds — mobile never needed a scroll lock. Written to Claude's long-term memory as `unreproduced-is-unfixed` (Claude Code)
- 2026-07-30 15:52 CT — also fixed the three permanently-red browser suites (t2, t6, t8b) that had been hiding regressions. Single root cause was drift in the shared `_boot.js` launcher: it waited on `typeof state !== "undefined"` instead of `body[data-ready]`, so init's async tail clobbered every seed; saved-list seeding also now needs `state.lists` + `activeListId` AND `showList()` to unhide the list view, or rows render `hidden` and waitForSelector times out on a working page; and t2 still called `openPermitModal(html)`, argument-less since FEAT-025. Verified they fail when the fix is reverted. 43/43 browser suites and 111 unit tests green. NOTE: `verify-tmp/` is gitignored, so the entire browser suite is untracked and lives on one machine — worth its own card (Claude Code)
- 2026-07-30 15:10 CT — OPEN: this is fix attempt #2 and it is NOT confirmed on a real device. Test on the branch preview at https://raw.githack.com/dkaruri/chicago-building-permits-search/fix-010-mobile-scroll-2/docs/list.html (different origin, so the saved list will be empty there — add a couple of permits first). If it still locks up, the cause is not the page lock at all and the next step is a real Safari Web Inspector session over USB rather than a third guess (Claude Code)
- 2026-07-30 16:45 CT — MERGED to main (`0799285`, --no-ff) at Divyam's request and pushed; branch deleted. Client-only, no Worker deploy. Closed (Claude Code)

### FIX-016 · "Posting as" name in permit notes cannot be changed

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 19:25 CT
- **Updated:** 2026-07-29 19:51 CT
- **Tags:** Chicago Permit Search Tool

The "Posting as ___" line in the Notes area of a permit view (`docs/list.html`, `docs/index.html`) renders `localStorage.chi_permit_author` as plain text — no click handler, no input, no edit control. The value is captured by a one-time `prompt()` that only fires while the key is empty, so once it is set nothing in the permit view ever asks again. A typo in that name is permanent from that screen.

Reported by Divyam after entering the wrong name. The only workarounds today are a console one-liner or the Author field on List Details (which only exists if you own a list) — and **neither is available on a phone**, where most of this posting happens.

**Checklist:**
- [x] Make the name in "Posting as ___" an editable control in the permit view, on both pages
- [x] Update the label in place — re-rendering the card would discard an in-progress note draft
- [x] Keep the two pages identical; this markup is duplicated by design
- [x] Accessible: real control, named, keyboard-activatable, reachable on mobile
- [x] Decide what to do about posts already made under the wrong name (the Worker's PUT never reassigns `author`)

**Log:**
- 2026-07-29 19:25 CT — created and started at Divyam's request (Claude Code)
- 2026-07-29 19:41 CT — done on branch `fix-016-posting-name` (`381a1c1`, pushed, NOT merged — awaiting approval). The name is now a real `<button>` that re-prompts; the label repaints IN PLACE because re-rendering the card would rebuild the note textarea and discard an unposted draft (guarded by `t34-posting-name.js`). Cancel and whitespace-only input change nothing; the value is trimmed and capped at 40 to match the Worker. `postingName()` centralises a read that was previously an inline expression duplicated on both pages. Guards `t34-posting-name.js` and `t35-uiux-author.js`; 111 client + 117 Worker unit tests and 22 browser suites green; byte-identity held (Claude Code)
- 2026-07-29 19:41 CT — ui-ux-pro-max pass: 7.48:1 light / 8.96:1 dark, underlined so it does not rely on hue, Tab-reachable with a 2px focus ring, accessible name states the action and the current value. Inline-in-text targets are exempt from the 44px minimum (WCAG 2.5.8), so it overrides the global button sizing instead of growing a 44px box mid-sentence. **Three defects were invisible to the assertions and only showed in screenshots**: the focus ring sliced through the "Posting as" label, the label wrapped away from the name, and the global `button { width: 100% }` stretched it into a full-width block. All fixed (Claude Code)
- 2026-07-29 19:51 CT — merged to main (`03f8961`, --no-ff) at Divyam's request and pushed; branch deleted, live on GitHub Pages. Merged after FIX-004 and re-verified together on the merged tree — no interaction between them. Client-only, no Worker deploy needed (Claude Code)
- 2026-07-29 19:41 CT — last checklist item resolved as "leave them": posts already made keep the old name, because the Worker's PUT never reassigns `author`. Changing that would let anyone rewrite the byline on an existing post, which is worse than a stale name. Delete and repost is the intended route. If it becomes a nuisance, the narrow version is to allow it only for the post's own author within a short window — worth a separate card, not this one (Claude Code)

### FIX-023 · Permit view opens blank on My Permit List

- **Priority:** P0-Critical
- **Status:** done
- **Created:** 2026-07-31 16:11 CT
- **Updated:** 2026-07-31 16:19 CT
- **Tags:** Chicago Permit Search Tool

Tapping a permit in My Permit List opened the permit overlay with nothing in it. Live-only: every real permit that names a general contractor was affected, from the moment FEAT-034 shipped.

Root cause: `followUpGcName` read `row.general_contractors` as an array of `{name}` objects. The field is a pipe-delimited **string** everywhere in the product — that is what the Worker returns, what Socrata publishes, and what `contractorLinesHtml` has always parsed. `gcs.find` therefore threw, and because `permitDetailHtml` joins its section thunks, one throw emptied the entire card.

It shipped green because all three FEAT-034 guards (t44, t45, t46) invented the array-of-objects fixture, so the test suite agreed with the bug.

**Checklist:**
- [x] Reproduce against the live site (drove `list.html#s=PeeXTko`, caught `TypeError: gcs.find is not a function`)
- [x] Trace to the source rather than guarding the render loop
- [x] Correct the fixtures in t44/t45/t46 to the real pipe-string shape, and confirm they now fail
- [x] Fix `followUpGcName` to parse the real shape
- [x] Verify end-to-end with a real row fetched from the live Worker
- [x] Confirm `index.html` is unaffected (its `followUpToggleHtml` is a deliberate no-op stub)
- [x] Full regression: 54 browser scripts, 128 client + 158 Worker unit tests

**Log:**
- 2026-07-31 16:11 CT — found while starting FIX-022; Divyam reported the permit view opening blank (Claude Code)
- 2026-07-31 16:11 CT — fixed on branch `fix-023-permit-view-empty` (pushed, NOT merged — awaiting approval). Client-only, `docs/list.html`; no Worker deploy needed. **Lesson: the three guards written for FEAT-034 all used a fixture shape that exists nowhere in the product, so a feature that crashed on every real permit passed its own tests. A fixture is a claim about production data and has to be checked against it** (Claude Code)
- 2026-07-31 16:19 CT — merged to main (`b6d8288`, --no-ff) at Divyam's request and pushed; branch deleted. Re-verified on the merged tree against a live row before pushing. Client-only, live on GitHub Pages once Pages rebuilds (Claude Code)

### FIX-022 · Desktop: "Read more" link opens GC/Open Sub view instead of the whole area being clickable; GC View shows full names with actions right-aligned

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-30 15:41 CT
- **Updated:** 2026-07-31 18:10 CT
- **Tags:** Chicago Permit Search Tool

Two desktop problems around GC/Open Sub rows. (1) In the Permit View, the WHOLE General Contractor area (and likewise the whole Open Sub area) is currently the click target that opens the GC View / Open Sub View (FEAT-025 card stack). Replace that: add a clearly clickable "Read more" text on the RIGHT of the GC/Open Sub row that navigates to the respective view, and make the rest of the area inert for navigation — so the name and details can be highlighted/selected/copied freely without accidentally opening the card. (2) Inside GC View, long names truncate to "…"; display names in full (wrap, don't clip), and move the per-row actions (Call, Add to list) to be right-aligned so full names have the row width to breathe.

**Checklist:**
- [x] Permit view: add a "Read more" clickable text on the right of the General Contractor area that opens the GC View; remove the whole-area click target so the name/details are freely selectable
- [x] Same for Open Subs: "Read more" on the right of each Open Sub area opens the Open Sub view; the rest of the area no longer navigates
- [x] "Read more" is an obvious affordance (link-styled, keyboard-accessible, focus ring) and announces where it goes (accessible name like "Read more about <name>")
- [x] GC View: remove the "…" truncation on names — render them in full, wrapping to multiple lines when long
- [x] GC View: right-align the Call and Add-to-list actions on their rows; keep alignment consistent across rows as names wrap
- [x] Check the same rows on narrow/mobile widths — this ticket targets desktop, so mobile behavior must not regress (tap-to-open, truncation rules, and tap targets there stay as designed)
- [x] Verify with hostile cases: very long company names, names with no spaces, 4-digit counts, and both themes
- [x] Owner ("owner as general contractor") rows go through the same hydration — they got the same treatment, and the "No profile on file" note still sits under the name rather than beside the link

**Log:**
- 2026-07-30 15:41 CT — created (Divyam)
- 2026-07-30 16:06 CT — reworded by Divyam: rather than making the name text selectable within a clickable area, replace the whole-area click target with a "Read more" link on the right of the GC/Open Sub row that opens the respective view; applies to both GCs and Open Subs. GC View full-name + right-aligned actions half unchanged (Claude)
- 2026-07-31 16:32 CT — in-progress on branch `fix-022-read-more`. Divyam chose ONE behaviour at every width: "Read more" is the only click target on desktop AND mobile, the row itself never navigates (so the name is selectable on a phone too). Design-time `ui-ux-pro-max` pass done — 44px target, focus ring, descriptive accessible name, wrap-over-truncate (Claude Code)
- 2026-07-31 18:01 CT — done: `53cae02` on branch `fix-022-read-more`, pushed, NOT merged (awaiting approval). Client-only, `docs/index.html` + `docs/list.html` patched identically; no Worker deploy needed. The GC View header keeps the stacked layout on desktop via a new `contact-card` class, so the permit card's own header is untouched. Two things the ticket did not name and the build needed: a 66-character name with no spaces overflowed the row until `.ci-main` got `overflow-wrap: anywhere`, and the global `button { width: 100% }` made "Add all N to list" claim the whole row and wrap below Call (Claude Code)
- 2026-07-31 18:10 CT — merged to main (`fbd54fa`, --no-ff) at Divyam's request and pushed; branch deleted. Re-verified on the merged tree, then LIVE on GitHub Pages after the Pages build completed: permit B200480349 → "Read more about STEVE PEREZ & COMPANY INC" is a 44px target, the row does not navigate, the GC View name is unclipped and the actions sit right-aligned on one row. Zero page errors (Claude Code)
- 2026-07-31 18:01 CT — verified: t18 rewritten to assert the row does NOT navigate and the link is a 44px target right of the details with the right accessible name; t19 + t37 now drive the link. Both fail against the unfixed tree and pass against the fix. New `verify-tmp/_shotreadmore.js` covers desktop + iPhone 13 × light/dark with hostile names. Full regression green: 55/55 browser scripts, 128 client + 158 Worker unit tests. Link contrast measured 7.76:1 light / 8.61:1 dark (Claude Code)

### FIX-035 · Permit Map: remember every filter and exclusion across reload and page exit

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-05 10:33 CT
- **Updated:** 2026-08-05 10:33 CT
- **Tags:** Chicago Permit Search Tool

Reported by Divyam: the filters and exclusions set on Map Search (`docs/map.html`) are not remembered — leaving the page or refreshing loses them. Persistence has been claimed twice already, so **reproduce and inventory before writing anything**: FIX-008 covered the date/GC/neighborhood/radius controls, the layer toggles and the viewport (`chi_permit_map_settings`, `chi_permit_map_layers`, `chi_permit_map_view`), and FEAT-024's log says its work-type exclusions and property-use select persist and re-apply on first render. Something in that chain is either not saving, not restoring, or newer than the code that saves — FEAT-021's value range and FEAT-040's visited/called chips are the obvious candidates for having no persistence at all. Done when every control in the Filters drawer survives a reload and a full page exit, and the map that comes back matches the one that was left.

**Checklist:**
- [ ] Reproduce on the live site first and write the inventory in this task's Log: for EVERY control on the map (date from/to, GC min/max, neighborhood/street, radius, value range, work-type exclusions, property use, layer toggles, viewport, and FEAT-040's visited/called chips if it has landed) record save / restore / re-apply-on-first-render as three separate yes-or-no answers
- [ ] Fix the ones that fail, keyed into the existing `chi_permit_map_*` storage rather than a fourth parallel key
- [ ] Make restore APPLY, not just repopulate: a control that shows its saved value while the map ignores it is the worse bug, because it lies
- [ ] Cover exclusions specifically — they live behind a collapsed `<details>`, so a silently-dropped exclusion is invisible until someone counts the pins
- [ ] Degrade safely on stale/corrupt saved state (an excluded work type that no longer exists, a value range with min > max) — fall back rather than rendering an empty map
- [ ] One guard suite that drives every control, reloads, and asserts both the control state AND the rendered result set — asserting the input value alone would pass the "shows but doesn't apply" bug
- [ ] Verify on desktop and mobile, on a reload and on a genuine page exit and return

**Log:**
- 2026-08-05 10:33 CT — created (Divyam)

### FIX-036 · Permit Map: draw and label zoning-district boundaries so each district's extent is unmistakable

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-05 10:33 CT
- **Updated:** 2026-08-05 10:33 CT
- **Tags:** Chicago Permit Search Tool

On the Map Search zoning layer (`docs/map.html`, `docs/data/zoning.geojson`), where one district ends and the next begins is not clear. Divyam's example: an **RM-4.5** label appears in the middle of what reads as an **RS-3** area, with nothing showing how far the RM-4.5 actually extends. Each district polygon should carry a visible outline marking its exact border, with the district's own label attached to that outlined shape, so a small pocket of one zoning class inside another is obviously its own bounded area rather than a stray label. The data is already loaded — the same `zoning.geojson` FEAT-024's residential filter indexes — so this is a rendering job, not an ingestion one.

**Checklist:**
- [ ] Reproduce with Divyam's case: find an RM-4.5 polygon surrounded by RS-3 and screenshot what it looks like today at the zoom where the confusion happens
- [ ] Add a distinct outline (line layer) per district polygon so boundaries read at a glance; make sure neighbouring same-class districts do not merge visually into one blob
- [ ] Bind the label to its polygon so the text belongs to the outlined shape — one label per district, placed inside it, not floating between two
- [ ] Handle small polygons and dense downtown areas: labels must not collide, disappear entirely, or spill outside the district they name
- [ ] Check legibility over the permit pins, clusters and heat layers in BOTH themes — the outline must not fight the markers it sits under
- [ ] Check zoom behaviour: outlines and labels should stay useful zoomed out and not clutter zoomed in
- [ ] Verify performance — this is a large polygon set; measure render/pan cost before and after rather than assuming it is free
- [ ] Verify on desktop and mobile, and confirm the zoning layer toggle still turns everything (fill, outline, labels) on and off as one unit

**Log:**
- 2026-08-05 10:33 CT — created (Divyam)

### FIX-034 · Attach permit notes to the permit's General Contractors and Open Subs as well

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-05 09:50 CT
- **Updated:** 2026-08-05 09:50 CT
- **Tags:** Chicago Permit Search Tool

Every note attached to a permit should also attach to that permit's General Contractors and Open Subs, so the note is reachable from the contractor side, not just the permit side. Builds directly on FEAT-034's notes infrastructure (`GET /api/notes/bulk`, note timestamps) and overlaps with FEAT-037's roll-up model (a GC's notes = notes on their permits + notes written directly on the GC) — extend that association to Open Subs too, and coordinate the two rather than building parallel plumbing. The association should ride the same normalized contractor-name key the rest of the app uses.

**Checklist:**
- [ ] Decide the association mechanics with FEAT-034/FEAT-037's data layer: when a note is created (or already exists) on a permit, make it queryable by each GC and each Open Sub named on that permit — roll-up by contractor key, not a copied/duplicated note
- [ ] Backfill: existing permit notes become visible from their permits' GCs and Open Subs, not just notes written from now on
- [ ] Surface them in the GC View and the Open Sub View (Notes section per FEAT-037: text, timestamp, author, and which permit each note came from, newest first)
- [ ] Respect FEAT-034's visibility rules (public thread posts vs. private notes; on shared lists show public + your own private ones) — attaching to a contractor must never widen who can see a note
- [ ] Handle multi-contractor permits: a note on a permit with 2 GCs and 3 Open Subs appears under all 5, clearly attributed to the one permit
- [ ] Keep it consistent on both index.html and list.html card stacks
- [ ] Verify on desktop and mobile: a contractor with notes across several permits, a contractor with none (no empty section/zero badge), and both themes

**Log:**
- 2026-08-05 09:50 CT — created (Divyam)

### FIX-006 · Shared permit-list link should layer over the directory with a back button

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 16:12 CT
- **Updated:** 2026-07-27 16:12 CT
- **Tags:** Chicago Permit Search Tool

When My Permit List is opened from a shared link, the Search Directory renders above the permit list instead of the list taking over the view. Arriving via a link should land directly on the permit list as its own layer, with a Back control returning to the directory — matching how the list behaves during normal in-app navigation.

**Checklist:**
- [ ] Reproduce by opening a generated share link in a fresh session (and in a new browser/incognito)
- [ ] Determine why the directory renders above the list on link entry (initial view state, render order, or restored last-viewed list from FEAT-016)
- [ ] Make link entry open the permit list as the active layer, directory hidden behind it
- [ ] Add a Back control to the directory, consistent with normal navigation
- [ ] Ensure browser back also returns to the directory rather than leaving the site
- [ ] Verify on desktop and mobile, and confirm normal (non-link) navigation is unchanged

**Log:**
- 2026-07-27 16:12 CT — created (Divyam)

### FIX-009 · Viewer count on a list is inaccurate across reloads and mobile app switches

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-08-03 16:12 CT
- **Tags:** Chicago Permit Search Tool

The number of people viewing a shared list can be wrong after reloading the page or moving between apps on mobile — reloads appear to double-count, and backgrounded mobile sessions appear to linger (or drop) incorrectly.

**Checklist:**
- [x] Reproduce both cases: rapid reloads inflating the count, and app-switching on mobile leaving a stale viewer
- [x] Review how presence is tracked (Worker-side) — connection lifetime, heartbeat, TTL
- [x] Key presence to a stable per-browser session id so a reload replaces rather than adds a viewer
- [x] Handle visibilitychange/pagehide/bfcache so backgrounded and restored tabs update presence correctly, with a TTL sweep for clients that vanish without notice
- [x] Verify count stability across reloads, app switches, tab closes, and multiple real viewers
- [x] Keep a cached pre-fix page working against the new Worker (deploy-order safety)
- [x] Merge to main
- [x] Deploy the Worker and confirm live

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)
- 2026-08-03 15:23 CT — started; status → in-progress (Claude Code)
- 2026-08-03 15:49 CT — ROOT CAUSE, one line: `presence()` returned `this.ctx.getWebSockets().length`. Presence was a count of SOCKETS, and a socket is not a person. Three separate symptoms fall out of that one fact, which is why the card reads as three bugs. (1) Reload — the browser opens the new socket before the old one's close reaches the room, so one person is two viewers for as long as the teardown takes. (2) Mobile app switch — iOS freezes the tab and the socket is never closed cleanly, so a viewer who left counts forever; nothing anywhere in the room had a heartbeat or a TTL. (3) `webSocketClose` recomputed presence while the departing socket was STILL in `getWebSockets()`, so even a clean exit reported one viewer too many. Reproduced all three against a real `ListRoom` under `wrangler dev` before changing anything (Claude Code)
- 2026-08-03 15:49 CT — fix: presence is a set of SESSION ids, not a socket count. New pure `worker/src/presence.js` (`presenceFrom`/`presenceKey`) so the logic is unit-testable — `list-room.js` imports `cloudflare:workers`, which `node --test` cannot load, and that is exactly why this logic had no tests before. `ListRoom` stamps each socket `{sid, author, seen, beats}`, counts distinct sids, and excludes the socket on its way out. A 30s client heartbeat refreshes `seen`; anything past a 90s TTL is closed and uncounted. The sweep runs lazily on any message rather than on an alarm — a remaining viewer's own heartbeat is what corrects the count for everyone, so there is no server timer and no compute burned on an empty room. Presence frames only broadcast when the count or names actually change, so the heartbeat does not spam the room (Claude Code)
- 2026-08-03 15:49 CT — client (`docs/list.html`): session id lives in **sessionStorage**, not localStorage. That is the whole point — it survives a reload and dies with the tab, so a refresh REPLACES the viewer while two genuinely open tabs are still two viewers. localStorage would have merged two real people at one desk into one. Plus: heartbeat while connected, `pagehide` closes the socket immediately (the only unload event iOS fires reliably, and it precedes a bfcache freeze), and `visibilitychange`/`pageshow` reconnect without waiting out the exponential backoff (Claude Code)
- 2026-08-03 15:49 CT — caught a deploy-order hazard that would have been self-inflicted: a NEW Worker facing an OLD cached page would have swept it every 90s, because the old client cannot heartbeat — the fix would have looked like a disconnect bug on exactly the mobile users this card is about. The sweep is now opt-in (`beats`), set only when the client supplied a real sid. A pre-fix page gets a synthetic id, counts as one viewer, and is never reaped. **Deploy the Worker first**, then the client (Claude Code)
- 2026-08-03 15:49 CT — verified. 173 worker unit tests (8 new in `presence.test.mjs`); 65/65 browser suites green, including the existing presence-pill guard t12. New `verify-tmp/t56-presence-lifecycle.js` proves the client half on desktop AND iPhone 13 — sid present and unchanged across a real `page.reload()`, a ping on the 30s interval (fired via a captured interval rather than waiting 30s), socket closed on pagehide, exactly one new socket on resume — and it FAILS against pre-fix `list.html` on four of those. `verify-tmp/_fix009-room.js` drives a real `ListRoom` under `wrangler dev`: reload=1, two sessions=2, departing peer drops, a quiet client swept after the real 90s TTL, legacy client left alone; 5 of its 6 assertions fail against the pre-fix room. Branch `fix-009-presence-accuracy` (`995623b`), pushed, NOT merged — awaiting merge approval and a Worker deploy (Claude Code)

- 2026-08-03 15:54 CT — MERGED to main (`6f6118a`, --no-ff), branch deleted. The client half is live on Pages; **the fix does nothing until the Worker is deployed**, which is Divyam's to run. Benign either way — the new client's `sid` and `ping` are simply ignored by the old Worker, so the count stays as wrong as it is today until the deploy, and nothing breaks (Claude Code)
- 2026-08-03 15:54 CT — caught at merge time: git reported `presence.js` as **Bin**, not text. It held a literal NUL byte — `presenceKey` joined names with a 0x00 instead of a space. Harmless (the key is only ever compared for equality, and all 173 tests passed either way) but corrupt source, and this repo has been bitten by invisible control bytes three times. Repaired in `4075a09`; the committed blob was verified clean by reading it back out of git rather than trusting the write. Worth recording that the TESTS COULD NOT have caught this — only the `Bin` in the merge stat did (Claude Code)
- 2026-08-03 15:54 CT — swept all 316 tracked source files for NUL/backspace bytes while there. One other hit, pre-existing and unrelated to this card: `worker/src/closure.js:156` writes a word-boundary `404` guard with two REAL backspace bytes instead of escapes, so `isKeyMissingError` tests for a literal backspace and can never match on the 404 path. It fails in the SAFE direction (it under-detects "key missing", so the closure seed treats an absent key as an error rather than as a first-run baseline — it will not wipe the accumulated observations), and the second `/key .*not found/i` check may cover it in practice. NOT fixed here — out of scope for this card, reported to Divyam (Claude Code)
- 2026-08-03 16:12 CT — DEPLOYED and VERIFIED LIVE. `chi-permits-api` version `854d2f4c-888b-47b4-b8ab-e67b47fa8aa9`, bound to the PRODUCTION KV `ef1c7094...` (not the preview id). `verify-tmp/_fix009-room.js PeeXTko prod` passes all six assertions against the deployed Worker over `wss://`, including the real 90-second sweep: reload=1, two sessions=2, departing peer drops, quiet client swept, legacy client untouched. Pages is serving the new client (7 hits for the new identifiers in the live `list.html`). Read the list back afterwards to confirm the probe mutated nothing — 99 permits, 0 ticks, title intact; the probe only ever sends hello/ping, never a patch. Status → done (Claude Code)
- 2026-08-03 16:12 CT — deploy gotcha worth keeping: `npx wrangler deploy` from `worker/` FAILED, and not because of the working directory. An earlier run from the repo ROOT had auto-scaffolded a `wrangler.jsonc` there with `assets: {directory: "docs"}`; wrangler walks UP the tree and prefers a root `.jsonc` over `worker/wrangler.toml`, so it tried to publish the 26.8 MiB `open_permits.json` as a Worker asset and aborted. Nothing was deployed and no stray Worker was created. Use **`npx wrangler deploy --config wrangler.toml`** from `worker/` — the bare form has been quietly wrong in this repo since that file appeared. The same failed run also deleted-by-scaffolding into `.gitignore`; all of it (stray config, root `.wrangler/`, the `.gitignore` block) has been cleaned up (Claude Code)

### FIX-011 · Permit view: show the actual neighborhood name, not just a number

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 12:11 CT
- **Updated:** 2026-07-30 20:00 CT
- **Tags:** Chicago Permit Search Tool

The neighborhood shown in the permit view is a bare number — most likely the dataset's community area code. Chicago has 77 named community areas (e.g., 22 → Logan Square); the view should display the real name, with the number at most as secondary detail.

**Checklist:**
- [x] Confirm which field the number comes from (community area vs. ward vs. census tract) in the permit data
- [x] Add the official community-area number → name mapping (77 areas, from the City data portal) to the pipeline or as a static lookup
- [x] Display the neighborhood name everywhere the number currently shows (permit view, list rows, map popups, exports)
- [x] Fall back gracefully when the code is missing or unrecognized (show the raw value, never blank)
- [x] Verify a sample of permits across different areas against the City's community area map

**Log:**
- 2026-07-29 12:11 CT — created (Divyam)
- 2026-07-30 19:55 CT — CONFIRMED the field: it IS `community_area`, a bare code 1-77, not ward or census tract — checked against live rows where all three appear side by side and differ (permit 101046020: community_area 1, ward 49, census_tract 10202). The permits dataset carries no name for it anywhere, so the lookup has to live client-side (Claude Code)
- 2026-07-30 19:55 CT — mapping sourced from the City's Community Areas boundary set `igwz-8jzy`: all 77, codes asserted contiguous 1-77 at build time. Static table rather than a fetch — these codes have been stable for decades and a row should not wait on the network to be labelled. READING the generated list caught two the City stores awkwardly: MCKINLEY PARK naively title-cases to "Mckinley Park", and 76 is stored as `OHARE` with NO apostrophe, which my correction map missed on the first pass because it was keyed on "O'hare". Both correct now and pinned by the guard (Claude Code)
- 2026-07-30 19:55 CT — every surface that showed the bare code now resolves it: permit overlay on both pages, map detail sheet on all three, map result rail. Exports carried no neighborhood AT ALL, so they gain the name (a bare code in a spreadsheet would be worse than nothing). The map's neighborhood filter now matches on the NAME too — typing "Logan Square" previously matched nothing because only the code was in the haystack; the code still matches, so nothing is lost (Claude Code)
- 2026-07-30 19:55 CT — fallbacks are deliberate: unknown codes, 0, null, empty, junk and already-named values all pass through as the RAW value. Never blank, and never an invented name — a confidently mislabelled neighborhood is worse than a number the reader can look up (Claude Code)
- 2026-07-30 19:55 CT — verified against real ADDRESSES, not just the mapping: 22 Logan Square (Humboldt/Diversey/Dickens), 32 Loop (233 S Wacker), 6 Lake View (Broadway/Newport), 41 Hyde Park (Drexel/Blackstone), 76 O'Hare (Bessie Coleman Dr — literally at the airport). Built on branch `fix-011-neighborhood-names` (`fba05ce`, pushed, NOT merged). Guard `t42-neighborhood.js` covers the table, every display surface and all six fallback shapes across all three pages, and fails against the pre-fix code. 111 client unit tests, 49/49 browser suites, lookup byte-identical across the three pages. Awaiting merge approval (Claude Code)
- 2026-07-30 20:00 CT — MERGED to main (`3b34a95`, --no-ff) and pushed; branch deleted. Client-only, no Worker deploy needed — live on Pages. Closed (Claude Code)

### FIX-012 · GC "average processing days" should measure average time to close a permit

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 12:44 CT
- **Updated:** 2026-08-03 11:57 CT
- **Tags:** Chicago Permit Search Tool

For General Contractors, the "average processing days" stat currently measures application-to-issuance time (the dataset's processing_time). What Divyam wants shown is how long the GC takes to CLOSE a permit on average — issuance to completion/closure. This is a metric definition change, not just a relabel.

**Checklist:**
- [x] Identify the right closure signal in the permit data (completion/closed date, status transition out of ACTIVE) and note coverage/quality in this task's Log
- [x] Compute average issuance→closure days per GC in the pipeline, excluding still-open permits, and export it — by OBSERVATION across seeds; not derivable retroactively (see Log)
- [x] Replace the processing-days stat on GC profiles/cards with the new metric, labeled clearly (e.g. "Avg time to close a permit")
- [x] Decide whether app→issuance processing days stays as a secondary stat or is dropped; keep sort options consistent — KEPT, relabelled "days to get issued" (it measures the permit desk, not the builder); both are sort options
- [x] Handle GCs with no closed permits (show n/a, never 0) — the pill is ABSENT, and the directory column shows an em dash
- [x] Verify a sample of GCs by hand against their permit histories

**Log:**
- 2026-07-29 12:44 CT — created (Divyam)
- 2026-07-30 16:55 CT — in-progress. DATA FINDING: **there is no closure DATE anywhere in the City's published data**, so issuance-to-closure cannot be computed retroactively at all. Checked exhaustively: (a) `ydr8-5enu` has 122 columns and exactly four are date/status related — `application_start_date`, `issue_date`, `processing_time`, `permit_status`; there is no completion, closed, final or expiry date. (b) `permit_status` DOES carry COMPLETE (462,083 rows) so closure is knowable as a STATE, but the dataset is a snapshot and never records WHEN the state changed. (c) Socrata's row-level `:updated_at` is not a substitute — sampled COMPLETE permits issued in 2020 all carry `2025-10-14T20:58-21:00Z`, seconds apart: that is a bulk re-upload timestamp, not a status change. (d) No inspections dataset links permits to a final inspection date; the only permit-adjacent sets are violations and issuance-side "time to issue" performance metrics. (e) `dmcg-xwb8 "Building Permits Search"` is a non-tabular search view, not queryable (Claude Code)
- 2026-07-30 16:55 CT — measured the computable substitutes on real GCs across all 15 contact slots (an earlier pass using only `contact_1_name` was wrong — it returned rows whose status is null, and the app matches every slot). BEAR CONSTRUCTION COMPANY: 2,890 permits, 2,263 COMPLETE of 2,626 decided = **86.2% completion rate**, 147 open averaging **642 days old** (median 577, oldest 2,050). BULLEY & ANDREWS: 1,387 permits, 834 of 1,016 = **82.1%**, 129 open averaging **469 days** (median 420, oldest 2,030). Both are exact and honest; neither is a duration-to-close (Claude Code)
- 2026-07-30 16:55 CT — asked Divyam which metric should replace the stat. He pushed back asking whether open-to-close time can simply be computed for all jobs — it cannot, for the reason in (b) above: the data records THAT a permit closed, never WHEN. The only route to the true metric is to start observing it: log the date each permit is first seen COMPLETE on each seed, and compute issue -> first-seen-COMPLETE from then on. That yields real closure times going forward, accurate to the seed cadence, but covers no permit that closed before we started watching. Awaiting his decision (Claude Code)
- [x] Run `npm run seed` — FIRST run done 2026-07-30 17:32 CT (baseline established)
- [x] Run `npm run seed` a SECOND time — done 2026-07-30 17:55 CT (booked 0, only 6 min after the baseline); the daily CI seed has booked real observations every run since
- 2026-07-30 17:20 CT — built on branch `fix-012-close-time` (`ecba9d5`, pushed, NOT merged). Divyam chose "open-job age now + start observing closures". New `worker/src/closure.js` + 9 unit tests. Open-job age is exact and computed from permits the seed already fetches. Time-to-close is OBSERVED: each seed snapshots the open set, and a permit that has left it and now reads COMPLETE books issue_date -> observation date. EXPIRED/CANCELLED are excluded — stopping is not finishing, and counting them would flatter slow builders. Stats stored aggregated per contractor ({n, days}) so KV stays bounded by contractor count rather than growing with every permit that ever closes. Snapshot is written LAST so a partial upload re-detects the same closures next run instead of losing them (Claude Code)
- 2026-07-30 17:20 CT — contractors with no observations get NO close keys, so the pill is absent rather than 0; for months that will be nearly everyone, and 0 would read as "closes same day" — the exact confusion this ticket was raised about. Directory column shows an em dash. Verified a hostile render at 390px in both themes: pills wrap, nothing clipped. Adds the first KV READ the seed has ever needed, with the same `--remote` requirement as the writes — without it wrangler reads local Miniflare, every run looks like the first, and no closure ever accumulates. 136 Worker + 111 client unit tests, 46/46 browser suites, overlay block byte-identical (Claude Code)
- 2026-07-30 17:20 CT — NOT DONE until seeded TWICE: run one writes `closure:open_snapshot` and establishes the baseline (no close times yet); run two is the first that can observe a closure. Open-job age appears after the first seed. Awaiting merge approval (Claude Code)
- 2026-07-30 17:35 CT — MERGED to main (`1fe7197`, --no-ff) and branch deleted. Baseline seed run: `closure:open_snapshot` and `closure:stats` written to remote KV, and the step reported exactly what it should — "no previous snapshot — this run establishes the baseline", "close-time now known for 0 GCs and 0 subs". 40,593 open permits snapshotted (Claude Code)
- 2026-07-30 17:35 CT — verified at the destination, and the numbers match an INDEPENDENT measurement made straight from Socrata before any of this was built: Bear Construction 147 open, age avg/median/max 642/577/2050; Bulley & Andrews 129 open, 469/420/2030. Identical to the figures logged at 16:55. `close_days_avg` is absent on both, which is correct at baseline, and principals from FIX-015 are intact. Open-job age is LIVE (Claude Code)
- 2026-07-30 17:35 CT — STAYS in-progress deliberately: the observed close-time path has not yet been proven end-to-end, because no permit has closed while we were watching. It closes when a second seed books its first observation (Claude Code)
- 2026-08-03 11:57 CT — **DONE — the observation path is proven end-to-end and the metric is LIVE.** The condition this card was held open for has been met: closures are being booked. The second seed (2026-07-30 17:55 CT, `workflow_dispatch`) booked 0, which is correct — it ran six minutes after the baseline, so nothing had closed in between. The daily CI seed has booked real observations on every run since. Read straight from remote KV: `closure:stats` now holds 59 general contractors (86 observations) and 140 open subs (224 observations), every one with a non-zero `{n, days}` (Claude Code)
- 2026-08-03 11:57 CT — verified at the destination, both branches, on the deployed site rather than a fixture. `/api/contact/SUNRUN INSTALLATION SERVICES` returns `close_days_avg: 71, close_sample: 12`, and the arithmetic matches KV exactly (854/12 = 71.2 → 71); PEERLESS ENTERPRISES 2773/7 = 396.1 → 396. Rendered headless against production `index.html`: SUNRUN's card shows **"closes in ~71 days (12 seen)"**. BEAR CONSTRUCTION COMPANY has no observations yet and shows **no close pill at all** — absence, not a zero, which is the specific confusion this ticket was raised about. Open-job age is on both cards (SUNRUN 345d, Bear 646d; Bear was 642d on 07-30, four days of ageing, consistent) (Claude Code)
- 2026-08-03 11:57 CT — the fixtures in `verify-tmp/t39-closetime.js` were checked against a REAL production payload rather than trusted on their own: same field names, same shape, same absence semantics. t39 passes on both pages (close pill present with sample, absent without, directory column em dash, old stat relabelled "days to get issued"); `worker/test/closure.test.mjs` 11/11 green (Claude Code)
- 2026-08-03 11:57 CT — the 2026-08-01 scheduled seed FAILED and it cost nothing, which is the design working. It died in the Socrata fetch (`ConnectTimeoutError`, 10s connect) BEFORE any KV write, so `closure:open_snapshot` was never advanced; the 08-02 run compared against 07-31's snapshot and re-detected every closure in the gap. Only the precision of "which day we noticed" slips by a day, never the sample — the issue date is read from the snapshot, not the row. No action needed (Claude Code)
- 2026-08-03 11:57 CT — one caveat worth recording for whoever reads these numbers: many contractors carry near-identical 396/397-day observations, because a large batch of permits issued around 2025-07-02 left the open set in the same seed. That is honest — the metric is accurate to the seed cadence by construction — but early averages are dominated by whenever the City last swept statuses, not by builder speed. It washes out as samples accumulate; the `(n seen)` sample size is on the pill precisely so a small n reads as a small n (Claude Code)


### FIX-013 · Desktop: tag chips at the top should size to their text, not the list width

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 13:11 CT
- **Updated:** 2026-07-31 10:58 CT
- **Tags:** Chicago Permit Search Tool

On desktop, the tags listed at the top stretch to the width of the list/container instead of hugging their text. Each tag should be an inline pill sized to its content (fit-content / inline-flex), wrapping naturally as a row of chips — not full-width blocks.

**Checklist:**
- [x] Locate the tag elements and identify why they expand (block-level display, width:100%, or a stretched flex/grid item)
- [x] Size each tag to its text with appropriate padding; lay the group out as a wrapping chip row
- [x] Confirm mobile/narrow layout is unchanged (or improved) by the change
- [x] Check hover/focus states and touch targets still meet the ui-ux-pro-max standard after resizing
- [x] Verify on desktop widths across the pages where these tags appear

**Log:**
- 2026-07-29 13:11 CT — created (Divyam)
- 2026-07-31 10:58 CT — done; MERGED to main (`ea2af41`, --no-ff) and live. Root cause was the global `button, input, select, textarea { width: 100% }` reset at the top of `docs/list.html` catching every `<button class="tag">` — measured 1039px on desktop and 348px on mobile, one chip per row. The sibling `<span class="tag">` chips were never affected, which is why only some pills looked wrong. Same trap as FIX-016's inline "Posting as" button: a button that is not a form control has to opt out of BOTH width and min-height. Fixed alongside a mojibake `::before` tick on selected chips (visible garbage on every pressed pill), now written as the CSS escape `\2713` so no future encoding round-trip can corrupt it. One fix covers FIX-019 too. Guard `t43-tagchips.js` (Claude Code)

### FIX-003 · Speed up permit removal in My Permit List and stop accidental opens

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 15:53 CT
- **Updated:** 2026-08-07 09:37 CT
- **Tags:** Chicago Permit Search Tool

Removing a permit from My Permit List (`docs/list.html`) is slow because of the confirmation step, and the remove tap sometimes opens the permit instead — the click appears to fall through to the row's open/detail handler.

**Checklist:**
- [x] Replace the blocking confirmation with immediate removal plus a short-lived undo
- [x] Stop the remove control from triggering the row's open action (stop event propagation on click and touch)
- [x] Verify rapid successive removals stay in sync with saved-list storage
- [x] Test on desktop and on a phone viewport, including the visited-checkmark and reorder controls nearby
- [x] Give the mobile remove control a hit-area halo so a near-miss is a no-op instead of an open
- [x] Stop the remove cell advertising itself as clickable now that it is inert

**Log:**
- 2026-07-27 15:53 CT — created (Divyam)
- 2026-08-07 09:14 CT — in-progress; branch `fix-003-fast-remove` (Claude Code)
- 2026-08-07 09:32 CT — done; `de22170` on `fix-003-fast-remove`, **pushed, NOT merged** (merges need Divyam's approval). Two separate causes under one card. **Accidental opens:** the `event.stopPropagation()` was on the BUTTON, but the whole `<td class="select-cell">` sits inside a `<tr onclick>` that opens the permit — measured 60×110 for the cell around a 44×44 button on desktop, so **62% of the remove cell opened the permit**, and `td.select-cell { cursor: pointer }` plus a hover highlight advertised the whole thing as the target. Reproduced first: clicks above/below/left/right of the button all opened the permit. The guard now sits on the cell, where every miss routes through, and the cursor/hover is scoped to the select cell that genuinely is clickable. The same row template ships on `index.html` and `map.html`, so all three are fixed, not just the page the ticket named. **Mobile** had no dead zone at all (cell == button, 44×44) — no margin for error instead; its 8px inset moved from `top`/`right` into `padding`, so the × renders in the same place but the cell absorbs an 8px halo (60×60). **Slowness:** `window.confirm()` per permit made clearing a route's worth of stops a dialog-per-tap. Removal is instant now, with a 12s Undo in the existing `#list-action-status` aria-live line (reused `.linkish`, no new DOM or CSS surface) that restores the permit at its **original stop number** — the list is a route, so position is data — with its note and edit time, through the same commit path the removal used. Undo is 50×44, tab-reachable in 4 hops, 7.48:1 light / 8.96:1 dark. Verified `verify-tmp/t65-fast-remove.js` desktop + iPhone 13, all green, with three mutants (cell guard removed / undo appends instead of restoring position / undo drops the note) all caught, plus a control proving the row body still opens the permit. 204/204 worker + 250/250 unit; t46, t47, t57, t59, t64 still green. A dark-mode contrast read of 2.32:1 was the known theme-transition race, not a real failure — 8.96:1 once settled (Claude Code)
- 2026-08-07 09:37 CT — **MERGED to main** (`4870547`, `--no-ff`) on Divyam's approval and pushed; Pages deploy triggered. Client-only change (`docs/*.html`), no Worker deploy needed. Merged tree re-verified before pushing: t65 all green, control-byte scan clean (Claude Code)

### FIX-001 · General bug and compatibility fixes

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Sweep the tool for general bugs and browser/device compatibility issues.

**Checklist:**
- [ ] Audit console errors across all pages (Search Directory, Permit Map, My Permit List)
- [ ] Test on Chrome, Safari, Firefox, and mobile browsers
- [ ] Fix issues found and note each in this task's Log
- [ ] Verify no regressions in search, map, and list flows

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FIX-018 · Label the visited checkbox column "Visited/Called" on desktop and mobile

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 15:55 CT
- **Updated:** 2026-07-31 13:41 CT
- **Tags:** Chicago Permit Search Tool

The visited checkbox on permits in My Permit List (`docs/list.html`) has no header label. Add a "Visited/Called" label at the top of the checkbox column so it is clear what checking it means, on both desktop and mobile layouts.

**Checklist:**
- [x] Locate the visited-checkmark column (FEAT-008) in the list's desktop and mobile layouts
- [x] Add a "Visited/Called" header label above the checkbox column on desktop
- [x] Add the same label on the mobile layout, keeping it legible without breaking the row layout on small screens
- [x] Keep the label consistent with the column in any shared-list/read-only view if the checkbox appears there
- [x] Verify on desktop and phone viewports that the label renders, aligns with the checkboxes, and doesn't overflow
- [x] Fix the thead/tbody column-order mismatch the visible label exposed (every header sat one column off)

**Log:**
- 2026-07-29 15:55 CT — created (Divyam)
- 2026-07-31 13:17 CT — status → in-progress; started work in chicago-building-permits-search (Claude Code)
- 2026-07-31 13:41 CT — implemented on branch `fix-018-visited-label` (`c6a52e7`, pushed). `docs/list.html`: the tick `<th>` now renders a visible "Visited/Called" (sr-only duplicate removed, `white-space: normal` so it can wrap at its `<wbr>` — `.saved-permits-table th` is nowrap above 640px); the cell's `data-label` carries the same text, which the mobile stacked-card layout prints via `::before` at 13.8px; the checkbox `aria-label` now says "visited/called". Shared/read-only lists render through the same `permitTable(..., move:true)` path, so they inherit it — there is no separate read-only renderer. (Claude Code)
- 2026-07-31 13:41 CT — DEFECT FOUND AND FIXED while verifying: `thead` emitted the tick header FIRST while the row emitted the tick cell THIRD (after remove and select), so every header in the saved-permits table sat one column off. Harmless-looking while the tick header was a bare ✓ over an empty remove header; with a real label it put "Visited/Called" over the remove (×) column. `thead` now follows the row order (remove, select, tick). (Claude Code)
- 2026-07-31 13:41 CT — verified headless at 1280px and iPhone 13 in light and dark (`verify-tmp/t47-visitedlabel.js`, 14 assertions; control run against the pre-fix code fails 5 of them). Screenshots reviewed at both viewports/themes. Full `list.html` browser suite (49 scripts) and 286 unit tests pass. Status → done. (Claude Code)
- 2026-07-31 13:39 CT — merged to `main` with user approval (`587f74d`, `--no-ff`); guard test re-run green on merged main, branch deleted local + remote, GitHub Pages deploy triggered. (Claude Code)
- 2026-07-31 13:47 CT — LIVE AND VERIFIED on the production Pages site: header reads "Visited/Called" at 1280px and on iPhone 13 (mobile label via `::before`), sits at the tick column's index and over the checkbox, zero page errors on both. (Claude Code)
- 2026-07-31 13:41 CT — NOTE, not fixed here (out of scope): every `<th>` in this table renders at 9.6px uppercase — below the 12px legibility floor. Site-wide table-header restyle, worth its own card. (Claude Code)

### FIX-021 · Desktop: make the list-header section (Starting Location through List Note) collapsible

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-30 15:13 CT
- **Updated:** 2026-07-30 15:13 CT
- **Tags:** Chicago Permit Search Tool

On desktop in My Permit List (`docs/list.html`), let the whole block from "Starting Location" down through "List Note" collapse and expand as one section, so the permit rows can take the screen when that header block isn't needed. A clear toggle opens it back up; the collapsed/expanded choice should persist with the existing last-view state so it survives reloads and list switches.

**Checklist:**
- [ ] Identify the exact block spanning Starting Location → List Note in the desktop layout (and what sits between them: route controls, filters, description, etc.)
- [ ] Wrap it in a collapsible section with a clear toggle (chevron + label), animated open/close, `aria-expanded` on the control
- [ ] Persist the collapsed state in last-view storage per list; default expanded
- [ ] Keep all controls inside fully functional when expanded (no lazy-render surprises), and make sure nothing inside is reachable by keyboard while collapsed
- [ ] Decide mobile behavior: leave mobile unchanged unless the same collapse is an obvious win there — this ticket only requires desktop
- [ ] Verify on desktop widths: collapse, expand, reload persistence, list switch, and no layout shift of the permit rows below

**Log:**
- 2026-07-30 15:13 CT — created (Divyam)

### FIX-019 · My Permit List: tag pills should hug their text, not span the list width

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-07-30 09:27 CT
- **Updated:** 2026-07-31 10:58 CT
- **Tags:** Chicago Permit Search Tool

On My Permit List (`docs/list.html`), the tag pills stretch to the full width of the list on both desktop and mobile. Each pill should take only the space its text needs plus padding (inline-flex / fit-content), wrapping naturally as a row of chips. Same pattern as FIX-013 (tag chips at the top, desktop) — keep the chip styling consistent between the two.

**Checklist:**
- [x] Locate the tag pill elements in `docs/list.html` and identify why they expand to full width (block display, width:100%, or stretched flex/grid item)
- [x] Size each pill to its content with appropriate padding; lay the group out as a wrapping chip row
- [x] Apply on both desktop and mobile layouts; keep touch targets adequate on mobile
- [x] Keep the styling consistent with FIX-013's chip treatment if that lands first (or share one fix and log it in both tasks)
- [x] Verify on desktop and phone viewports, on lists with few and many tags

**Log:**
- 2026-07-30 09:27 CT — created from Divyam's report (Claude)
- 2026-07-31 10:58 CT — done; same single fix as FIX-013, merged to main (`ea2af41`, --no-ff) and live. Both tickets were the same global `width: 100%` button reset in `docs/list.html`; see FIX-013's log for the full root cause (Claude Code)

### FIX-014 · GC view: Specialties counts hang outside their bubbles — keep the number inside like Associations

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-07-29 13:11 CT
- **Updated:** 2026-07-30 19:35 CT
- **Tags:** Chicago Permit Search Tool

In the General Contractor view, the numbers on Specialties bubbles overflow past the edge of the pill, while Associations renders its counts contained correctly. Make Specialties display its count inside the bubble the same way Associations does.

**Checklist:**
- [x] Compare the Specialties and Associations bubble markup/CSS and identify why one contains its count and the other overflows (absolute positioning, white-space, min-width, or padding differences)
- [x] Align Specialties to the Associations pattern — ideally share one bubble component/style for both
- [x] Check long specialty names and 3+ digit counts wrap or truncate gracefully
- [x] Verify on desktop and mobile in the GC overlay card, and anywhere else Specialties bubbles render

**Log:**
- 2026-07-29 13:11 CT — created (Divyam)
- 2026-07-30 19:30 CT — CAUSE: the pill was painted by `.pm-chiplist li > span:first-child` — the NAME element. Specialties put its count in a SIBLING span, so the number sat outside the bubble entirely. Associations escaped only because its name and count both live inside a `<button class="assoc">`, which carries the pill itself. Two structures, one positional selector, and only one of them matched it. Not padding or white-space (Claude Code)
- 2026-07-30 19:30 CT — fixed on branch `fix-014-specialty-chips` (`1e35d08`, pushed, NOT merged). Both lists now wrap name+count in ONE element that carries the pill, and the brittle positional selector is deleted so they cannot silently drift apart again. Long names wrap inside the chip instead of forcing it wider than the card; chip capped at 100% width. Verified with a 53-character specialty and a 4-digit count (1,284) at 390px — no horizontal scroll on page or overlay (Claude Code)
- 2026-07-30 19:30 CT — the screenshot caught what the assertions passed: I first used `align-items: baseline`, which put the count on the FIRST line's baseline so it floated alone in the top-right of a two-line chip — geometrically inside, visually detached, and a NEW inconsistency in a ticket about making two components consistent. Now `center`, matching `.assoc` (Claude Code)
- 2026-07-30 19:30 CT — guard `t41-chips.js` measures CONTAINMENT geometrically rather than asserting markup: it walks up to the nearest ancestor that actually paints a background and radius, checks the count's box is within it, and checks both lists paint the same pill (radius/background/border). Asserting the markup would pass even if the CSS drifted back, which is exactly how these two diverged. Against the pre-fix code it reports "no painted bubble" for every specialty count. 4 page/viewport combinations. 111 client unit tests, 48/48 browser suites, shared blocks byte-identical. Awaiting merge approval (Claude Code)
- 2026-07-30 19:35 CT — MERGED to main (`f5539c1`, --no-ff) and pushed; branch deleted. Client-only, live on Pages. Closed (Claude Code)

### FIX-015 · Show the person in charge of a GC company (and Open Sub LLCs/companies) everywhere they appear

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 14:07 CT
- **Updated:** 2026-07-30 18:10 CT
- **Tags:** Chicago Permit Search Tool

Wherever a General Contractor company shows up (directory rows, profile cards, permit detail, overlay cards, map popups, list rows, exports), display the name of the person in charge of that company. Same for Open Subs that are LLCs or companies: show the responsible person alongside the business name. Likely sources: the city contractor registry / licensing data already ingested (FEAT-004/FEAT-014 surfaced titles), and IL Secretary of State LLC registrations (manager/registered agent) — FEAT-029 covers deeper LLC ingestion (originally FEAT-026, consolidated 2026-08-06); this task uses whatever fields are available now and leaves richer enrichment to FEAT-029.

**Checklist:**
- [x] Identify where a "person in charge" name exists in current data (contractor registry contact/licensee name, permit contact fields) for GCs and for Open Sub companies; note coverage in this task's Log
- [x] Add the name to the pipeline exports so it rides the existing JSON indexes
- [x] Display it everywhere GCs appear: directory rows, GC profile/overlay card, permit detail contractor lines, map popups, CSV export
- [x] Same for Open Subs that are LLCs/companies, in all the same surfaces
- [x] Handle missing data honestly (omit the line rather than showing blank/unknown junk)
- [x] Verify a sample of well-known GCs and sub companies against the registry/SoS records
- [x] ADDED by Divyam 2026-07-30: show the unit owner's name and contact information on the permit view, alongside the GC's owner
- [x] Run `npm run seed` from `worker/` — the join happens at seed time, so nothing appears until then
- [x] Confirm on a real phone once seeded

**Log:**
- 2026-07-29 14:07 CT — created (Divyam)
- 2026-07-30 16:05 CT — in-progress. DATA FINDING, which overturns the task's premise: neither source this ticket names actually carries a person in charge. (a) The permits dataset's contact slots hold only name/type/city/state/zip — and the person-shaped names on a GC's permits are the OWNER contact, i.e. the GC's CUSTOMER. Sampled live: "ALL-RIGHT SIGN INC" pairs with owner Tim Leung, "LEBSKI CONSTRUCTION" with owner Michael Jerbich. Displaying those would confidently name the wrong human on every card. (b) The city licensed-contractor registry is a flat DataTable of licenseType/licenseNo/name/address/phone/expiry across all 6 scraped categories, 17,185 rows, no officer/agent column — and there is no per-licence detail page to scrape, so the existing scraper already takes everything it has. Person-named licensees are sole proprietors (~2% of GC-class) where the person IS the business name already shown, so they add nothing (Claude Code)
- 2026-07-30 16:05 CT — the field DOES exist in a third city dataset the ticket does not mention: **Business Owners (ezma-pppn)** — 329,725 rows, 319,616 with a named person, giving owner first/middle/last and owner_title (PRESIDENT, MANAGING MEMBER, SOLE PROPRIETOR, SECRETARY...) per business licence. Joined on the project's existing normalized-name key it covers 190,727 distinct businesses (Claude Code)
- 2026-07-30 16:05 CT — COVERAGE, measured with the shipped module against live data (not a throwaway script): **GCs 1,057/4,985 with open jobs = 21.2%, and 45.0% of the top 200 by open jobs** — the ones anyone actually scrolls. **Subs 119/993 = 12.0%, 20.0% of the top 200**; sub matches skew to sole proprietors, where person and business are the same name. Spot-checked leads: Frackiel Builders → Bonnie E. Frackiel (President), Bulley & Andrews → Paul R. Hellermann (President, +4 more), Bear Construction → James S. Wienold (President, +1). Remaining ~79% get no line at all, per the checklist's "omit rather than show blank junk" (Claude Code)
- 2026-07-30 16:05 CT — data half done on branch `fix-015-person-in-charge` (`c72004e`, pushed, NOT merged). New `worker/src/principals.js` + 7 tests; joined at SEED time in `seed-kv.js` on the existing normalized-name key, so every surface that renders a profile row inherits it with no extra client call — that is the whole point of doing it there rather than per-request. Company owners (e.g. "Marsh & McLennan Companies, Inc." as SHAREHOLDER) are dropped: not a person in charge. 48% of matched GCs list several owners, so titles are RANKED to make the lead name deterministic across rebuilds instead of dataset row order — that is what picks Bear Construction's President over its Secretary. Unmatched companies get no keys at all rather than empty ones, so the UI keys off absence. 124 Worker tests green (Claude Code)
- 2026-07-30 16:26 CT — display half done (`894f228`, same branch, pushed, NOT merged). Divyam extended the scope: the permit view must also name the UNIT's owner with contact information, not just the GC's. Both are in. The owner block is built from the permit's own contact slots — the same names identified above as the contractor's CUSTOMER — so they are labelled as the owner and kept out of the contractor blocks; t37 explicitly asserts an owner's name never shows up as a contractor's "Run by". Owner contact detail is thin because the source is thin and the UI says so plainly ("No phone published for owners") rather than implying a failed lookup; but owner lines reuse `.contractor-line`, so an owner who is also a licensed contractor (the 59k "owner as general contractor" permits) resolves to a real tel: link — that is the owner phone where one exists at all. Contractors gained "Run by <name> <title> +N more" on every permit view, a "Person in charge" block on the contractor card, the lead name on directory rows, and a Unit owner column in CSV. No new client fetch anywhere (Claude Code)
- 2026-07-30 16:26 CT — ui-ux-pro-max pass caught two real defects, both measured not eyeballed: the "Run by" label was 11px, and the NAME measured identical to its own label and title (6.32:1 for all three), so the line had no hierarchy on the one word that matters. The name now carries ink + weight (16.35 light / 16.1 dark). Then the SCREENSHOT caught what no assertion could — a blanket /api/contact fixture made the owner inherit the GC's principal and rendered "Run by" under UNIT OWNER; test-only, but it would have read as a product bug, so the fixture is name-aware now and the render was re-checked by eye. Guards `t37-principals.js` and `t38-uiux-principals.js`; 111 client + 124 Worker unit tests green (Claude Code)
- 2026-07-30 16:26 CT — NOTE for FIX-020: on this branch `t2`, `t27` and `t36` fail, because they are FIX-010 round-2 guards and this branch is cut from `main`, where FIX-010 is not merged. The suite is gitignored and therefore SHARED across branches instead of travelling with the code — concrete evidence for that card, not a regression here (Claude Code)
- 2026-07-30 16:05 CT — NEXT: the display half (checklist items 3-6) — GC/sub cards, directory rows, permit overlay, map popups, CSV — plus the ui-ux-pro-max pass. Pausing here per the standing confirm-before-each-phase rule. DEPLOY HAZARD: the join runs at seed time, so nothing appears anywhere until Divyam runs `npm run seed` from `worker/`; the seed now also pages 320k owner rows and takes correspondingly longer (Claude Code)
- 2026-07-30 16:45 CT — MERGED to main (`48015e0`, --no-ff) and production KV SEEDED at Divyam's request. Seed reported `Resource location: remote` on every write and matched **1,119/5,784 GCs and 1,421/7,441 subs** — subs landed far better than the 12% estimated off the stale `docs/data` export, because the live profile set is different. Verified at the destination rather than trusting "Done!": read three GCs back off the live API and got real principals with a fresh seeded_at (Claude Code)
- 2026-07-30 16:45 CT — that read-back immediately exposed two name-formatting defects no test had produced: "Allan E. Bulley, Iii" and "Michael W..D.. Sudol". Generational suffixes were being title-cased and pre-punctuated initials were having a period appended to every letter. Also found VANDERBILT-HOLLINGSWORTH becoming "Vanderbilt-hollingsworth", wrong in the original code too and never noticed. Fixed on branch `fix-015-name-formatting` (`9ea7551`, pushed, NOT merged — awaiting approval); "V" is disambiguated by position, since it is a suffix in "Henry Tudor V" and a middle initial in "Anna V. Reyes". Swept all 239,794 distinct formatted names from the live dataset for residue: 144 trip a crude detector and nearly all are false positives. 127 Worker tests. **A RE-SEED is required after that merge for the corrected names to reach production** (Claude Code)
- 2026-07-30 18:10 CT — CLOSED at Divyam's request. Everything is merged, seeded and verified live: unit owner on the permit view, person in charge on cards/directory/CSV, name formatting corrected after real data exposed two defects. Coverage is partial by nature (~19-21% of contractors, 45% of the top-200 GCs) and companies with no match render no line at all, which is intended (Claude Code)

### FIX-017 · Verify the GC and Open Subs counts at the top are accurate; document how they're computed

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-29 15:39 CT
- **Updated:** 2026-07-29 15:39 CT
- **Tags:** Chicago Permit Search Tool

Check whether the General Contractors and Open Subs counts shown at the top of the site are accurate, and explain the logic behind those numbers so Divyam can see exactly how they're arrived at. The explanation is a first-class deliverable: write it in this task's Log in plain language — what source rows are counted, how entities are deduplicated (name normalization? license id?), what "open" means (which permit statuses), the cutoff date/data vintage, and anything excluded (unlicensed, missing names, out-of-scope permit types).

**Checklist:**
- [ ] Trace where each headline count comes from (pipeline aggregation vs. client-side count of index entries)
- [ ] Recompute both counts independently from the raw dataset (DuckDB query) and compare with what the site shows
- [ ] Check dedup logic: the same company under name variants or multiple licenses should not double-count; note how the pipeline handles this today
- [ ] Check the "open" definition: which permit statuses qualify a GC/sub as having open work, and whether stale permits inflate the count
- [ ] Write the plain-language explanation of the counting logic in this task's Log (for Divyam)
- [ ] If the counts are wrong, fix the aggregation and verify the corrected numbers against the raw-data recomputation; if right, say so explicitly

**Log:**
- 2026-07-29 15:39 CT — created (Divyam)

### FIX-002 · Site-wide ui-ux-pro-max pass: revitalize, clean up, and reformat elements without breaking anything

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-31 11:31 CT
- **Tags:** Chicago Permit Search Tool

Invoke the **ui-ux-pro-max skill** across the whole site (index.html, map.html, list.html) to revitalize, clean up, and reformat elements — layout, spacing, hierarchy, contrast, touch ergonomics, motion — while ensuring FULL functionality is preserved. This is a design-quality sweep, not a redesign: every existing behavior, control, and flow must work exactly as before, proven by the test suite and screenshots, not assumed.

**Checklist:**
- [ ] Run the ui-ux-pro-max skill against all three pages, desktop and mobile viewports, both themes
- [ ] Revitalize and reformat elements it flags: spacing/alignment to the 8px grid, type hierarchy and the 12px floor, contrast to WCAG AA, 44px touch targets, consistent chip/pill/button treatments
- [ ] Clean up accumulated inconsistencies between the three pages (shared components should look and behave identically)
- [ ] Audit layout and overflow on phone-sized viewports
- [ ] Add ARIA labels / semantic markup where missing; verify with a Lighthouse accessibility pass
- [ ] FULL functionality guarantee: run the entire browser suite + unit tests after each change batch; screenshot-diff key screens so purely visual regressions get caught too
- [ ] Log every element changed and why in this task's Log, so anything that looks different is traceable

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)
- 2026-07-31 11:31 CT — rescoped by Divyam: this is now an explicit site-wide ui-ux-pro-max skill pass — revitalize, clean up, and reformat elements while ensuring full functionality; title, description, and checklist updated (Claude)

### FIX-020 · The browser test suite is gitignored and exists on one machine only

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-30 15:55 CT
- **Updated:** 2026-07-30 18:40 CT
- **Tags:** Chicago Permit Search Tool

`verify-tmp/` is in `.gitignore`, so the entire browser test suite — 43 Playwright suites plus the `.mjs` unit tests and the shared `_boot.js` launcher — is untracked and lives only on Divyam's machine. Nothing is backed up, nothing is reviewable in a diff, and a fresh clone has no way to check that a change to `docs/*.html` still works. This already cost real time: `t2`, `t6` and `t8b` sat permanently red for weeks because `_boot.js` drifted behind the multi-list and card-stack reworks, and nobody could see it happening in a commit. Done when the suites are versioned, the scratch output is not, and a fresh clone can run them.

**Checklist:**
- [ ] Separate the suite from the scratch: test sources, `_boot.js` and the `.mjs` unit tests get tracked; screenshots, `server.log`, `node_modules/`, and the `_dbg*`/`_shot*`/`_wheelprobe*` one-offs stay ignored
- [ ] Decide the tracked location — keep `verify-tmp/` and narrow the ignore rule, or move the real suites to `tests/browser/` and leave `verify-tmp/` as pure scratch (prefer the second; the name currently lies about what is in it)
- [ ] Commit `package.json` + a lockfile for the Playwright dependency so versions are pinned
- [ ] Add a short runner (npm script or `run-tests.sh`) that starts the static server on 8791, runs every suite, and reports failures — right now the invocation is a shell loop retyped from memory each session
- [ ] Document the browser prerequisites in the repo: the cached Chromium headless-shell path AND the manual WebKit install (the npm installer stalls; the build zip has to be fetched from the CDN)
- [ ] Note the known-flaky suites so a red run is not ambiguous — `t14-live.js` reaches the real network
- [ ] Verify from a clean clone: install, run the suite, and confirm it goes green without any file that only exists on the original machine

**Log:**
- 2026-07-30 15:55 CT — created (Claude Code, at Divyam's request after FIX-010)
- 2026-07-30 18:40 CT — related flakiness fixed ahead of this card, on branch `fix-008-map-view` (`6895d95`). `t14-live` was failing ~50% of runs (measured 4/8) because it waited on `typeof shareUserList === "function"` — declarations hoist, so init had not run and its async tail replaced `state.lists`, wiping the seed. 10/10 after. Scanning for the same predicate found it in 13 MORE suites, passing but latently flaky. Converting them exposed the deeper defect: `data-ready` was set on the LAST line of `init()`, after `await search()`, which REJECTS on local preview because the Worker is CORS-locked to the Pages origin — so the flag stayed undefined forever and anything waiting on it hung. The flag now lives in one `.finally()` per page and means "init finished", not "init succeeded"; duplicates that had drifted across the three pages are gone and `map.html` has it for the first time. Two clean full sweeps: 0 failures of 47, twice. A third sweep reported `FAIL t17.js` but was killed mid-run — t17 then passed 8/8 in isolation, so that was the teardown, not a flake (Claude Code)

### FIX-026 · "Reported cost" sort does nothing in General Contractors / Open Subs modes

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-31 14:44 CT
- **Updated:** 2026-07-31 15:06 CT
- **Tags:** Chicago Permit Search Tool

Live as `ab3f7b4`.

Found while building FEAT-021. The Sort dropdown in `index.html` offers "Reported cost" in all three search modes, but it is a no-op in two of them: picking it reorders nothing, and the results silently stay in their previous order.

Cause: `sortRows()` sorts on `Number(b[key] || 0)` with `key = "reported_cost"`. Open Permits rows do carry `reported_cost`, so it works there. General Contractors and Open Subs rows are contractor **profiles** — their money field is `reported_cost_total` (the lifetime sum across that contractor's jobs), and they have no `reported_cost` at all. So every row evaluates to 0 and the comparator reports every pair as equal.

The silence is the problem: nothing errors, the dropdown shows the selection, and the list just doesn't change — so it reads as "these are already sorted by cost" rather than as a broken control.

Decide which is meant before fixing, since they are different questions: sort contractors by their **lifetime** reported-cost total (`reported_cost_total`, the field that exists), or drop the option from the two profile modes the way FEAT-021 hides the value range there.

**Checklist:**
- [x] Decide: map the sort to `reported_cost_total` in profile modes, or remove the option from those modes — **mapped**, because the ranking is useful and the data exists: it surfaces the highest-dollar-volume contractors, which is the question the two profile modes are for
- [x] If mapping it, relabel so the column and the option say what is being sorted ("Total reported cost") — a lifetime sum under a "Reported cost" label invites the same confusion
- [x] Check `sortValue()`'s `cost` key and the sortable results-table headers for the same mismatch — clean, no change needed: the contacts table has no cost column and its sortable headers are name/type/public-contact/open-jobs/open-job-age, so the `cost` key belongs to the permits table only
- [x] Verify by sorting each of the three modes and confirming the order actually changes and is correct
- [x] Merge to main and verify on production

**Log:**
- 2026-07-31 14:44 CT — created (Claude Code, noticed during FEAT-021)
- 2026-07-31 15:00 CT — fixed on `fix-026-cost-sort` (`881e67c`), pushed. `sortFieldFor()` resolves the dropdown's key per mode (`reported_cost` → `reported_cost_total` outside Open Permits) and the option is relabelled "Total reported cost" there. Verified by `verify-tmp/t50-costsort.js` — 11 assertions that check the ORDER changes and is correct, not that a control exists, since the old bug passed every presence check; confirmed to FAIL against the un-fixed code, where the list stays in `open_jobs` order. FEAT-021's 68 assertions, 164 Worker tests and the neighbouring suites still pass. **Scope note:** `list.html` and `map.html` carry copies of the same `sortRows`, both behind `display: none` (`.layout` and `.controls` respectively), so the bug is unreachable there and they were left alone — if FIX-002's site-wide pass un-hides that directory, it has to carry this fix. **Observed, not changed:** the contacts table shows no cost column, so the new order has no visible justification — but that is pre-existing and consistent, since "Total jobs" and "Days to get issued" are equally invisible in that table. Adding a value column is a separate design call. (Claude Code)
- 2026-07-31 15:06 CT — **DONE, live.** Merged `--no-ff` to main (`ab3f7b4`); Pages build 2m34s. No Worker change, so this was a merge-only ship. Verified against the real dataset on production, desktop and iPhone 13, 20/20: in both profile modes the cost sort reorders the list and **every** row is descending by `reported_cost_total` (top GC: GILBANE BUILDING COMPANY at $1,207,719,804; top Open Sub: MAP STRATEGIES LLC at $4,283,481,870), the option reads "Total reported cost" there and "Reported cost" in Open Permits, and Open Permits still sorts descending by per-permit cost. (Claude Code)

### FIX-025 · Filter inputs are under 16px, so iOS zooms the page on every focus

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-31 14:39 CT
- **Updated:** 2026-08-03 12:14 CT
- **Tags:** Chicago Permit Search Tool

**DONE — merged and live as `f112b9d`, and confirmed on a real iPhone by Divyam on 2026-08-03.** The card was held open purely for that check, because the symptom it is named for — Safari zooming on focus — cannot be reproduced headlessly.

Measured while building FEAT-021, on the fields next to the new ones — this is pre-existing and site-wide, not caused by that work. Safari on iOS auto-zooms the page whenever a focused input's font is below 16px, and then leaves the page zoomed in; the user has to pinch back out after every filter edit.

Measured at an iPhone 13 viewport: every control in the Search panel renders at **15px** (`body.directory-page .controls input` sets `font-size: 1rem`, but `index.html` shrinks `html` to 15px below 640px, so 1rem is not 16px there — the same rem trap recorded on FIX-022), and every field in the map filter drawer renders at **14.4px** (`map-date-from` at 13.76px). Touch heights are fine: 44–50px throughout.

Not fixed inside FEAT-021 on purpose: the new value-range fields were matched to their neighbours rather than made the only 16px inputs in a row of 15px ones. It needs one deliberate pass across all three pages.

**Checklist:**
- [x] Decide the fix: raise the inputs to a hard 16px, or stop shrinking `html` below 640px — **raised the controls**. The shrink is a deliberate density choice the rest of the layout is built on, and this is a form-control problem, so the fix belongs on form controls rather than on the page's type scale
- [x] Apply to `index.html`, `map.html` and `list.html` — the rem behaves differently per page, so verify each rather than assuming one rule covers all three
- [x] Confirm the date inputs too (`map-date-from`/`map-date-to` are the smallest at 13.76px)
- [x] Verify at an iPhone 13 viewport that no control computes below 16px
- [x] Verify raising the type did not break the layouts — no clipping, no control past the viewport edge, no horizontal scroll at 390px, and no leak to desktop
- [x] Confirm on a real iOS device that focusing a filter no longer zooms — **confirmed by Divyam 2026-08-03**
- [x] Merge to main
- [x] Re-verify the floor survived the CSS that shipped after it (FEAT-024, FIX-027) — re-measured live 2026-08-03, all 29 controls at 16px

**Log:**
- 2026-07-31 14:39 CT — created (Claude Code, from measurements taken during FEAT-021)
- 2026-07-31 15:07 CT — status → in-progress; auditing every form control on all three pages before choosing the fix (Claude Code)
- 2026-07-31 15:17 CT — fixed on `fix-025-input-zoom` (`fc387c2`), pushed. The audit found **32** controls under the floor, not the handful the card listed: 9 on index.html (15px), 14 on map.html (14.4px, dates 13.76px) and 9 on list.html. Applied as a blanket 16px floor on `input`/`select`/`textarea` below 640px, in **px** — `1rem` is exactly the trap that caused this bug, meaning 15px on index.html (shrinks `html`) and 16px on list.html (shrinks only `body`). Chose a blanket floor over per-field rules because the walkthrough/photo/note dialogs render on demand and an id-by-id fix would have missed them — the first audit did miss them, until the test suite opened the dialogs. **Two traps worth recording.** (1) The rule needs `:is()`: written as three plain selectors, `html body select` scores 0-0-3 and LOSES to `body.directory-page .controls select` (0-2-2), which is exactly what happened on the first attempt — the inputs passed and #sort/#mode-select stayed at 15px, because the input arm happened to carry two `[type]` tests. `:is()` takes its most specific argument so every arm lands at 0-2-3. (2) `#photo-compose .dlg-field input` is id-scoped (1-1-2) and outranks the floor, so it was fixed at source or it would have been the one control still zooming. Verified by `verify-tmp/t51-input-zoom.js`, 15 assertions across all three pages, confirmed to FAIL against the un-fixed code; it also covers the half that could have broken things (no clipping, nothing past the viewport, no horizontal scroll at 390px) and that the floor does not leak to desktop, checked byte-for-byte against main. t47/t48/t49/t50 still pass. **Only the real-device confirmation is left** — headless cannot show the zoom. (Claude Code)
- 2026-07-31 15:24 CT — merged `--no-ff` to main (`f112b9d`); Pages build 3m0s. No Worker change, merge-only ship. Verified on production at an iPhone 13 viewport: all 32 controls across the three pages compute at 16px or above (9 / 14 / 9), and no page scrolls horizontally at 390px. **Status deliberately left in-progress rather than done**, because the card's own checklist has one item automation cannot close — the zoom symptom itself. Everything measurable is confirmed live; what remains is Divyam tapping a filter field on a real iPhone. (Claude Code)
- 2026-08-03 12:05 CT — asked to implement this card; it was already built, merged and live, so the useful work was a REGRESSION check rather than new code. Two CSS changes have shipped to all three pages since this fix landed (FEAT-024 `568d695`, FIX-027 `8885e8d`), and this card's own note says the `:is()` selector fails *silently and partially* when disturbed — so it was worth re-measuring rather than assuming. It held. Source intact on all three pages; the id-scoped audit re-run finds only the two `#photo-compose .dlg-field input` rules, both already at 16px. t51 passes 15/15 locally, and the deployed `index/map/list.html` are byte-identical (md5) to `main`, so the local run that opens the on-demand dialogs applies to production exactly (Claude Code)
- 2026-08-03 12:05 CT — re-measured LIVE production at an iPhone 13 viewport: **29 controls, every one at exactly 16px, no horizontal scroll on any page**. Two are worth naming. `map-date-from` was the worst offender on this card at 13.76px and now reads 16px. `map-property-use` is FEAT-024's NEW control, added after this fix shipped, and it lands inside the floor's coverage for free — which is the argument for the blanket rule over per-field fixes, now demonstrated rather than predicted. map.html measures 15 controls where this card originally counted 14, for that reason (Claude Code)
- 2026-08-03 12:05 CT — **STAYS in-progress, deliberately, for the same single reason as on 07-31.** The symptom this card is named for is Safari's zoom-on-focus, and no headless browser reproduces it — it is a real-device behaviour. Marking this done off green automation would be closing it on evidence that cannot see the bug. Divyam: on your iPhone open the live site, tap the **Name/permit/address** field on Search (`index.html`), then the **date** and **Search area** fields in the map's Filters drawer (`map.html`) — those three were 15px, 13.76px and 14.4px before the fix. If the page does not zoom and strand you, close this card; if it still zooms, reopen with which field did it (Claude Code)
- 2026-08-03 12:14 CT — **DONE.** Divyam confirmed on a real iPhone that focusing the filter fields no longer zooms the page. That was the last open item and the only one automation could not close; every measurable half was already green live (29 controls at 16px, no horizontal scroll). Closing (Claude Code)

---

## ✨ Features

> **Purpose:** New features and ideas to be added to the existing Chicago Permit Search tool. Enhancements that extend the current project rather than repair it.

### FEAT-045 · Tooling: control-style snapshot harness for blanket CSS changes

- **Priority:** P3-Low
- **Status:** done
- **Created:** 2026-08-07 09:30 CT
- **Updated:** 2026-08-07 09:30 CT
- **Tags:** Chicago Permit Search Tool, tooling

Card written after the fact — this shipped with no card at all, found by auditing merge commits against the board.

Before/after diffing for a change that edits **one rule covering many elements**: a global `button {}`, a blanket floor (the 16px iOS font floor, the 44px touch-target floor), a specificity change (`:is()`, `:where()`, re-scoping a selector), or anything described as "just a refactor, no visual change". These cannot be checked by looking at the page: the regression is always in the one member the rule was not written for, and it stays invisible until someone opens that surface. This repo has paid for that lesson repeatedly — FIX-025's `:is()` trap let two selects through, and the `:where()` sweep considered during FIX-029 was measured at 364 broken declarations and rejected.

`scripts/verify/snapshot-controls.js` writes a JSON snapshot of every control's computed geometry across the pages; `scripts/verify/diff-snapshots.js` compares two snapshots and **exits 1 if anything changed**, so it can gate a refactor that is meant to be behaviour-preserving. `--all` shows every group. Needs a static server on `docs/` (`npx http-server docs -p 8791 --silent`). Honours `CHROME_PATH`, otherwise picks the newest cached `chromium_headless_shell-*` — Playwright's own default is deliberately not trusted, matching the rest of the verification setup.

**Log:**
- 2026-08-07 09:30 CT — **backfilled from git.** Commit `efd6851` on branch `tooling-snapshot-harness`, merged to `main` as `91a5116` on 2026-08-06 and pushed; `main` == `origin/main` == `91a5116`, branch gone from local and `origin`. 296 lines across `scripts/verify/{README.md,snapshot-controls.js,diff-snapshots.js}`. Documentation and tooling only — no product code, nothing deployed, nothing user-facing. Filed as done rather than as a todo because the work is already in `main`; the card exists so the board stops disagreeing with the repo (Claude Code)

### FEAT-044 · Lift the directory result caps

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-07 09:30 CT
- **Updated:** 2026-08-07 10:14 CT
- **Tags:** Chicago Permit Search Tool

**This card exists to resolve an ID collision.** Branch `origin/feat-044-lift-directory-caps` carries a 148-line design spec (`docs/superpowers/specs/2026-08-06-lift-directory-caps-design.md`, commit `54f6ada`) that originally claimed the ID **FEAT-040**. FEAT-040 was already taken on this board by "Permit Map: filter by visited / not visited / called / not called", created 2026-08-05 10:33 — a day before that spec. The board has priority and IDs are never reused, so the directory-caps work is **FEAT-044** from here on. The collision is now resolved on both sides; the work itself has not started.

**Checklist:**
- [x] Rename the spec's ID to FEAT-044 and rename the branch (`feat-044-lift-directory-caps`); no code depends on the old name
- [ ] Read the existing spec before designing further — it is 148 lines and predates this card
- [ ] Apply the ceiling discipline this repo has already learned: multiply any new cap through every serialisation boundary and MEASURE it (see FEAT-035's Durable Object 128 KiB per-value split and the request-body cap that a 220→1000 change breached)

**Log:**
- 2026-08-07 09:30 CT — created during a board/git reconciliation audit, purely to give the branch a non-colliding ID. No work done on the feature itself (Claude Code)
- 2026-08-07 10:14 CT — collision resolved in the code repo: branch renamed `feat-040-lift-directory-caps` → **`feat-044-lift-directory-caps`** (old remote deleted), and the spec's heading renumbered to FEAT-044 with a note recording why (`238b846`). The spec is design only — no product code referenced the old ID. Feature itself still not started (Claude Code)

### FEAT-043 · Contractor background verification: how long they take to finish, and whether they pay their subs

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-06 09:19 CT
- **Updated:** 2026-08-06 09:19 CT
- **Tags:** Chicago Permit Search Tool

Requested by Divyam: give each contractor a background-verification view answering two questions a person hiring them would actually ask — **how long do their jobs take**, and **do they pay their open subs**.

Half of this is already built. FIX-012 established the closure metric: time-to-close is OBSERVED, not published — the City's data records *that* a permit closed, never *when* — so every seed since 2026-07-30 books issue-date → first-seen-COMPLETE per contractor into `closure:stats`. That is the duration signal; this card turns it from a pill into a verification view, adds distribution rather than just a mean, and adds the still-open dimension (jobs sitting open far past this contractor's own typical close time).

The payment half has no direct source and must not be faked. Nothing in the permits data records whether a sub was paid. The honest proxy is the **mechanics lien** — a sub who is not paid records one against the property with the Cook County Recorder — which is exactly the deed/title source now in FEAT-029's checklist, so this card is gated on that ingestion. Absence of a lien is weak evidence of payment and must never be displayed as "pays subs"; a recorded lien is strong evidence of a dispute and can be shown as the record it is.

**Checklist:**
- [ ] Define what "background verification" shows before building it — write the field list and the exact claim each field is entitled to make in this task's Log
- [ ] Duration: build on FIX-012's observed closure stats rather than recomputing. Show the distribution (median and spread, not just the mean over `{n, days}`) and the observation count, so a contractor with three observations does not read like one with sixty
- [ ] Duration: add currently-open job age — jobs open well beyond this contractor's own observed typical close, which is the live signal a stalled job produces before any closure is ever booked
- [ ] Suppress the metric entirely below a minimum observation count rather than showing a thin average — FIX-012 already established that absent beats misleading here, and the pill is omitted rather than zeroed
- [ ] Payment: gate on FEAT-029's Cook County Recorder ingestion; match mechanics liens to contractors by name normalization (the licensed-contractor match) and to properties by PIN/address
- [ ] Payment: show recorded liens as records with date, claimant, property and amount — never derive a "pays / does not pay" verdict, and never render absence of liens as evidence of payment
- [ ] Check what else is available and honest before settling: IDFPR licence status and any disciplinary record, licence lapses, and the City's own registry status (FEAT-004/FEAT-014 already ingest this)
- [ ] Surface the view wherever a contractor appears — GC profile first, then directory row and permit detail — with a per-source caveat naming the source and its vintage
- [ ] Verify against contractors whose history is independently known, and confirm a low-observation contractor and a lien-free contractor both render honestly rather than favorably

**Log:**
- 2026-08-06 09:19 CT — created (Divyam)

### FEAT-042 · Surface Closed permits: a Search Directory option and a Closed-permits list per GC

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-05 11:00 CT
- **Updated:** 2026-08-05 11:00 CT
- **Tags:** Chicago Permit Search Tool

Requested by Divyam: the app currently centers on open/active permits; closed permits should be reachable too. Two surfaces: (1) add **Closed Permits** as a search option in the Search Directory so a user can look them up the way they look up open ones, and (2) under each General Contractor in the General Contractors view, list that GC's Closed permits so their full scope of work is visible — not just what's currently open. The point is the complete picture of a contractor: open plus closed.

Confirm first where closed permits live: whether the dataset the app already ingests carries closed/completed records (a status field) or whether closed permits are a separate pull that isn't currently loaded — that decision (filter existing data vs. ingest more) drives the size of this and should be written in the Log before building.

**Checklist:**
- [ ] Establish the data source: does the ingested permit data already include closed/completed permits (a status the app filters out today), or do they need a separate fetch? Record the answer in the Log — it decides whether this is a filter change or an ingestion change
- [ ] Search Directory: add a Closed Permits option so users can search closed permits, consistent with how open permits are searched (same fields/filters where they make sense); make clear in the UI which status is being searched
- [ ] General Contractor view: add a Closed permits section per GC alongside their open permits, so both together show the full scope of the GC's work; label the two clearly so an open and a closed permit are not confused
- [ ] Keep it consistent on both index.html and list.html card stacks, matching the existing open-permit presentation (details, contractor attribution, notes where they apply)
- [ ] Handle the empty and mixed cases: a GC with only open permits, only closed, or both; no empty/zero-count section that reads as broken
- [ ] Watch volume — closed permits can be a large historical set; page/limit rather than rendering an unbounded list, and measure the added load cost
- [ ] Verify on desktop and mobile in both themes: searching closed permits from the directory, and viewing a GC's open + closed permits together

**Log:**
- 2026-08-05 11:00 CT — created (Divyam)

### FEAT-041 · General Contractor view: embed a map of the GC's open permits

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-05 11:00 CT
- **Updated:** 2026-08-05 11:00 CT
- **Tags:** Chicago Permit Search Tool

Requested by Divyam: inside the General Contractor view, show a map of that GC's open permits. Use the existing Permit Map (`docs/map.html`) as the reference build — same tile/marker/cluster stack — rather than a second mapping approach, but scoped to just this GC's open permits instead of the whole city. The permits and their coordinates are already resolved for the GC view; this is a rendering/embedding job, not a new data pull.

The core risk is layout: an embedded map must size to its container and must NOT overflow or introduce nested/duplicate scrolling on either mobile or desktop. Map libraries grab scroll/touch to pan, so getting the container sizing, height, and gesture handling right is the actual work here.

**Checklist:**
- [ ] Reuse the Permit Map's map setup (tiles, markers, clustering, theme handling) rather than forking a parallel implementation; feed it only this GC's open permits
- [ ] Give the embedded map a bounded, explicit height that fits the GC view's layout on both desktop and mobile — no page-level horizontal overflow, no nested scrollbar fighting the page scroll
- [ ] Handle map pan/zoom gestures inside the card without hijacking the page scroll on mobile (e.g. the usual embedded-map scroll/touch handling)
- [ ] Fit the initial viewport to the GC's open permits (bounds of the set), and handle the edge cases: a single permit, permits far apart, and a GC with zero open permits (no empty/broken map — hide or show a clear empty state)
- [ ] Keep pins consistent with the main Permit Map (same marker meaning, popup/click behavior) so the two don't drift
- [ ] Verify on desktop and mobile in both themes: the map loads, sizes correctly, pans without breaking page scroll, and causes no overflow

**Log:**
- 2026-08-05 11:00 CT — created (Divyam)

### FEAT-040 · Permit Map: filter by visited / not visited / called / not called

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-08-05 10:33 CT
- **Updated:** 2026-08-05 10:33 CT
- **Tags:** Chicago Permit Search Tool

Bring FEAT-031's visited/called filtering to Map Search (`docs/map.html`): filter the map to visited, not visited, called or not called. The states already exist and already sync — they are per-permit flags on a saved list (`ticks`, `called`), stored with the actor's name and shared through the Worker.

The design question this card must answer first: **those flags live on a LIST, and the map shows every permit in the city.** A permit that is in no list has no visited state at all, so "not visited" cannot honestly mean "every unvisited permit in Chicago". The likely answer is that the filter scopes the map to a chosen list (or to all listed permits) the way the list page does, and says so on screen — but decide it deliberately and write the decision in the Log before building. Reuse FEAT-031's chip pattern: mutually exclusive within a pair, combinable across pairs, pressing the active chip clears its facet.

**Checklist:**
- [ ] Decide and record the scope: which permits the filter can speak about, and what the map shows when a filter is on (only listed permits? a list picker? a clear on-screen statement of the scope?) — an honest "not called" is impossible over permits with no list
- [ ] Add the chips to the map's filter drawer, matching FEAT-031's semantics and wording exactly so the two pages do not drift
- [ ] Compose correctly with the existing map filters (date, GC range, neighborhood/radius, value range, work-type exclusions, property use) and say in the status strip what is active
- [ ] Reflect the state on the pins themselves where it helps (a visited permit reading as unvisited on the map would be worse than no filter)
- [ ] Keep the flags live: a permit ticked on the list page should reach the map through the same sync path, not a stale copy
- [ ] Persist with the rest of the map's filters (see FIX-035) — a filter that silently resets on reload is how permits get missed
- [ ] Verify on desktop and mobile: each facet alone, combined across pairs, with an empty result set, and on a shared list where someone else did the visiting

**Log:**
- 2026-08-05 10:33 CT — created (Divyam)
- 2026-08-07 09:30 CT — note, no work done: branch `origin/feat-040-lift-directory-caps` wrongly claims this ID for unrelated work (lifting the directory result caps). This card keeps FEAT-040 — it was created first — and that branch has been renumbered to **FEAT-044** (Claude Code)

### FEAT-039 · Lift the route-optimizer ceiling to the full 1000-permit cap by fetching fewer matrix cells

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-08-04 13:06 CT
- **Updated:** 2026-08-07 09:30 CT
- **Tags:** Chicago Permit Search Tool

FEAT-035 raised the list cap to 1000 but left `MAX_SORT_STOPS` at 500, so Optimize Route is unavailable on the largest lists the tool now lets you build. It says so honestly rather than failing, but the feature is simply absent above 500 stops.

**The CPU ceiling is already gone — do not re-solve it.** FIX-004 set the 400 limit because the 2-opt/Or-opt local search was ~O(n^3) on the main thread (6.2s at 400, 25s at 600). FEAT-035 made that search evaluate moves incrementally instead of rebuilding and re-summing the whole path per candidate, which is ~O(n^2) a pass: **measured 0.58s at 400 stops and 1.35s at 1000**. A worker thread is not needed and would be wasted effort.

**What actually binds now is the OSRM matrix request count.** The matrix tiles at 50x50 (the split that yields the most cells per 100-coordinate request), costing `ceil(n/50)^2` requests: 64 at 400 stops, **100 at 500, and 400 at 1000** — against the public OSRM demo server, at 4-way concurrency. That is minutes of traffic to a shared host and an invitation to be rate limited, which is why 500 was chosen rather than a number the arithmetic allowed. The fix is to fetch fewer CELLS, not to route faster.

Two candidate approaches, both noted but neither built:
- **Sparse k-nearest matrix** — a stop only ever needs durations to its plausible neighbours, so fetch a band around each stop rather than the full square. Both the greedy seed and the local search read the matrix through `legDuration(a, b)`, which already returns `Infinity` for a missing pair, so a sparse matrix may drop in behind that accessor with little change to the search itself. Needs care: too sparse and 2-opt/Or-opt cannot see the moves that untangle a bad greedy path.
- **Cluster-then-route** — FIX-004's originally noted path: partition the stops geographically, solve each cluster, then stitch. Changes route quality in a way a user would notice, so it needs a quality comparison, not just a speed one.

**Checklist:**
- [x] Decide sparse-k-nearest vs cluster-then-route on measured route quality, not just request count — reuse FEAT-035's harness (`verify-tmp/feat035-impl.mjs` has `randomInstance`/`routeCost` and a full-recompute reference; compare the paired distribution over ~200 instances, not one run, since two correct local optima can differ 10% either way)
- [x] Confirm the neighbour band is wide enough that 2-opt and Or-opt still find their moves — a sparse matrix that hides an improving move degrades the route silently
- [x] Keep `legDuration`'s `Infinity`-for-missing contract, and re-check the guards that depend on it (a `-Infinity` delta must not be accepted; the local search's restart budget must still terminate)
- [x] Bring the request count for 1000 stops down to the same order as today's 64-100, and state the new number in the `MAX_SORT_STOPS` comment the way the current one does
- [x] Raise `MAX_SORT_STOPS` to 1000 only once the request count justifies it; if it lands somewhere between, set it to what was measured and keep the honest message above it
- [x] Be a good citizen of the public OSRM demo server — keep the concurrency cap, and check whether the volume warrants a self-hosted or paid routing endpoint instead
- [x] Verify on a real 1000-permit list end to end: route completes, progress reporting stays sane, and the resulting order is not visibly worse than the same list sorted at 500

**Log:**
- 2026-08-04 13:06 CT — created from FEAT-035's deliberate deviation: the CPU ceiling was removed, the routing-service budget is what remains (Claude Code)
- 2026-08-04 14:55 CT — started: read `fetchDurationMatrix`, `greedyRouteOrder` and the `MAX_SORT_STOPS` guards end to end before choosing an approach (Claude Code)
- 2026-08-04 ~15:53 CT — session ended mid-task with the work uncommitted; parked on branch `feat-039-sparse-matrix` as commit `0e2baac` on 2026-08-05 so FEAT-032 could start from a clean `main`. Nothing lost (Claude Code)
- 2026-08-05 11:42 CT — **resolved the three red assertions.** Root cause was an off-by-one in request accounting, not in the sparse strategy: `fetchDurationMatrix` passed the FULL `MATRIX_REQUEST_BUDGET` to `bandTilePairs` and then spent `fillCoarseDurations`' request on top, so every sparse sort cost budget + 1 — a flat 101 against a budget of 100 at both 600 and 1000 stops, which is exactly what the assertions reported. The line's own comment ("One request of the budget is spent on the coarse layer below") and the `MAX_SORT_STOPS` comment's live measurement of 99 both already described the intended behaviour; the code had drifted from them, most likely during the span/radius ranking rework. Fix is `MATRIX_REQUEST_BUDGET - 1` at that one call site. Commit `a5bfe64`, pushed (Claude Code)
- 2026-08-05 11:42 CT — 1000 stops now costs **99 requests** (was 101), 500 and under still take the dense path at 100 and are byte-for-byte untouched. `feat039-matrix.mjs` 17/17, including the route-quality comparison against the full matrix and the local-search termination check (Claude Code)
- 2026-08-05 11:42 CT — `t63-sparse-matrix` was not a product failure at all: it targets `:8793`, which nothing serves during a sweep, so it died on a connection error that read like a timeout. Pointed at `:8791` like every other `t*.js`; it now passes in the real page — 1000 stops, 99 requests, no request over the 100-coordinate limit, order improved 94.96%, progress reporting sane (Claude Code)
- 2026-08-05 11:55 CT — **re-ran the live probe against the real OSRM demo server rather than inheriting the number.** The `MAX_SORT_STOPS` comment claimed "99 requests, 13s, no failures" while the code was costing 101, so the claim needed re-earning: `_live39-osrm.js` with 1000 real Chicago permit coordinates now measures **99 requests, 0 failures, 13.2s wall (12.5s matrix), 1000 stops / 999 legs, 664 mi / 32 hr**. Matches the shipped comment exactly. The 4-way concurrency cap is unchanged and the volume is what a 500-stop sort already sent, so no self-hosted or paid routing endpoint is warranted (Claude Code)
- 2026-08-05 11:58 CT — **done.** Commit `a5bfe64` on `feat-039-sparse-matrix`, pushed. Full browser sweep (73 scripts): 70 green; `t41-notes-feed` passes in isolation (batch port contention), `t64-list-provenance` is FEAT-032's suite on a branch without FEAT-032, and `t9` fails identically on `main` (pre-existing, unrelated). Unit suites 229 pass. **Not merged — awaiting approval** (Claude Code)
- 2026-08-07 09:30 CT — **backfilled from git: this was merged and the card never said so.** `feat-039-sparse-matrix` went to `main` as merge `725d9e5` on 2026-08-06 and is pushed (`main` == `origin/main` == `91a5116`); the branch is gone from both local and `origin`. The line above it still read "Not merged — awaiting approval" for a day, which was the board's version of the truth while git had the opposite. Approval and merge happened; only the bookkeeping was skipped (Claude Code)

### FEAT-038 · Source property use from the Cook County Assessor class, so the permit view stops approximating

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-08-03 11:03 CT
- **Updated:** 2026-08-04 14:51 CT
- **Tags:** Chicago Permit Search Tool

The permit view's "Property use" line is a guess. `permitUse()` (FEAT-013) reads `permit_type` + `work_description` and is rendered with an "approx" badge because the permits dataset carries no occupancy field. Over a real month it can classify only **32%** of permits; the other 68% read "Unclear".

Divyam asked whether the zoning source that made FEAT-024's filter work could replace it. **It cannot, and should not** — see the log. But the permits dataset already carries `pin_list`, the Cook County PIN, which joins straight to the Assessor's parcel universe (`nj4t-kc8j`) and its `class` field: the County's own legal classification of the parcel's use for assessment. That is a recorded fact the badge can cite, not an inference from prose.

Measured over July 2026 (2,384 open geocoded permits): 2,101 (88.1%) carry a usable 10-digit PIN, and **2,057 (86.3%) match an Assessor parcel record** — 67.4% residential, 11.5% commercial/industrial, 5.0% exempt, 1.8% vacant, 0.4% incentive. With the existing text heuristic kept as fallback for the unmatched, **only 11.5% of permits would still read "unknown", down from 68%.**

**Checklist:**
- [x] Build a three-digit class → use mapping, NOT a major-class one (see the log — this is where the errors concentrate)
- [x] Resolve a permit's class on demand from `pin_list`, cached per permit, the same shape as the existing zoning and TIF lookups — never a bulk fetch
- [x] Handle the multi-PIN case (`pin_list` is pipe-delimited; ~39 permits a month carry several parcels)
- [x] Show the class as a sourced fact ("Residential · Cook County class 203") and drop the "approx" badge where the class is decisive
- [x] Keep `permitUse()` as the fallback for the ~12% with no parcel match, still badged as approximate
- [x] Keep a hedge for the genuinely mixed 5xx classes rather than calling them commercial — the dictionary MOVED this concern; see the log
- [x] Verify a sample against the Assessor's own property search, not just against the old heuristic — the property search 403s automated clients, so two other Assessor-published datasets stood in; see the log
- [x] Decide whether the FEAT-024 map filter should switch to this source too, or stay on zoning (they answer different questions — see the log)
- [x] A pre-existing bug found on the way: `pmFacts` emitted its empty placeholder even when `extra` supplied the value, so Zone shipped as "—RS-3" and TIF district as "——". Fixed at the root

**Log:**
- 2026-08-03 11:03 CT — created from Divyam's question after FEAT-024 shipped: "if the residential/commercial filter works effectively now, can we accurately use the same data sources to correctly tag residential/commercial on the Permit details, and not have to use approximations?" (Claude Code)
- 2026-08-03 11:03 CT — **answer: yes, but NOT from zoning.** Zoning states what a district ALLOWS, not what a property IS. Measured over the same July month, **213 of the 623 permits the text confidently calls residential sit in non-residential districts** — 98 in planned developments, 44 business, 39 downtown, 12 manufacturing, 12 commercial, 6 open space, 2 transportation. Those are overwhelmingly real housing work (a B3-5 fire alarm reading "AFFECTS: 40 DWELLING UNITS"). Zoning is the right signal for a FILTER ("show me residential areas") and the wrong one for a LABEL on one permit, where it would confidently mislabel about a third of them. FEAT-024 stays on zoning deliberately (Claude Code)
- 2026-08-03 11:03 CT — the join was proven end to end before this card was written, not assumed: `pin_list` → `nj4t-kc8j.pin10` → `class`, newest `year` first, batched 150 PINs per request. Coverage figures above are from that run. Cook County major classes: 0xx/1xx vacant, 2xx houses and 2–6 units, 3xx apartments 7+, 4xx not-for-profit, 5xx commercial/industrial, 6xx–9xx incentive, EX exempt (Claude Code)
- 2026-08-03 11:03 CT — **three caveats found while measuring, all of which belong in the build rather than being discovered after it.** (1) The class describes the PARCEL, not the work: agreement with the text heuristic where both speak is 85.9%, and the 82 disagreements are instructive — class 590 on "NEW 2 STORY SINGLE FAMILY RESIDENCE", class 517 on plumbing-fixture work — some are conversions the class has not caught up with. (2) **A naive `5xx → commercial` mapping is wrong**: several 5xx classes explicitly ARE mixed commercial/residential (593 is "two or three story, over 62 years, mixed commercial and residential"), and that is exactly where the probe's disagreements clustered, because the probe used major class. (3) It adds a second live dependency on Cook County's Socrata, so it needs the on-demand + cache treatment, not a bulk fetch (Claude Code)
- 2026-08-04 14:41 CT — started: reading `permitUse()`, the zoning/TIF lookup shape, and every path that builds a permit row (Claude Code)
- 2026-08-04 14:41 CT — **the mapping is not hand-written.** The Assessor publishes its own class dictionary — `ccao-data/data-architecture`, `dbt/seeds/ccao/ccao.class_dict.csv`, 252 classes with a `major_class_type` per class — so the table is generated from that file rather than from the code manual as remembered. This settles checklist item 1 with a source instead of an assertion, and the file itself proves why a major-class mapping is wrong: **591 is Commercial but 593 is Industrial**, 991/997 are Class-3 residential incentives despite the 9, and the four genuinely mixed-use classes (212, 318, 418, 918) sit under **three different** major types (Claude Code)
- 2026-08-04 14:41 CT — **the card's own mixed-5xx example was wrong, and the dictionary is what caught it.** This card said "593 is two or three story, over 62 years, mixed commercial and residential". It is not — the dictionary has 593 as "Industrial building". The genuinely mixed classes are 212, 318, 418 and 918, and they now get their own "Mixed use" label; no 5xx class is mixed. The hedge the checklist asked for still exists, it just belongs somewhere else than the card guessed. Same lesson as measuring before believing a ticket's stated cause (Claude Code)
- 2026-08-04 14:41 CT — **`pin_list` is not on the permit rows.** It is selected by none of the six row-construction sites across the three pages, and the map path stores rows under compressed one-letter keys. Threading it through all of them would have been a far wider diff than the feature; instead `ensurePermitPins()` reads it off the row when a path happens to carry it and otherwise does ONE lookup by permit number, for the one permit whose overlay is open. Deliberately skipped: adding `pin_list` to the two `$select` lists so the common paths need no second request — worth doing if that request is ever measured to matter (Claude Code)
- 2026-08-04 14:41 CT — **found and fixed a pre-existing rendering bug that ships today.** `pmFacts` renders `${v ? esc(v) : "—"}${extra}`, so a row whose value arrives via `extra` got the EMPTY placeholder anyway: Zone has been rendering as **"—RS-3"** and TIF district as **"——"** on every permit since the async rows landed. The new Property use row is the third caller of that shape and inherited it, which is how it surfaced. Fixed in `pmFacts` itself rather than worked around in the new row — one guard where all three callers route through (Claude Code)
- 2026-08-04 14:41 CT — **the Assessor's own property search could not be used, and the substitute is better.** `cookcountyassessor.com/pin/<pin>` is client-rendered and its CloudFront rule returns 403 to a headless browser, so checklist item 7 went to two OTHER datasets the Assessor publishes, both from the assessment pipeline rather than the parcel universe the feature reads: (1) **Assessed Values (`uzyt-m557`) agrees on the class for 297 of 298** sampled parcels, the one difference being RR-railroad vs 591; (2) more usefully, **Single/Multi-Family Improvement Characteristics (`x54s-btds`) confirms the class MEANS what the mapping claims** — classes 202/203/204 are one-story homes in three size bands, and **79/79** of the sampled parcels' measured building areas fall inside their class's band. Agreement on a code only proves we copied it; the size-band check is what proves the reading (Claude Code)
- 2026-08-04 14:41 CT — **measured on the shipped code**, July 2026, 2,382 open geocoded permits: **87.7% now show a sourced Assessor class**, 5.2% fall back to the text heuristic still badged approx, and **7.1% still read "—"** — against **32.5%** that the text heuristic could classify at all. Better than this card's 11.5% estimate for the remainder. Sourced split: 62.9% residential, 12.3% commercial/industrial, 5.6% exempt, 5.0% mixed, 1.8% vacant. **Zero** class codes appeared in that month that the table does not cover (Claude Code)
- 2026-08-04 14:41 CT — **decision on checklist item 8: FEAT-024's map filter STAYS on zoning, and the two are now deliberately different sources.** This card's own log already made the argument and it still holds — zoning answers "show me residential AREAS" and the Assessor class answers "what IS this parcel", and the class is only available per-permit via a live lookup that a map filter over thousands of points must not make. `resolveGeoForRows` was given an explicit comment saying it must not resolve the class, so an export cannot quietly turn the on-demand lookup into a bulk one. For the same reason the saved-list table's "Use" column stays on `permitUse()` — a column is a bulk fetch by another name (Claude Code)
- 2026-08-04 14:41 CT — verified: 14 unit assertions **extracted from the shipping page at test time** (`verify-tmp/feat038-use.mjs`, the feat024 pattern, and it also asserts the block is byte-identical on both pages); **7 mutants, all caught** — including bucketing 991 by its leading digit, taking the first bucket instead of Mixed use, caching a network failure, and badging a sourced class approximate; 21 browser assertions across index.html, list.html and iPhone 13 (`verify-tmp/t62-property-use.js`); contrast **6.32:1 light / 8.51:1 dark** with a poisoned control proving the probe still discriminates; and **6/6 live unstubbed permits** where the overlay's class matched Cook County read independently. Worker suite still 200/200 (Claude Code)
- 2026-08-04 14:41 CT — `289e834` on branch `feat-038-assessor-class`, pushed. Held there pending Divyam's merge approval (Claude Code)
- 2026-08-04 14:51 CT — **DONE and LIVE.** Divyam approved the merge; `--no-ff` merge `67a4ca5` on `main`, branch deleted locally and on origin. Re-ran the full battery against the MERGED tree before pushing (14 unit, 21 browser, 200 worker) — not just against the branch. Verified at the destination rather than trusting the push: polled the live Pages files until `ASSESSOR_CLASS_USE` actually appeared in both `index.html` and `list.html` (~2 min), then drove the **production site** with 6 real permits and no stubs — every one rendered the class that Cook County returns when read independently (Claude Code)

### FEAT-025 · Contractor detail view in the permit overlay

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 14:27 CT
- **Updated:** 2026-07-28 21:50 CT
- **Tags:** Chicago Permit Search Tool

Tap a general contractor or open sub inside a permit detail overlay to open that
contractor's profile as a card in the same overlay, with a navigable card stack
(permit → contractor → permit → …). Full parity with the directory pane's
profile: stat pills, License, Specialties, Associations, and the contractor's
open permits with a Call action and "Add all N to list". Browser Back steps the
stack and only closes at the bottom. Both index.html and list.html.

All three phases are shipped and live.

**Checklist:**
- [x] Card stack core: typed descriptors, one history entry per card, focus restore
- [x] Contractor card renderer: pills, License, Specialties, Associations, permits table
- [x] Data layer: parallel fetch, skeleton, error + Retry, aria-busy lifecycle
- [x] Bidirectional wiring: contractor rows open cards, permit rows open permits
- [x] "Add all N to list" goes through the list picker
- [x] Focus moves and card is announced on every navigation
- [x] Push/back motion, interruptible, reduced-motion respected
- [x] ui-ux-pro-max pass: 44px targets, 8px spacing, contrast, 12px type floor, landscape
- [x] Full-suite verification: 111 client + 99 Worker + 11 browser suites
- [x] Phase 2: Worker matching ladder — exact / cross-category / normalized
- [x] Phase 2: `matched as <name>` and `Profile data as of <date>` on the card
- [x] Phase 3: last-view persistence — tab, query, sort, page, scroll
- [x] Contractors/Open Subs open in the overlay, matching the permit view (filters + paging ported, side pane deleted)
- [x] Re-run `node seed-kv.js` so `seeded_at` exists and the staleness line shows

**Log:**
- 2026-07-27 14:27 CT — design spec written, accessibility audit at design time (Claude Code)
- 2026-07-27 16:23 CT — tasks 1-4 built on branch, task 4 held for review (Claude Code)
- 2026-07-28 18:20 CT — task 4 reviewed; keyboard-dead contractor rows fixed; bulk add now offers the list picker; tasks 1-4 merged to main `d608b38` (Claude Code)
- 2026-07-28 18:55 CT — tasks 5-6 complete; ui-ux-pro-max pass fixed mid-number wrapping and a sub-12px type floor that also rendered differently on the two pages; merged to main `1a96736`; Phase 1 done (Claude Code)
- 2026-07-28 19:34 CT — Phase 2: Worker matching ladder + matched_as/matched_category/seeded_at, 18 new Worker tests (117 total). Worker deployed and all three rungs verified in production, then merged to main `24d6537`. seeded_at pending a seed-kv.js re-run (Claude Code)
- 2026-07-28 20:12 CT — Phase 3: chi_permit_last_view now carries tab/query/sort/page/scroll/selection on both pages; merged to main `011f56c`. All three phases done — 111 client + 117 Worker + 13 browser suites green (Claude Code)
- 2026-07-28 21:50 CT — Contractor card you left open now reopens on load (chi_permit_last_view.card), replacing the selection restore the pane deletion removed. t13 flake fixed — same async-init race as t19/t23. Merged `2731365` (Claude Code)
- 2026-07-28 21:20 CT — Contractors/Open Subs now open the same animated overlay card as permits; the 4 permit filters and paging ported in; inline #detail-panel deleted (net -310 lines). a11y pass found both focusable <tr> templates were inert on Enter (including the card's permit rows, live since Phase 1) — fixed. Merged to main `74d8760`. Trade-off: the selected profile is no longer restored across reloads, since the pane it selected into is gone (Claude Code)
- 2026-07-28 21:05 CT — seed-kv.js re-run and VERIFIED: seeded_at is live (2026-07-28T19:45:49.226Z, both categories). First attempt silently wrote to the local Miniflare KV — wrangler 4.x defaults `kv key put` to local — so kvPut now passes --remote. All FEAT-025 items closed (Claude Code)

### FEAT-021 · Add permit value range to Search and Map Search

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-31 14:51 CT
- **Tags:** Chicago Permit Search Tool

Filter/search by permit (reported cost) value range in both the Search tool and the Map Search tool.

Live: Worker version `8c859f74`, site merged as `03477ee`.

Scope decision: the range shows only in **Open Permits** mode on the Search tool. The General Contractors / Open Subs modes are contractor profiles whose only money field is `reported_cost_total` (a lifetime sum across all their jobs) — filtering that by a per-permit range would answer a different question than the card asks, so `setMode()` hides the fields there.

Where the filtering happens, and why it differs per surface:
- **Search** sends `cost_min` / `cost_max` to the Worker, which adds a `reported_cost` clause to the SoQL. Not filtered in the browser: `/api/permits` caps at 1000 rows ordered by `issue_date DESC`, so a client-side filter would silently drop every match outside that first page.
- **Map Search** filters the already-loaded month shards in the browser on `row.c`. The shards are cached per month, so pushing the range into the Socrata query would break that cache for no gain.
- A permit with **no** reported cost drops out once either bound is set — it cannot be shown to sit inside a range.
- `min > max` shows an inline `role="alert"` error beside the fields on both pages. Deliberately **not** `#map-status-strip`: that strip is `display: none` below the mobile breakpoint, so the existing "Choose a valid date range." error is already invisible on a phone (worth its own card if you want it fixed).

**Checklist:**
- [x] Add value-range input to Search filters
- [x] Add value-range filter to Map Search
- [x] Ensure indexes expose reported cost efficiently
- [x] Verify results match range on both tools
- [x] ui-ux-pro-max at design time and again before landing (desktop + iPhone 13, both themes)
- [x] Merge to main and verify on production

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)
- 2026-07-31 14:20 CT — status → in-progress; starting design pass (Claude Code)
- 2026-07-31 14:39 CT — implemented on `feat-021-permit-value-range` (`9fa3c37`), pushed. No index work was needed: `reported_cost` was already in the `$select` for both the Worker query and the map's Socrata fetch. Also moved `permits.js` off its `index.js` import to a local `json()` helper (same pattern as profiles.js) — importing index.js pulls in `cloudflare:workers`, which `node --test` cannot load, so the endpoint had no tests at all before this. Verified: 6 new Worker tests (164 total pass), 128 unit tests, and `verify-tmp/t49-value-range.js` — 68 assertions across desktop and iPhone 13, each confirmed to FAIL against the un-fixed code. The pre-landing UI pass caught one real defect the assertions missed: `.controls > p { order: 8 }` outranked the error's own rule and parked the message below the Search button, a screen away from the fields; fixed and now asserted by layout position, not DOM order. Raised FIX-025 for a pre-existing issue measured along the way. (Claude Code)
- 2026-07-31 14:51 CT — **DONE, live.** Deployed the Worker first (version `8c859f74`), then merged `--no-ff` to main (`03477ee`); Pages build 2m25s. Worth recording: the first post-deploy probe said the filter was NOT working — `cost_min=999999999` still returned 50 rows and a banded query came back with null costs. That was propagation lag, not a bug; re-probed a minute later and it was correct. **A probe run seconds after "Deployed" tests the old version** ([[verify-at-the-destination]] applies to timing, not just destination). Verified against live data: a 1000-row band query returns every row inside 200k–250k with zero nulls, a min-only bound of 5M holds at the floor across 479 rows, an unbounded query is unchanged, and the ward filter is unaffected. Then drove the real production site headless — 10/10 on desktop and iPhone 13: Search rows all inside the band, the min>max error renders beside the fields, and the Map filter narrows the set with every row above the floor. Also raised FIX-026 (the "Reported cost" sort is a no-op in the two profile modes), noticed while reading `sortRows` for this work. (Claude Code)

### FEAT-027 · Integrate HighLevel CRM

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

Connect the Search Tool to HighLevel (GoHighLevel) CRM so contractor/sub profiles and permit-derived leads can flow into CRM pipelines. Context for humans, not a Claude Code deliverable: the larger plan this enables is identifying general contractors / open subs running 20+ simultaneous jobs as candidates for business buy/sell outreach — this task covers only the CRM integration groundwork.

**Checklist:**
- [ ] Review HighLevel API (auth model, contacts, opportunities/pipelines, custom fields, rate limits)
- [ ] Decide sync direction and scope: push GC/sub profiles and selected permits as CRM contacts/opportunities with custom fields (open jobs, specializations, license match)
- [ ] Design where the integration runs (the site is static — likely an export/sync script, scheduled workflow, or the Worker rather than in-browser)
- [ ] Implement an export path for a filtered set (e.g., GCs with ≥ N open jobs) into HighLevel
- [ ] Handle credentials safely — no API keys in the public repo or client-side code
- [ ] Verify a test batch lands correctly in a HighLevel pipeline

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)

### FEAT-031 · My Permit List: filter by visited / called

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-08-04 10:23 CT
- **Tags:** Chicago Permit Search Tool

In a list in My Permit List (`docs/list.html`), let people filter permits by whether someone has visited or called them. The visited checkmark (FEAT-008) and the Call action (FEAT-025 cards) already exist — this adds a tracked "called" state alongside visited and exposes both as list filters.

**Checklist:**
- [x] Track a "called" state per permit, set when the Call action is used and manually togglable like the visited checkmark
- [x] Add filter controls to the list view: all / visited / not visited / called / not called (combinable) — *"all" needs no chip of its own: pressing the active chip clears its facet, so every chip is its own escape route*
- [x] On shared lists, reflect visit/call state consistently for everyone viewing the list; show who acted where the data allows — *the data did not allow it before; flags now store the actor's name instead of a bare 1*
- [x] Make filters play well with reordering, route optimization, and exports (filtered view should not silently change export scope without saying so) — *already true by construction from FEAT-034; guarded by a fresh assertion rather than assumed*
- [x] Verify on desktop and mobile — 116 assertions across desktop + iPhone 13, plus a 60-check a11y sweep
- [x] Split the single "Visited/Called" column into two (added — one control for two facts was the thing this card exists to separate)
- [x] Raise the checkbox hit target to 44px (added — measured at 38px, and this doubles the number of them)
- [x] Deploy the Worker, then merge (deploy-order hazard — Worker deployed by Divyam and confirmed live BEFORE the merge)
- [ ] **Verify a shared list with two real viewers on two devices — still open.** The sync path is covered by unit and headless tests, and the Worker is live, but a genuine two-device check has not been done. Flagged rather than counted as passed.

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)
- 2026-08-04 09:38 CT — status → in-progress. Read the existing code first: **FEAT-034 already built the seat this feature sits in.** `state.listFilters` is an object, the filter bar is a `role="group"` explicitly commented as the place FEAT-031's chips join, `visibleListRows()` is a VIEW filter only (exports/routing/drive-times keep reading `userListRows()`), reordering is already locked with `aria-disabled` while filtered, and the Worker's `ticks`/`follow` flag endpoints share one handler over one list document. So "called" is a third flag of the same shape, not a new subsystem (Claude Code)
- 2026-08-04 10:16 CT — **BUILT on branch `feat-031-visited-called-filters` (`c8d4c96` spec, `aa55401` Worker, `f678ada` client), pushed, NOT merged, Worker NOT deployed.** Design-time `ui-ux-pro-max` pass first, folded into `docs/superpowers/specs/2026-08-04-visited-called-filters-design.md`; a second pass before landing. Worker: `called` is a third per-key flag beside `ticks`/`fu`, and the three cases in `applyOp` collapsed into one since the only difference was which map they wrote (Claude Code)
- 2026-08-04 10:16 CT — **the single "Visited/Called" column became two.** One checkbox for two different facts was exactly what this card exists to separate. The new cell reuses `.tick-cell` rather than taking a class of its own, which is what makes it a zero-new-CSS change: the mobile stack rules are written against that class — `order: 2` (directly under the permit number), flex row, and a `::before` that prints `data-label` as the inline label. **A fresh `.call-cell` would have fallen into the default `order: 3` bucket and stacked at the BOTTOM of the phone card, separated from the box it pairs with.** Caught at design time, not after building it (Claude Code)
- 2026-08-04 10:16 CT — chips are **mutually exclusive within a pair, combinable across pairs**. A permit cannot be both visited and not visited, and offering the contradiction only to render a guaranteed-empty table is a dead control; across facets they compose, which is the question the field actually asks — visited + not called = "been there, nobody has phoned yet". Called is set by hand AND automatically when a `tel:` link is used from inside a permit card, via **one delegated listener** rather than an onclick threaded through the three templates that render a phone number, so a fourth added later cannot silently forget. Deliberately NOT set from a contractor card: a call placed from a firm's own profile is not about any one of its permits, and ticking one would be a guess (Claude Code)
- 2026-08-04 10:16 CT — **"show who acted" needed a data change, so it got one.** A flag stored `1`; it now stores the actor's name (the one the notes feed already collects), falling back to `1` when blank. `1` stays truthy, so **every list stored before this keeps working and simply has no name to show — no migration**. It reaches the checkbox `aria-label` and `title` and two new CSV columns (`visited_by`, `called_by`), never colour or hover alone. The generic list `PUT` carries `called` across from storage rather than the body, so renaming a list cannot wipe the team's call log — the rule `fu` already had, now with a test (Claude Code)
- 2026-08-04 10:16 CT — **two numbers measured rather than assumed.** (1) `.tick` was a **38px** hit target (22px box + `.5rem` margin), under the 44 floor, and this change doubles how many of them there are; `margin: .6875rem` makes it exactly 44. (2) Chip contrast, both themes, both states: `--accent` 5.36:1 light / 9.76:1 dark, `--t5` 7.76 / 8.61. The live browser probe then reproduced 7.76 and 8.61 **exactly**, which is a useful check that the static calculation modelled the real cascade (Claude Code)
- 2026-08-04 10:16 CT — **three probe traps, each of which reported a clean failure for working code.** (1) The contrast probe measured 80ms after a theme switch and caught the chip **mid-transition** at `rgba(142,184,255,0.706)`, reporting **4.26:1 for a colour that settles at 8.61:1**; wait on `getAnimations()`, never a fixed delay — **and the control written to prove the probe discriminates fell into the same trap**, reporting the unpoisoned value until the poison was applied with `transition: none`. (2) A `display:none` table cell reports `top: 0`, which reads as "above everything" in a stacking-order assertion; at 390px this table hides four columns. (3) `docs/list.html`'s git blob is **CRLF**, so a multi-line `"...\n..."` anchor in the mutation script silently never matched and the mutant was reported as *skipped* rather than failing (Claude Code)
- 2026-08-04 10:16 CT — **two existing suites went red BY DESIGN and were updated, not silenced.** `t47-visitedlabel` is FIX-018's guard and asserted the header reads `"Visited/Called"` — that single column is what this card splits; its real requirement (a visible, legible, non-overflowing word label) is unchanged and is now asserted for BOTH columns. `t44-followup` and `t45-uiux-followup` used a bare `.pm-fu` selector, which the new call toggle also matches, so they were silently driving the wrong button — fixed at the source too: **the follow-up button now carries `.pm-followup`**. Separately, `verify-tmp/pb-reducer-impl.mjs` claimed "AUTO-EXTRACTED" but was a hand copy that **had already lost FEAT-034's `fu` case**, so the live-sync reducer had been tested against a stale transcription for weeks; it now extracts from `docs/list.html` at test time and covers all three flags (Claude Code)
- 2026-08-04 10:16 CT — verification. **190 Worker + 175 client unit tests**, `verify-tmp/t57-visited-called.js` at **116 assertions** across desktop and iPhone 13 (renamed from t54, which collided with FIX-028's suite), `_t57-audit.js` at 60 a11y checks, and `_feat031-mutants.js` at **10/10 caught** — each predicate broken in turn on a working build, because a suite that only aborts on missing markup has not tested behaviour. Full browser sweep: 65 scripts, all green (t44's one red in the batch was the documented `:8791` port contention — it passes in isolation, unlike t45, which was a real failure and is fixed). CSV column alignment asserted too, since header and row are two separate literals (Claude Code)
- 2026-08-04 10:16 CT — **DEPLOY-ORDER HAZARD, verified against production rather than assumed.** `GET https://chi-permits-api.divyam-c-karuri.workers.dev/` still advertises `PUT /api/lists/:id/ticks | /follow` with no `/called`, so the deployed Worker predates this. Merging the client first means every call mark stays local and never reaches a shared list — not destructive (it resyncs later), but silently single-player. **Deploy the Worker with or before the merge: `npx wrangler deploy --config wrangler.toml` from `worker/`** — the bare `npx wrangler deploy` is not safe in this repo. Same class as FEAT-034's hazard. This is also why the "shared list with multiple viewers" checklist item is still open: it cannot be honestly verified until the Worker is live. **Awaiting approval to merge** (Claude Code)
- 2026-08-04 10:23 CT — **DONE, merged and live.** Divyam deployed the Worker; confirmed at the destination before merging rather than taken on trust — the API now advertises `PUT /api/lists/:id/ticks | /follow | /called` and returns `called` in the list shape. Existing data re-read after the deploy: reference list `PeeXTko` still holds **99 permits**, `called` present and empty, ticks and follow-ups untouched. Merged `--no-ff` (`abe825f`), branch deleted, Pages rebuilt. Re-verified on the MERGED tree before pushing — 190 Worker + 175 client unit tests, t57/t44/t45/t47 and the a11y sweep all green (Claude Code)
- 2026-08-04 10:23 CT — one item deliberately left unticked: **a real two-device check of a shared list has not been done.** The sync path is covered by unit tests, the reducer tests, and headless runs, and the Worker is live, so there is no known gap — but "two people watching one list on two phones" is not something these suites actually prove, and marking it passed would be a claim I have not earned (Claude Code)

### FEAT-024 · Map Search: filter out work types and filter to residential only

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 15:53 CT
- **Updated:** 2026-08-03 11:12 CT
- **Tags:** Chicago Permit Search Tool

In Map Search (`docs/map.html`), let the user exclude certain types of work and narrow results to residential properties only. FEAT-013 (building type) already supplies the residential signal; this exposes it as a map filter.

**Checklist:**
- [x] Enumerate the work types present in the permit data and pick the filterable set
- [x] Add a work-type exclude control to Map Search
- [x] Add a residential-only toggle, defining which building types count as residential — *delivered as a three-option select rather than a toggle, and keyed on ZONING DISTRICT rather than building type; see the log*
- [x] Verify both combine correctly with the existing month and value-range filters
- [x] Check performance with filters applied across the monthly map shards — *the shards no longer exist (the map fetches Socrata directly since the Worker migration), so this became: how long does classifying a month of permits take. 11ms for 2,384 points, plus a one-off 104ms parse + 77ms index*
- [x] Persist both filters and apply them on first render after a reload (added — they sit behind a collapsed drawer, so a restored filter that only half-applies is invisible)
- [x] Degrade safely when the zoning file cannot be loaded (added)
- [x] Un-clip the Neighborhood / street field, which carried the same specificity bug (added at Divyam's request; pre-existing, folded into this branch rather than split off)
- [x] Merge and confirm on the live site

**Log:**
- 2026-07-27 15:53 CT — created (Divyam)
- 2026-08-03 09:22 CT — status → in-progress on branch `feat-024-map-work-type-residential`. Design spec committed (`6bb1ef7`, `docs/superpowers/specs/2026-08-03-map-work-type-residential-design.md`) after a design-time ui-ux-pro-max pass (Claude Code)
- 2026-08-03 09:22 CT — checklist item 1 answered, and it changed the control: **`work_type` exists only on Express Permit Program permits.** Trailing 12 months of open permits — Express 14,798 (20 distinct labels), Renovation/Alteration 4,812 and New Construction 1,466, both with `work_type` ALWAYS blank. A control offering only Socrata's labels could not exclude renovation or new construction, which is 30% of permits and the two categories most worth isolating. The filterable set is 22: the 20 labels plus two synthesized from `permit_type`. Also noted: `Porch,Deck,Balcony,or Fire Escape` is ONE label containing literal commas — never split this field on commas (Claude Code)
- 2026-08-03 09:22 CT — **the residential signal changed source at Divyam's suggestion, and the data backs him decisively.** The checklist assumed FEAT-013's `permitUse()` text heuristic. Measured over July 2026 (2,384 open geocoded permits) it classifies only 32% and can prove residential for just 623 (26%) — the permits dataset has no occupancy field, and an `OCCUPANCY:` label appears in only 73 descriptions, almost all Business/Utility/Education. Divyam asked why not use the zoning districts the map already draws. Point-in-polygon against the shipped `docs/data/zoning.geojson` classifies **99.8%** (5 rows city-wide fall in no district) and finds **1,496 residential (62.8%)**; 1,084 permits the text called "unclear" sit in RS/RT/RM. Cost is affordable — 5.0 MB raw / ~850 KB gzipped, already lazy-loaded for the Zoning Districts layer, and measured at 104ms parse + 77ms index + **11ms to classify all 2,384 points**. `permitUse()` is NOT modified; it still labels individual permits on index/list, which is a different question (what the work says) from what this filter asks (what the property is) (Claude Code)
- 2026-08-03 09:22 CT — zoning states what a district ALLOWS, not what is built: B1–B3 are storefronts with housing above, and real housing work sits there (a B3-5 fire alarm reading "AFFECTS: 40 DWELLING UNITS", plumbing replacements in B3-2/B3-3). Strict RS/RT/RM would drop ~200 permits a month of genuine residential work, so Divyam chose a two-step select — All / Residential zoning only (RS, RT, RM, DR ~63%) / Residential + business (adds B1–B3, ~71%) — rather than one toggle. Work-type control is a collapsed `<details>` checklist, default nothing excluded (Claude Code)
- 2026-08-03 10:08 CT — **built on branch `feat-024-map-work-type-residential` (`1233a27`, pushed, NOT merged — awaiting approval).** Client-only, `docs/map.html`; no Worker deploy needed. The zoning index is built from the file the zoning LAYER already lazy-loads, now shared through one cached promise so the ~850 KB is fetched at most once whichever consumer asks first. Permits in no district at all are KEPT rather than dropped, per [[chi-permits-neighborhood]]'s never-invent-a-classification rule; a failed zoning load turns the filter off and says so in the status strip instead of emptying the map (Claude Code)
- 2026-08-03 10:08 CT — **three defects were invisible to 45 passing assertions and only the screenshots caught them.** (1) Below 640px `.map-filter-grid` is a FLEXBOX, not a grid, so `grid-column` was silently inert — AND a bare `.map-use-field` (0-1-0) loses to `.map-filter-grid label` (0-1-1), so the select rendered at 50% and clipped to "Residential zoning o". That is the FIX-025 specificity trap a second time; the fix needs `.map-filter-grid .map-use-field`. (2) The global label styling uppercased all 22 work-type names, shouting, and inconsistently with the layer toggles directly beneath them — `.check-row` opts out of this and the new rows did not. (3) The bounded list cuts off mid-row with nothing to say more exists, so the summary now reads "3 of 22 excluded" rather than "3 excluded". **`.map-neighborhood-field` has defect (1) exactly — its full-width rule loses the same specificity fight, so "Search area, id, or street" is clipped on every phone today. Initially left out of scope; FIXED on this branch at Divyam's request — see the 10:26 entry.** (Claude Code)
- 2026-08-03 10:08 CT — a fourth defect the suite caught: the zoning-failure message was written straight to `#map-status-strip` inside `applyMapFilters`, which `renderMapSideList` rewrites moments later — so the fallback was silent AND the strip went on naming a property-use filter the map was not applying. Now carried on `state.map.propertyUseFallback` and rendered where the strip is actually composed (Claude Code)
- 2026-08-03 11:12 CT — **DONE, live.** Merged to `main` (`568d695`, `--no-ff`) after FIX-027, branch deleted, Pages rebuilt. Client-only, no Worker deploy. Re-verified on the merged tree BEFORE pushing, because FIX-027 touched `map.html` in the same release: 152 client + 164 Worker unit tests and all six directly-affected suites green (t52, t53, t28, t43, t42, t45). Then driven against the LIVE site with real Socrata data — **and the live behaviour matches the measurement this was designed from: 1,507 of 2,384 July permits survive the residential filter, 63.2%, against the 62.8% predicted.** Not just a plausible count either: 40 surviving permits were spot-checked back through `zoneCategoryAt` and every one is genuinely in an RS/RT/RM or DR district. The synthesized "Renovation / alteration" and "New construction" entries are present in the live checklist, excluding a work type really removes those rows, the status strip names the active filter, and there are zero page errors (Claude Code)
- 2026-08-03 10:26 CT — `67e1d19` on the same branch: the `.map-neighborhood-field` clipping noted above is FIXED here rather than split into its own card, at Divyam's request. It had the identical bug — written as a bare class (0-1-0) it was outranked by `.map-filter-grid label` (0-1-1), so the rule had **never once taken effect** and the field sat at 50% on every phone with "Search area, id, or street" clipped mid-word. Both full-width fields now share one rule scoped to `.map-filter-grid` (0-2-0). **That makes three times this specificity trap has bitten `docs/map.html`** — twice in FIX-025, once here — so the rule now carries a comment telling the next reader to measure after touching it. Intended visible side effect: with neighborhood correctly full-width, "Radius (miles)" sits alone on its row instead of paired with it. Guarded by two new t52 assertions measuring the input against its own placeholder's rendered width, placed beside the equivalents for the select so the pair cannot regress apart; the visual control re-breaks both rules together and catches 4/4. t52 is now 53/53 (Claude Code)
- 2026-08-03 10:08 CT — verification. `verify-tmp/feat024-zone.mjs` (22 unit tests) extracts the functions from `docs/map.html` **at test time** rather than hand-copying them into a `-impl.mjs` like the sibling suites — those static transcriptions can drift, and a test agreeing with a stale copy proves nothing ([[a-fixture-is-a-claim-about-production]]). `verify-tmp/t52-worktype-residential.js` is 51 assertions across desktop and iPhone 13. Both fail against the pre-change tree, but only by aborting on the missing markup, so the behavioural half was proven separately: `_t52-mutants.js` breaks each predicate in turn on a WORKING build (property-use always-pass, always-fail, exclusion no-op, blank buckets dropped) — 4/4 caught — and `_t52-visual-control.js` restores each broken style — 3/3 caught. The contrast probe needed its own control and was wrong at first: it read `color(srgb 1 1 1 / 0.96)` components as 0–255, turning the drawer's white background into near-black, and reported 3.30:1 for text that measures 6.31:1. Real figures 6.31:1 light / 8.54:1 dark. 151 client + 164 Worker unit tests pass; 58/61 browser scripts green — t28 and t43 fail identically with and without this change, and t27 passes 3/3 in isolation both ways (it only fails under back-to-back runs on the shared port) (Claude Code)

### FEAT-032 · Feed the search conditions/filters into the list description

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-08-07 09:30 CT
- **Tags:** Chicago Permit Search Tool

When permits are pulled into a list from Search or Map Search, record the conditions and filters that produced them (ward, date range, work types, value range, etc.) in the list's description, so anyone opening the list later can see how it was built.

**Checklist:**
- [x] Capture the active filters/conditions at the moment permits are added or a list is pulled
- [x] Render them as a compact human-readable summary in the list description (e.g. "Ward 47 · Jun–Jul 2026 · renovation excluded · $50k–$250k")
- [x] Append rather than overwrite when adds come from different searches; keep the description editable by hand
- [x] Show the summary on shared/opened lists too
- [x] Verify with adds from both Search and Map Search, and with manually added permits (which should note no filters)
- [x] Render the description on the list itself — it was previously only visible in the Edit-details dialog and on the directory card

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)
- 2026-08-05 09:51 CT — started; branch `feat-032-list-provenance` (Claude Code)
- 2026-08-05 10:29 CT — implemented. Provenance is stored **in the description** rather than in a field of its own: the description already syncs to the shared doc, renders on the directory card and is hand-editable, so a parallel "sources" store would have meant building all three again. Each add appends one line, e.g. `• Aug 5 — 12 from Permit Map: Jul 1–Aug 5, 2026 · $50k–$250k · 1 work type excluded`; a hand-typed stop records `added by hand: no filters`. A repeat add from the same search on the same day bumps that line's count instead of stacking a duplicate; a different search always appends. Only the last line is ever rewritten, so hand-written text is never touched, and past the 2000-char cap the OLDEST provenance is evicted rather than the string being sliced (Claude Code)
- 2026-08-05 10:29 CT — the description had no on-page surface at all, so "show it on shared/opened lists" needed one built: read-only block under the list title, clamped to 3 lines with a Show more/less expander (a 2000-char description would otherwise push the toolbar off the first screen) (Claude Code)
- 2026-08-05 10:29 CT — Search and the Permit Map hold no live socket, so a description appended there would have been overwritten by the room's older copy on the next `state` frame. Appends set `descPending`; `list.html` holds the local text across that frame and pushes it as a `meta` op. **Known gap:** the KV directory blurb still only refreshes on an Edit-details save, so a shared list's card in "All lists" can show a stale blurb until then (Claude Code)
- 2026-08-05 10:29 CT — verified: 20 unit tests (`verify-tmp/feat032-source.mjs`, extracted from the shipped source at test time, incl. a check that the block is byte-identical on all three pages) with a 6-mutant control proving they discriminate; 29 browser assertions (`verify-tmp/t64-list-provenance.js`) at desktop + iPhone 13 covering both add paths, the manual add, clamp/expand, Tab-reachability, Enter activation, 44px target, no h-scroll, and 4.5:1 contrast in both themes (measured 6.32:1 light / 8.51:1 dark; probe proved to discriminate by a poisoned control run) (Claude Code)
- 2026-08-05 10:29 CT — filed **FIX-034**: `index.html`/`map.html` still carry the full-list data-loss bug FEAT-035 fixed in `list.html`. Worked around here (the count records what actually landed) rather than fixed, because it changes add semantics on two pages (Claude Code)
- 2026-08-05 10:45 CT — caught a bug of my own in review: the expanded state persisted across a change of list, so a second list opened pre-expanded reading "Show less". Now reset on a change of list only — resetting on every repaint would have collapsed the description mid-read, since this also runs after each add and on every live frame. Regression test added and proved to fail against the bug (Claude Code)
- 2026-08-05 10:49 CT — **done.** Commit `9707131` on branch `feat-032-list-provenance`, pushed. Full browser sweep run (73 scripts): 70 green; the 3 reds — `t9`, `t40-mapstate`, `t63-sparse-matrix` — were each re-run in isolation and fail identically on `main`, so none is caused by this change (`t63` belongs to the parked FEAT-039 work). Worker suite 200/200. **Not merged — awaiting approval** (Claude Code)
- 2026-08-07 09:30 CT — **backfilled from git: this was merged and the card never said so.** `feat-032-list-provenance` went to `main` as merge `aaf598b` on 2026-08-06 and is pushed (`main` == `origin/main` == `91a5116`); the branch is gone from both local and `origin`. Same failure as FEAT-039 — the line above still read "Not merged — awaiting approval" while git had it merged (Claude Code)

### FEAT-028 · Classify permit lenders: private/small lender vs small, medium, or large bank

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

For the lender recorded on a permit (builds on FEAT-023), determine whether it is a private mortgage or small lender, and label it as a private/small lender or a small, medium, or large bank.

**Checklist:**
- [ ] Pick a classification source (FDIC/NCUA institution data for banks/credit unions by asset size; NMLS for non-bank lenders; unmatched → private/small)
- [ ] Define the size thresholds for small / medium / large bank and document them
- [ ] Normalize and match lender names against the classification source
- [ ] Add the lender-size label wherever lenders are displayed (FEAT-023 surfaces)
- [ ] Verify a sample of known lenders classifies correctly, including private-money edge cases

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)

### FEAT-029 · Property intelligence: STR/Airbnb licensees cross-referenced with MLS listing history, zoning, HOA rules, and deed/LLC/licensing records

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-08-06 09:19 CT
- **Tags:** Chicago Permit Search Tool

Consolidates FEAT-026 (deed/title, MLS, LLC, VA loan, IDFPR enrichment), FEAT-029 (Airbnb/short-term-rental licensee layer) and FEAT-030 (HOA locations, fees, rental rules) into one card — they were three views of the same join: take an address or PIN and say **what this property is, what it is allowed to be, and what it has been marketed as**. Both source cards are in the Archive with their bodies intact; their IDs are retired.

The STR layer on its own answers "where is Airbnb density concentrated" and nothing more. Cross-referenced with MLS listing history (list/delist cycles, price cuts, days on market, sale history, whether it was ever marketed as an investment or furnished/short-term unit), zoning, and HOA rental rules, the same layer answers the question actually worth asking of a permit or a parcel: is this property being run as a short-term rental, could it be, and is the owner someone who wants a property manager.

**Sequencing:** the source-evaluation gate comes first and MLS is the one with real constraints — IDX/RETS/RESO feeds carry redistribution and display terms, and an unlicensed scrape is not an option. Settle terms before anything is built on it. Zoning is the cheapest piece and already shipped: `docs/data/zoning.geojson` is loaded for the zoning layer and indexed by FEAT-024, so the zoning half of this card is a join, not an ingestion.

**Checklist:**
- [ ] Evaluate every source before building: access method, Chicago coverage, cost, and terms of use — City shared-housing/STR registrations; MLS (which feed, what redistribution/display terms, what listing *history* depth is actually licensed); Cook County Recorder of Deeds for deeds, mortgages, liens; IL Secretary of State LLC registrations; VA loan records; IDFPR licence lookup; HOA sources (MLS association/fee fields, county records, condo declarations). Rank by enrichment value vs. effort and write the findings in this task's Log
- [ ] Design the join keys per source: PIN/address for STR, MLS, deeds and HOA (the permits dataset already carries `pin_list`, the key FEAT-025 uses to reach the Assessor's parcel universe); name normalization for LLC/IDFPR, mirroring the licensed-contractor match
- [ ] Ingest the City STR/shared-housing registrations with locations and export a map-ready index
- [ ] Add the STR layer to Map Search: density view (clusters or heat) plus per-licence markers, licence details in the popup for outreach, respecting existing filters where sensible and persisting with the remembered map state (FIX-008 / FIX-035)
- [ ] Add MLS listing history per property: current status, list and delist events, price changes, days on market, sale history, and any signal that it was marketed as furnished / short-term / investment. History over snapshot — a single current listing state is not what this card is for
- [ ] Cross-reference STR licensees against zoning using the already-shipped `zoning.geojson` index rather than a new fetch, and show the district alongside the registration
- [ ] **Do not compute a legality verdict.** Chicago's shared-housing rules live in the ordinance and in per-precinct/per-building restrictions, not in the zoning district code, so district + registration status can be shown side by side but "this STR is illegal" cannot be derived from them. State what each source says and leave the conclusion to the reader — same rule as [[chi-permits-neighborhood]]'s never-invent-a-classification and FEAT-025's zoning-vs-Assessor split
- [ ] Associate permits and addresses with an HOA where one exists; show HOA presence and fee amount on permit detail and list pulls, and add a rentals-allowed check where the data supports it — "unknown" shown honestly wherever it does not
- [ ] Ingest the approved deed/title, LLC, VA loan and IDFPR sources into the pipeline and export the enriched fields into the JSON indexes (FIX-015 already surfaces whatever person-in-charge data exists today; the deeper LLC manager/registered-agent enrichment belongs here)
- [ ] Surface every enrichment with a per-source caveat naming the source and its vintage — an MLS field and a Recorder field carry very different confidence and must not read alike
- [ ] Keep per-property enrichment an on-demand cached lookup, never a bulk fetch across a result set — the constraint FEAT-025 established for the Assessor class applies to all of these, and a table column is a bulk fetch by another name
- [ ] Verify a sample against each source of record: density hotspots against known short-term-rental neighborhoods, fees and rental rules against known condo/HOA buildings, and listing history against a handful of properties whose sale history is independently known

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)
- 2026-08-06 09:19 CT — expanded at Divyam's request to cross-reference MLS listing history and zoning, and consolidated with FEAT-026 and FEAT-030 into this single card. FEAT-026 and FEAT-030 moved to the Archive with full bodies preserved; their IDs are retired and must not be reused. FIX-015's pointer to FEAT-026 for deeper LLC ingestion now points here (Claude)
- 2026-08-06 09:19 CT — scope note carried over from FEAT-030: the HOA rentals-allowed check was always dependent on the MLS source that was in FEAT-026, which is why the two are now one card rather than two with a cross-reference between them (Claude)

### FEAT-017 · Address search for permits

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Search permits directly by street address.

**Checklist:**
- [ ] Add address input to search UI
- [ ] Match against permit address data (handle partial/fuzzy matches)
- [ ] Show matching permits with links to detail
- [ ] Verify against known addresses

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FEAT-018 · Search tool scope expansion and parity with Map Search tool

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Bring the Search tool's filters/data scope up to parity with what the Map Search tool offers, and expand scope where the two diverge.

**Checklist:**
- [ ] Inventory filters/data available in each tool
- [ ] Close the gaps in the Search tool
- [ ] Verify both tools return consistent results for the same query

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FEAT-019 · Map tool icons based on permit type

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:28 CT
- **Tags:** Chicago Permit Search Tool

Map markers should display a different icon depending on the permit type of the underlying permit.

**Checklist:**
- [ ] Enumerate permit types present in the dataset
- [ ] Design one distinct icon per permit type (plus a fallback for rare/unknown types)
- [ ] Implement icon selection on Map Search markers
- [ ] Add a map legend mapping icons to permit types
- [ ] Verify legibility at all zoom levels and on mobile

**Log:**
- 2026-07-27 10:09 CT — created; blocked pending spec of what icons are based on (Claude)
- 2026-07-27 10:28 CT — unblocked: Divyam confirmed icons are based on permit type; status → todo (Claude)

### FEAT-020 · Map tool compatibility fixes

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Resolve browser/device compatibility issues specific to the Map Search tool.

**Checklist:**
- [ ] Test map rendering and interactions across browsers and mobile
- [ ] Fix issues found and log them here
- [ ] Verify month filter and markers behave consistently

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FEAT-022 · Historical map of a General Contractor's work

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

From a GC's profile, view a map of their past permits/projects over time.

**Checklist:**
- [ ] Aggregate permits per GC with locations and dates
- [ ] Map view (reuse MapLibre) filtered to one GC, with time dimension
- [ ] Link from contractor profile
- [ ] Verify with a high-volume GC

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FEAT-023 · Display lenders on projects and their associated GCs

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Surface lender information on projects and connect lenders to the GCs they work with.

**Checklist:**
- [ ] Identify data source for lender info
- [ ] Show lender on permit/project detail
- [ ] Cross-reference lenders ↔ GCs
- [ ] Verify sample projects

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FEAT-033 · Rich link previews for shared permit lists (Slack, texts, social embeds)

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-29 13:18 CT
- **Updated:** 2026-07-29 13:18 CT
- **Tags:** Chicago Permit Search Tool

When a shared permit-list link is posted in Slack, a text message, or social apps, the unfurled preview should show the list's relevant information (name, permit count, description) instead of a generic page title. Key constraint: link crawlers don't run JavaScript, so per-list Open Graph tags can't come from the static page — the share URL needs to be served (or pre-rendered) by the Worker, which already holds shared-list data.

**Checklist:**
- [ ] Inventory what a share link looks like today and what Slack/iMessage currently unfurl for it
- [ ] Serve share URLs through the Worker: inject per-list OG/Twitter meta (og:title = list name, og:description = permit count + list description from FEAT-032, og:url) into the HTML for crawlers and users alike
- [ ] Add a sensible default OG card (site name + logo image) for all other pages
- [ ] Consider a generated preview image (permit count / area summary) as a stretch; plain text card is the baseline
- [ ] Validate with Slack unfurl, iMessage, and an OG debugger; confirm normal browsers still load the list exactly as before
- [ ] Respect privacy: only unfurl data the shared link already exposes

**Log:**
- 2026-07-29 13:18 CT — created (Divyam)

### FEAT-034 · Per-list notes feed: searchable, timestamped notes inside each permit list — with GC follow-up tagging

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 13:27 CT
- **Updated:** 2026-07-31 10:58 CT
- **Tags:** Chicago Permit Search Tool

Make notes searchable within each permit list — NOT one overall site-wide tab. Inside a specific list in My Permit List (`docs/list.html`), a notes feed opened from a control at the top of that list lays out that list's notes as a timestamped feed (newest first) with search. Each entry shows its note text, timestamp, and the permit (in this list) it belongs to. Clicking a note jumps to its associated permit, and from a permit you can jump back into the feed — navigation works to and from in both directions without losing your place in the feed. The feed's scope is always the list you're in; different lists have separate feeds.

Also includes a **follow-up tag for GCs**: from a permit, tag its General Contractor as "follow up". The tag must be apparent both INSIDE the permit view (clear follow-up marker near the GC) and OUTSIDE it (visible badge on the permit's row in the list, without opening the permit). The list gains a filter to show only permits tagged for follow-up, composing with FEAT-031's visited/called filters.

**Checklist:**
- [x] Inventory where notes are stored today (per-permit) and expose them as a queryable collection scoped per permit list
- [x] Add a notes feed entry point at the top of each permit list view (inside the list, not a global tab)
- [x] Feed view: timestamped entries for this list only, newest first, each showing note text + linked permit summary
- [x] Search within the feed (note text, permit address/number); instant filter as you type
- [x] Click a note → open its associated permit; back returns to the feed at the same scroll/search state
- [x] From a permit in the list, link into the feed filtered to that permit's notes
- [x] Decide behavior on shared lists (do viewers see the feed? consistent with how notes themselves are shared)
- [x] Follow-up tag: from the permit view, tag the permit's GC to follow up (toggleable, like visited/called)
- [x] Show the follow-up state clearly inside the permit view, adjacent to the GC it applies to
- [x] Show a follow-up badge on the permit's list row so it's visible without opening the permit
- [x] Add a "follow-up" filter to the permit list (only tagged permits), combinable with visited/called filters (FEAT-031)
- [x] Sync follow-up state on shared lists the same way visited/called sync, so the whole team sees who's flagged
- [x] Mobile: 44px touch targets, feed usable on small screens
- [x] Verify round-trip navigation and search on mobile and desktop, across multiple lists (feeds stay separate); verify tagging + filter round-trip

**Log:**
- 2026-07-29 13:27 CT — created (Divyam)
- 2026-07-29 14:11 CT — scope clarified by Divyam: the feed lives INSIDE each specific permit list, not as an overall site tab; description, title, and checklist updated (Claude)
- 2026-07-30 15:05 CT — scope expanded by Divyam: add a GC follow-up tag — visible inside the permit view and on the list row — plus a list filter for follow-up-tagged permits (Claude)
- 2026-07-30 20:58 CT — started; status in-progress. Scope settled with Divyam: the feed shows BOTH public thread posts and private per-permit notes, each labelled; on a shared list viewers see the public posts plus their OWN private notes (no new sharing surface); the follow-up tag attaches to the PERMIT and is labelled with its GC, syncing exactly like the visited tick (Claude Code)
- 2026-07-30 20:58 CT — phase 1 (data foundations) done on branch `feat-034-notes-feed` (`2f2f688`): new `GET /api/notes/bulk` so the feed costs one request instead of one per permit; `fu` follow-up flags added to the list document alongside `ticks` (shared REST handler, no revision written, never settable from a PUT body); private notes now carry an edit timestamp in a parallel `noteTs` map — pre-existing notes stay undated rather than being given a false time. Also fixed KV list() cursor-following in `/notes/counts`, which would have silently under-reported past 1000 noted permits. 158 worker tests green, up from 136 (Claude Code)
- 2026-07-30 22:14 CT — phase 2 (the feed itself) done on `feat-034-notes-feed` (`0075d7e`): Notes button at the top of each list opens a native <dialog> feed of that list's notes, newest first, with instant search over note text / permit number / address / author. Private notes and shared posts appear together, each badged in WORDS (not colour alone); walkthroughs and photo posts render as prose instead of blank rows; notes with no recorded time say so and sort last rather than masquerading as newest. Round trip verified: tapping a note opens its permit and coming back restores both the search text and the scroll position, driven against a real 40-note overflow. Two distinct empty states (no notes yet vs no search matches). Shared-list behaviour per Divyam: viewers see the public posts plus their own private notes — no new sharing surface (Claude Code)
- 2026-07-30 22:14 CT — ui-ux-pro-max pre-landing pass caught two REAL defects, both fixed: the Material Symbols stylesheet is fetched with an explicit `icon_names` allowlist and none of the feed's icons were declared, so close/lock/group/sticky_note_2 would have rendered as their literal names in production — invisible to any DOM-level assertion; and "close" as literal text measured 100px against a 44px button, pushing the header 12px wide. Guard `t42-uiux-feed.js` now fails on any undeclared icon (verified against the bug) and checks 44px targets, the 16px input floor, contrast in both themes, real-Tab focus rings and horizontal overflow across desktop + iPhone 13. Guard `t41-notes-feed.js` covers the feed behaviour; both restoration guards verified to fail when the restore is reverted. 158 worker + 128 client unit tests, 51/51 applicable browser suites (Claude Code)
- 2026-07-31 09:40 CT — phase 3 (the GC follow-up tag) done on `feat-034-notes-feed` (`4f34ed2`): flag a permit for follow-up from inside its card, directly under the general contractors the flag is about, and see it from outside the card as a worded badge on the list row. New "Follow-up only" filter chip on the list. The flag attaches to the PERMIT and is labelled with its GC rather than to the contractor company — flagging the firm would mark every one of its permits at once, a much larger feature. Keyed exactly like a visited tick and riding the same (now generic) flag-sync queue to the Worker `/follow` endpoint from phase 1, so shared lists sync it the same way. The filter is a VIEW filter only: exports, drive distances and Optimize route all keep reading the full list, so narrowing the view can never quietly narrow what gets routed; reordering is locked while filtered (aria-disabled, not disabled, so the buttons stay focusable and can say why) because the move offset acts on the full list (Claude Code)
- 2026-07-31 09:40 CT — ui-ux-pro-max pre-landing pass caught two more REAL defects, both fixed before landing: `flag` was missing from the Material Symbols `icon_names` allowlist, so in production the badge and the toggle would both have rendered the literal word "flag" — the same class of bug as phase 2, now guarded again; and the filter chip reused the directory's `button.tag` rules, which are driven entirely by `--tc`, so without naming a colour it rendered panel-on-panel at exactly 1.00:1 in both themes. Guards `t44-followup.js` (behaviour, desktop + iPhone 13) and `t45-uiux-followup.js` (geometry + WCAG contrast, 2 viewports x 2 themes). 158 worker + 128 client unit tests and every browser suite green except `t43-tagchips`, which guards the still-unmerged `fix-013-019-tag-chips` branch (Claude Code)
- 2026-07-31 10:14 CT — phase 4 (close-out) done on `feat-034-notes-feed` (`9e096de`); implementation is COMPLETE, awaiting Divyam's merge call. Writing the close-out guard found one more real defect: `state.listFilters` survived a `showList()`, so switching from a list with the follow-up filter on to a list with nothing flagged showed an empty panel for a filter the user never set there — cleared on an actual list change now, verified by reverting the line (t46 fails 4 checks without it). Guard `t46-multilist.js` proves flags and filters stay separate across two lists, survive leaving and returning, and survive a reload read back from what was persisted rather than anything the test hands in; it also sweeps every visible control in the list view for the 44px floor at an iPhone 13 viewport. Full regression: 158 worker + 128 client unit tests and 53/54 browser suites green — the one exception is `t43-tagchips`, which guards the separate, still-unmerged `fix-013-019-tag-chips` branch and is not a regression from this work. NOTE for the merge: the follow-up filter chip inherits the directory's `button.tag[aria-pressed="true"]::before` glyph, which is mojibake on main and fixed on `fix-013-019-tag-chips` — merging that branch fixes the chip's pressed tick too (Claude Code)
- 2026-07-31 10:58 CT — MERGED to main (`3c5de2a`, --no-ff) and live on GitHub Pages; branch deleted. Status done. All 54 browser suites green on the merged tree, including `t43-tagchips` now that FIX-013/019 landed alongside — the follow-up filter chip picked up its proper tick from that fix, exactly as predicted. 158 worker + 128 client unit tests green. REMAINING: the Worker must be deployed (`npx wrangler deploy` from `worker/`) before `/api/notes/bulk` and shared-list follow-up sync work live — until then the feed falls back to private notes only and follow-up flags stay local (Claude Code)

### FEAT-035 · Permit lists: 1000-permit cap with 100-per-page pagination that remembers your page

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-29 13:50 CT
- **Updated:** 2026-08-04 13:05 CT
- **Tags:** Chicago Permit Search Tool

In My Permit List (`docs/list.html`), cap each list at 1000 permits and paginate the list view at 100 permits per page with click-through page controls. Pagination must keep its memory: clicking into a permit and coming back returns you to the same page (and scroll position), consistent with the existing last-view persistence (FEAT-025 Phase 3). Critically, pagination is a presentation layer only — Optimize Route must account for the full scope of the list (all pages, up to 1000), not just the visible page; same for exports and drive distances. FIX-004 (done on branch `fix-004-route-scope`) already un-bounded the optimizer via a tiled OSRM matrix, but set a practical ceiling of 400 stops (`MAX_SORT_STOPS`, main-thread local-search cost) — this task must reconcile that ceiling with the 1000-permit cap (raise it per FIX-004's noted path: incremental delta evaluation and/or a worker thread, or clearly message the limit).

**Checklist:**
- [x] Enforce a 1000-permit cap per list: block adds past the cap with a clear message (single adds and "Add all N" bulk adds — cap-aware partial add with a count of what was skipped)
- [x] Paginate the list view at 100 per page with page controls (prev/next + page numbers, current page and total count visible)
- [x] Persist the current page in last-view state: opening a permit and returning restores the same page and scroll position; reloads restore it too
- [x] Keep Optimize Route, drive distances, and exports (Google Maps/KML/CSV) scoped to the FULL list across all pages — verify with a multi-page list (FIX-004's tiled matrix)
- [x] Reconcile FIX-004's 400-stop optimizer ceiling with the 1000 cap: raise the ceiling (delta-evaluated local search, off-main-thread) or surface an honest limit message when a list exceeds it
- [x] Make pagination play well with reordering, visited/called state, and shared lists (viewers see consistent pages)
- [x] Check performance at the 1000-permit ceiling (render, OSRM request count, share/live sync)
- [x] Verify page memory and full-scope route optimization on desktop and mobile
- [x] Raise the Worker's own caps to match: MAX_PERMITS 220 -> 1000 and MAX_BODY 8 KB -> 64 KB, or a full list 413s on publish and loses its tail
- [x] Split the live-sync Durable Object doc across storage keys — one blob is 179 KiB worst case at the new cap, over the 128 KiB per-value limit

**Log:**
- 2026-07-29 13:50 CT — created (Divyam)
- 2026-08-04 11:45 CT — started: mapping list.html render/cap/route paths and worker list caps (Claude Code)
- 2026-08-04 12:40 CT — implemented. Pagination is a VIEW concern only: renderUserList slices what it hands to permitTable and everything else (exports, drive distances, Optimize Route, live sync) still reads userListRows(), the same contract FEAT-031's row filters hold to. permitTable gained indexOffset/total so stop ordinals keep counting across pages and the move buttons measure against the whole list. Page memory lives in the shared chi_permit_last_view key under its own listPage/listScroll/listId fields, guarded by list id so one list's page is never applied to another; index.html's search pager keeps `page`/`scroll` untouched (Claude Code)
- 2026-08-04 12:40 CT — two bugs found beyond the card's text, both fixed: (1) adding to a full list ran `next.slice(0, limit)` AFTER unshifting, which trims the TAIL — so an add silently DELETED the permits saved longest ago; it now fills to the cap and reports what was skipped. (2) "Add all N" on a contact card announced the requested count over the top of the cap message, so a capped bulk add claimed success (Claude Code)
- 2026-08-04 12:40 CT — optimizer ceiling reconciled by making the 2-opt/Or-opt local search INCREMENTAL (was rebuilding and re-summing the whole path per candidate, ~O(n^3) a pass; now ~O(n^2)). Measured 6.9s -> 0.58s at 400 stops and 1.35s at 1000, so CPU is no longer the limit. MAX_SORT_STOPS raised 400 -> 500 rather than 1000 because what binds now is the OSRM matrix at ceil(n/50)^2 requests — 100 at 500 stops but 400 at 1000, against a public demo server. Above the ceiling the existing honest message states the limit. Lifting it further means fetching fewer CELLS (sparse k-nearest, or FIX-004's noted cluster-then-route), not faster search — flagged for Divyam as a deliberate, measured choice (Claude Code)
- 2026-08-04 12:40 CT — Worker caps raised in step: MAX_PERMITS 220 -> 1000 (a unit test asserts it equals the client's userListLimit by reading both files) and MAX_BODY 8 KB -> 64 KB, without which every full list 413s on publish. The live-sync Durable Object doc is now split across doc:core/doc:ticks/doc:fu/doc:called — measured 179 KiB worst case as one value against a 128 KiB per-value limit; old rooms keep the single "doc" key until their next write, so no migration pass (Claude Code)
- 2026-08-04 12:40 CT — measured at the 1000 ceiling: open a full list 140ms, re-render 101ms, change page 248ms, 100 rows in the DOM. Verified 197 Worker + 191 client unit tests, t59 (48 assertions) and t60 (24 a11y assertions, contrast 7.76-9.11:1 in both themes with a poisoned control) on desktop AND iPhone 13. 13 mutants applied and all caught — one initially SURVIVED and exposed that nothing tested the reload restore path, which is a checklist requirement; the test was added (Claude Code)
- 2026-08-04 12:52 CT — committed to branch `feat-035-list-pagination` (e256b87) and pushed. Full browser suite: 69 of 70 green. The one red, t12, is NOT from this work — it fails 3/3 identically on HEAD on a quiet machine, and the assertion it fails (`closed.hidden`: the presence pill must hide when the socket closes) is exactly the behaviour FIX-031 deliberately inverted this morning, so t12 encodes the pre-FIX-031 contract. Raised separately rather than changed here (Claude Code)
- 2026-08-04 12:52 CT — NOT yet done: the Worker must deploy BEFORE this client change reaches Pages, or a 1000-permit list published against the old Worker is silently re-capped to 220 and loses its tail. Awaiting Divyam's go-ahead to deploy the Worker and merge (Claude Code)
- 2026-08-04 13:05 CT — Worker deployed FIRST (version d1f056b8) and verified against production before merging, end to end rather than by inference: a 17,066-byte body publishing a full 1000-permit list came back with all 1000 — the old MAX_BODY of 8192 would have 413'd that request outright and the old MAX_PERMITS of 220 would have truncated it. Both check lists were deleted afterwards (soft-delete, gone from the directory, 404 on read). Health check clean and existing user lists intact (Claude Code)
- 2026-08-04 13:05 CT — merged to main with --no-ff (44b28a6) and pushed; origin/main had an unrelated README edit which was merged in first (be8ebc9). GitHub Pages rebuilt and the live list.html was checked for every piece of the implementation AND for the absence of the three old values. Then the real production site was driven at desktop and iPhone 13: page 1 shows 100 of 250, both pagers render, stop numbers continue at 101 on page 2, route and exports still see all 250, every pager target >=44px, no sideways scroll. **DONE and live** (Claude Code)

### FEAT-036 · My Permit List: stat tiles should reflect the currently viewed list

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-30 10:42 CT
- **Updated:** 2026-07-30 10:42 CT
- **Tags:** Chicago Permit Search Tool

On My Permit List (`docs/list.html`), the "Permits Loaded", "Open Permits", "Contractors", and "Open Subs" stat tiles should be computed from the currently viewed list — a live count gathered from the permits in that list — and update in step when the viewed list changes (switching lists, adding/removing permits). Today they don't correlate with what's on screen.

**Checklist:**
- [ ] Find where the four stat tiles get their numbers today and confirm what they currently count
- [ ] Compute all four from the permits in the currently viewed list: total loaded, open (ACTIVE) permits, distinct contractors, distinct open subs
- [ ] Recompute when the viewed list changes: list switch, permit add/remove, and shared/read-only list views
- [ ] Keep counts consistent with pagination if FEAT-035 lands — count the full list, not just the visible page
- [ ] Verify on desktop and mobile against a hand-counted sample list

**Log:**
- 2026-07-30 10:42 CT — created from Divyam's report (Claude)

### FEAT-037 · Notes attached to a General Contractor: flagged under the GC in Permit View, listed in GC View

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-30 15:54 CT
- **Updated:** 2026-07-30 15:54 CT
- **Tags:** Chicago Permit Search Tool

Associate notes with a General Contractor (the person/company), not just with a permit. In the Permit View, under the General Contractor, show an indicator when that GC has associated notes (e.g. "3 notes on this contractor") so it's visible without leaving the permit. In the GC View, list those notes in full. Builds on FEAT-034's notes infrastructure (per-list feed, `GET /api/notes/bulk`, note timestamps) — coordinate with that in-progress work rather than inventing a parallel notes store: a GC's notes are naturally the notes on that GC's permits plus any notes written directly on the GC.

**Checklist:**
- [ ] Decide the association model with FEAT-034's data layer: notes written on a GC directly, plus roll-up of notes on that GC's permits — keyed on the same normalized contractor name the rest of the app uses
- [ ] Permit View: under the General Contractor line, show a clear "has notes" indicator with a count when the GC has associated notes; absent when there are none (never a zero badge)
- [ ] Make the indicator open/jump to those notes
- [ ] GC View: add a Notes section listing the GC's associated notes — text, timestamp, author, and which permit each came from (or "on contractor" for direct notes), newest first
- [ ] Respect note visibility rules from FEAT-034 (public thread posts vs. private notes; on shared lists show public + your own private ones)
- [ ] Keep it consistent on both index.html and list.html card stacks
- [ ] Verify on desktop and mobile with a GC that has notes on several permits, a GC with none, and both themes

**Log:**
- 2026-07-30 15:54 CT — created (Divyam)

### FEAT-001 · Build searchable directory of permits, contractors, and subs

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Search interface over the Chicago Building Permits dataset with type filters (General Contractors / Open Subs / Open Permits), ward filter, and sorting by open jobs, total jobs, average processing days, latest issue date, and reported cost.

**Checklist:**
- [x] Search UI with type + ward filters
- [x] Sort options wired to index data
- [x] Deployed to GitHub Pages

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-002 · Interactive permit map (MapLibre)

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Geographic visualization of permits with month filtering.

**Checklist:**
- [x] MapLibre map page
- [x] Month filter

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-003 · My Permit List with routing and exports

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Saved-permit tracking with OSRM driving-time estimates between saved permits and export to Google Maps links, KML, and CSV.

**Checklist:**
- [x] Save/track permits
- [x] OSRM route estimates
- [x] Google Maps / KML / CSV exports

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-004 · Contractor profiles

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Profiles showing public contact fields, open job counts, average processing days, work specializations, and licensing information.

**Checklist:**
- [x] Profile pages with workload metrics
- [x] Specialization + licensing data

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-005 · Data pipeline: DuckDB ingest + JSON indexes

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Scripts download the dataset into a local DuckDB database and generate compact JSON indexes for efficient client-side search.

**Checklist:**
- [x] DuckDB ingestion scripts
- [x] Compact JSON index generation

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-006 · Automated daily data refresh (GitHub Actions)

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 09:45 CT
- **Updated:** 2026-07-27 09:45 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Daily scheduled workflow pulls the latest records from the Socrata API and city contractor registries, then rebuilds the published indexes.

**Checklist:**
- [x] Scheduled workflow
- [x] Socrata + registry pulls
- [x] Auto-publish refreshed indexes

**Log:**
- 2026-07-27 09:45 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-007 · Read from permit to see type of permit

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-008 · Add visited checkmark to permits in permit list

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-009 · Add log walkthrough for chatting to owner / GCs / open subs

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Guided log walkthrough for recording conversations with the owner and/or general contractors and/or open subs.

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-010 · Add permit to permit list via address

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-011 · Add photos to permit

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-012 · Add open subs who aren't included under a permit

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-013 · Show building type (4-unit, apartment, etc.)

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Provide whether a house is a 4-unit, apartment, etc.

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-014 · Add Title under the GC

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-015 · Checkbox in log walkthrough for new build/remodel

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

### FEAT-016 · Remember last-viewed list on the list site

- **Priority:** P2-Medium
- **Status:** done
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Assignee:** Divyam
- **Tags:** Chicago Permit Search Tool

Remember what list you were last on when returning to the list site.

**Log:**
- 2026-07-27 10:09 CT — backfilled: completed prior to board creation; refine dates from git history (Claude)

---

## 🔭 Futures

> **Purpose:** Ideas outside the scope of the current project — things that may or may not become future projects or add-ons. Not actionable now. Claude Code must never implement from this list unless explicitly instructed.

### FUT-004 · Research Chicago Cityscape through its 14-day free trial

- **Priority:** P0-Critical
- **Status:** todo
- **Created:** 2026-08-06 14:02 CT
- **Updated:** 2026-08-06 14:02 CT

Sign up for the Chicago Cityscape 14-day free trial and work out what it
actually does — both as a source of features/data that could feed the Search
Tool, and as a standalone product worth understanding on its own terms.

Note the trial is time-boxed: once it starts, the clock runs 14 days, so plan
the evaluation before activating it rather than after.

**Checklist:**
- [ ] Plan what to evaluate BEFORE activating the trial (the 14 days start on signup)
- [ ] Activate the trial and record the start/end dates here
- [ ] Catalog the features, datasets and coverage it offers for Chicago
- [ ] Identify which capabilities could enrich the Search Tool, and how they'd integrate
- [ ] Assess it standalone: what it does well, where it falls short, who it's for
- [ ] Note pricing, licensing and any API/export access after the trial
- [ ] Write up findings and decide whether to pursue

**Log:**
- 2026-08-06 14:02 CT — created (Divyam)

### FUT-001 · Fill in forms for buy offers based on base price and other factors

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT

Auto-fill buy-offer forms using base price among other factors.

**Checklist:**
- [ ] Define the offer form(s) and required fields
- [ ] Decide pricing inputs (base price, comps, other factors)
- [ ] Prototype form fill

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FUT-003 · Research Regrid.com data for the Search Tool

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT

Evaluate Regrid.com parcel data and how it could enrich the Search Tool.

**Checklist:**
- [ ] Review Regrid data coverage for Chicago and licensing/cost
- [ ] Identify fields that would enrich permits/parcels
- [ ] Write up findings

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FUT-002 · Research Polyscan for the Search Tool

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT

Investigate Polyscan and whether it can be used with the Search Tool.

**Checklist:**
- [ ] Establish what Polyscan offers and access model
- [ ] Assess fit with the Search Tool
- [ ] Write up findings

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

---

## 🗄️ Archive

> **Purpose:** Completed or retired tasks moved here to keep the active lists short. Preserve full task bodies when archiving.

### FEAT-026 · Enrich profiles with deed/title, MLS, LLC, VA loan, and licensing data sources

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

Cross-reference and enrich permit, property, and contractor profiles with additional data sources: deed/title records (mortgages, liens), MLS data, Illinois LLC registrations (Secretary of State), VA loan data, licensing bodies, and IDFPR (Illinois Department of Financial and Professional Regulation).

**Checklist:**
- [ ] Evaluate each source: access method, coverage for Chicago, licensing/cost, and terms of use (Cook County Recorder of Deeds for mortgages/liens; MLS access rules; IL SoS LLC data; VA loan records; IDFPR license lookup)
- [ ] Rank sources by enrichment value vs. effort and note findings in this task's Log
- [ ] Design join keys per source (address/PIN for deeds and MLS, name-normalization for LLC/IDFPR, mirroring the licensed-contractor match)
- [ ] Ingest the first approved source(s) into the pipeline and export enriched fields into the JSON indexes
- [ ] Surface enrichments on profiles and permit detail with per-source data caveats
- [ ] Verify sample records against each source of record

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)
- 2026-08-06 09:19 CT — ARCHIVED: consolidated into FEAT-029 at Divyam's request. Not completed and not dropped — every source listed here is carried in FEAT-029's checklist. This ID is retired (Claude)

### FEAT-030 · HOA data: locations vs permits, fees, MLS cross-reference, rental rules

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

Include HOA data: where HOAs sit relative to permits, what their fees are, cross-referenced with MLS data (see FEAT-026 for the MLS source). When pulling a list for a building permit, check whether the HOA allows rentals.

**Checklist:**
- [ ] Identify HOA data sources (MLS fee/association fields, county records, condo declarations) and their coverage/terms
- [ ] Associate permits/addresses with an HOA where one exists
- [ ] Show HOA presence and fee amount on permit detail and list pulls
- [ ] Add a rentals-allowed check to permit list pulls where the data supports it; show unknown honestly otherwise
- [ ] Cross-reference against MLS data once FEAT-026's MLS source lands
- [ ] Verify a sample of known condo/HOA buildings for fee and rental-rule accuracy

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)
- 2026-08-06 09:19 CT — ARCHIVED: consolidated into FEAT-029 at Divyam's request. Not completed and not dropped — the HOA fee, rental-rule and MLS cross-reference items are carried in FEAT-029's checklist. This ID is retired (Claude)


---

<!-- TASK TEMPLATE — copy below this line, replace ALL-CAPS placeholders ─────

### FIX-NNN · SHORT IMPERATIVE TITLE

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** YYYY-MM-DD HH:MM CT
- **Updated:** YYYY-MM-DD HH:MM CT
- **Due:** YYYY-MM-DD
- **Assignee:** NAME
- **Tags:** Chicago Permit Search Tool

One or two sentences of context: what is wrong or wanted, where it lives
in the codebase, and how to know it is finished.

**Checklist:**
- [ ] First concrete step
- [ ] Second concrete step
- [ ] Verify / test the change

**Log:**
- YYYY-MM-DD HH:MM CT — created (Divyam)

──────────────────────────────────────────────────────────────────────── -->

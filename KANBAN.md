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
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

Map Search (`docs/map.html`) should persist the user's selected layers and filters (month, date range, GC job-count range, and future work-type/residential/value filters) so reloading the page restores the same view.

**Checklist:**
- [ ] Inventory every layer toggle and filter setting on the map page
- [ ] Persist them client-side (localStorage, consistent with the existing chi_permit_theme pattern) on every change
- [ ] Restore persisted state on load before first render; fall back to defaults when absent or invalid
- [ ] Handle stale state gracefully when saved filters reference months/shards that no longer exist
- [ ] Verify across reloads, new tabs, and after a daily data refresh

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)

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
- **Status:** todo
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-07-29 11:28 CT
- **Tags:** Chicago Permit Search Tool

The number of people viewing a shared list can be wrong after reloading the page or moving between apps on mobile — reloads appear to double-count, and backgrounded mobile sessions appear to linger (or drop) incorrectly.

**Checklist:**
- [ ] Reproduce both cases: rapid reloads inflating the count, and app-switching on mobile leaving a stale viewer
- [ ] Review how presence is tracked (Worker-side) — connection lifetime, heartbeat, TTL
- [ ] Key presence to a stable per-browser session id so a reload replaces rather than adds a viewer
- [ ] Handle visibilitychange/pagehide/bfcache so backgrounded and restored tabs update presence correctly, with a TTL sweep for clients that vanish without notice
- [ ] Verify count stability across reloads, app switches, tab closes, and multiple real viewers

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)

### FIX-011 · Permit view: show the actual neighborhood name, not just a number

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-29 12:11 CT
- **Updated:** 2026-07-29 12:11 CT
- **Tags:** Chicago Permit Search Tool

The neighborhood shown in the permit view is a bare number — most likely the dataset's community area code. Chicago has 77 named community areas (e.g., 22 → Logan Square); the view should display the real name, with the number at most as secondary detail.

**Checklist:**
- [ ] Confirm which field the number comes from (community area vs. ward vs. census tract) in the permit data
- [ ] Add the official community-area number → name mapping (77 areas, from the City data portal) to the pipeline or as a static lookup
- [ ] Display the neighborhood name everywhere the number currently shows (permit view, list rows, map popups, exports)
- [ ] Fall back gracefully when the code is missing or unrecognized (show the raw value, never blank)
- [ ] Verify a sample of permits across different areas against the City's community area map

**Log:**
- 2026-07-29 12:11 CT — created (Divyam)

### FIX-012 · GC "average processing days" should measure average time to close a permit

- **Priority:** P2-Medium
- **Status:** in-progress
- **Created:** 2026-07-29 12:44 CT
- **Updated:** 2026-07-30 17:20 CT
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
- [ ] Run `npm run seed` twice — the first run establishes the closure baseline, real close times appear from the second onward
- 2026-07-30 17:20 CT — built on branch `fix-012-close-time` (`ecba9d5`, pushed, NOT merged). Divyam chose "open-job age now + start observing closures". New `worker/src/closure.js` + 9 unit tests. Open-job age is exact and computed from permits the seed already fetches. Time-to-close is OBSERVED: each seed snapshots the open set, and a permit that has left it and now reads COMPLETE books issue_date -> observation date. EXPIRED/CANCELLED are excluded — stopping is not finishing, and counting them would flatter slow builders. Stats stored aggregated per contractor ({n, days}) so KV stays bounded by contractor count rather than growing with every permit that ever closes. Snapshot is written LAST so a partial upload re-detects the same closures next run instead of losing them (Claude Code)
- 2026-07-30 17:20 CT — contractors with no observations get NO close keys, so the pill is absent rather than 0; for months that will be nearly everyone, and 0 would read as "closes same day" — the exact confusion this ticket was raised about. Directory column shows an em dash. Verified a hostile render at 390px in both themes: pills wrap, nothing clipped. Adds the first KV READ the seed has ever needed, with the same `--remote` requirement as the writes — without it wrangler reads local Miniflare, every run looks like the first, and no closure ever accumulates. 136 Worker + 111 client unit tests, 46/46 browser suites, overlay block byte-identical (Claude Code)
- 2026-07-30 17:20 CT — NOT DONE until seeded TWICE: run one writes `closure:open_snapshot` and establishes the baseline (no close times yet); run two is the first that can observe a closure. Open-job age appears after the first seed. Awaiting merge approval (Claude Code)


### FIX-013 · Desktop: tag chips at the top should size to their text, not the list width

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-29 13:11 CT
- **Updated:** 2026-07-29 13:11 CT
- **Tags:** Chicago Permit Search Tool

On desktop, the tags listed at the top stretch to the width of the list/container instead of hugging their text. Each tag should be an inline pill sized to its content (fit-content / inline-flex), wrapping naturally as a row of chips — not full-width blocks.

**Checklist:**
- [ ] Locate the tag elements and identify why they expand (block-level display, width:100%, or a stretched flex/grid item)
- [ ] Size each tag to its text with appropriate padding; lay the group out as a wrapping chip row
- [ ] Confirm mobile/narrow layout is unchanged (or improved) by the change
- [ ] Check hover/focus states and touch targets still meet the ui-ux-pro-max standard after resizing
- [ ] Verify on desktop widths across the pages where these tags appear

**Log:**
- 2026-07-29 13:11 CT — created (Divyam)

### FIX-003 · Speed up permit removal in My Permit List and stop accidental opens

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 15:53 CT
- **Updated:** 2026-07-27 15:53 CT
- **Tags:** Chicago Permit Search Tool

Removing a permit from My Permit List (`docs/list.html`) is slow because of the confirmation step, and the remove tap sometimes opens the permit instead — the click appears to fall through to the row's open/detail handler.

**Checklist:**
- [ ] Replace the blocking confirmation with immediate removal plus a short-lived undo
- [ ] Stop the remove control from triggering the row's open action (stop event propagation on click and touch)
- [ ] Verify rapid successive removals stay in sync with saved-list storage
- [ ] Test on desktop and on a phone viewport, including the visited-checkmark and reorder controls nearby

**Log:**
- 2026-07-27 15:53 CT — created (Divyam)

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
- **Status:** todo
- **Created:** 2026-07-29 15:55 CT
- **Updated:** 2026-07-29 15:55 CT
- **Tags:** Chicago Permit Search Tool

The visited checkbox on permits in My Permit List (`docs/list.html`) has no header label. Add a "Visited/Called" label at the top of the checkbox column so it is clear what checking it means, on both desktop and mobile layouts.

**Checklist:**
- [ ] Locate the visited-checkmark column (FEAT-008) in the list's desktop and mobile layouts
- [ ] Add a "Visited/Called" header label above the checkbox column on desktop
- [ ] Add the same label on the mobile layout, keeping it legible without breaking the row layout on small screens
- [ ] Keep the label consistent with the column in any shared-list/read-only view if the checkbox appears there
- [ ] Verify on desktop and phone viewports that the label renders, aligns with the checkboxes, and doesn't overflow

**Log:**
- 2026-07-29 15:55 CT — created (Divyam)

### FIX-019 · My Permit List: tag pills should hug their text, not span the list width

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-30 09:27 CT
- **Updated:** 2026-07-30 09:27 CT
- **Tags:** Chicago Permit Search Tool

On My Permit List (`docs/list.html`), the tag pills stretch to the full width of the list on both desktop and mobile. Each pill should take only the space its text needs plus padding (inline-flex / fit-content), wrapping naturally as a row of chips. Same pattern as FIX-013 (tag chips at the top, desktop) — keep the chip styling consistent between the two.

**Checklist:**
- [ ] Locate the tag pill elements in `docs/list.html` and identify why they expand to full width (block display, width:100%, or stretched flex/grid item)
- [ ] Size each pill to its content with appropriate padding; lay the group out as a wrapping chip row
- [ ] Apply on both desktop and mobile layouts; keep touch targets adequate on mobile
- [ ] Keep the styling consistent with FIX-013's chip treatment if that lands first (or share one fix and log it in both tasks)
- [ ] Verify on desktop and phone viewports, on lists with few and many tags

**Log:**
- 2026-07-30 09:27 CT — created from Divyam's report (Claude)

### FIX-014 · GC view: Specialties counts hang outside their bubbles — keep the number inside like Associations

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-29 13:11 CT
- **Updated:** 2026-07-29 13:11 CT
- **Tags:** Chicago Permit Search Tool

In the General Contractor view, the numbers on Specialties bubbles overflow past the edge of the pill, while Associations renders its counts contained correctly. Make Specialties display its count inside the bubble the same way Associations does.

**Checklist:**
- [ ] Compare the Specialties and Associations bubble markup/CSS and identify why one contains its count and the other overflows (absolute positioning, white-space, min-width, or padding differences)
- [ ] Align Specialties to the Associations pattern — ideally share one bubble component/style for both
- [ ] Check long specialty names and 3+ digit counts wrap or truncate gracefully
- [ ] Verify on desktop and mobile in the GC overlay card, and anywhere else Specialties bubbles render

**Log:**
- 2026-07-29 13:11 CT — created (Divyam)

### FIX-015 · Show the person in charge of a GC company (and Open Sub LLCs/companies) everywhere they appear

- **Priority:** P1-High
- **Status:** in-progress
- **Created:** 2026-07-29 14:07 CT
- **Updated:** 2026-07-30 16:45 CT
- **Tags:** Chicago Permit Search Tool

Wherever a General Contractor company shows up (directory rows, profile cards, permit detail, overlay cards, map popups, list rows, exports), display the name of the person in charge of that company. Same for Open Subs that are LLCs or companies: show the responsible person alongside the business name. Likely sources: the city contractor registry / licensing data already ingested (FEAT-004/FEAT-014 surfaced titles), and IL Secretary of State LLC registrations (manager/registered agent) — FEAT-026 covers deeper LLC ingestion; this task uses whatever fields are available now and leaves richer enrichment to FEAT-026.

**Checklist:**
- [x] Identify where a "person in charge" name exists in current data (contractor registry contact/licensee name, permit contact fields) for GCs and for Open Sub companies; note coverage in this task's Log
- [x] Add the name to the pipeline exports so it rides the existing JSON indexes
- [x] Display it everywhere GCs appear: directory rows, GC profile/overlay card, permit detail contractor lines, map popups, CSV export
- [x] Same for Open Subs that are LLCs/companies, in all the same surfaces
- [x] Handle missing data honestly (omit the line rather than showing blank/unknown junk)
- [x] Verify a sample of well-known GCs and sub companies against the registry/SoS records
- [x] ADDED by Divyam 2026-07-30: show the unit owner's name and contact information on the permit view, alongside the GC's owner
- [x] Run `npm run seed` from `worker/` — the join happens at seed time, so nothing appears until then
- [ ] Confirm on a real phone once seeded

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

### FIX-002 · UI cleanup and mobile accessibility

- **Priority:** P3-Low
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

General UI polish plus accessibility on small screens.

**Checklist:**
- [ ] Audit layout and overflow on phone-sized viewports
- [ ] Improve touch target sizes and contrast
- [ ] Add ARIA labels / semantic markup where missing
- [ ] Verify with Lighthouse accessibility pass

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

### FIX-020 · The browser test suite is gitignored and exists on one machine only

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-30 15:55 CT
- **Updated:** 2026-07-30 15:55 CT
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

---

## ✨ Features

> **Purpose:** New features and ideas to be added to the existing Chicago Permit Search tool. Enhancements that extend the current project rather than repair it.

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
- **Status:** todo
- **Created:** 2026-07-27 10:09 CT
- **Updated:** 2026-07-27 10:09 CT
- **Tags:** Chicago Permit Search Tool

Filter/search by permit (reported cost) value range in both the Search tool and the Map Search tool.

**Checklist:**
- [ ] Add value-range input to Search filters
- [ ] Add value-range filter to Map Search
- [ ] Ensure indexes expose reported cost efficiently
- [ ] Verify results match range on both tools

**Log:**
- 2026-07-27 10:09 CT — created (Divyam)

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
- **Status:** todo
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-07-29 11:28 CT
- **Tags:** Chicago Permit Search Tool

In a list in My Permit List (`docs/list.html`), let people filter permits by whether someone has visited or called them. The visited checkmark (FEAT-008) and the Call action (FEAT-025 cards) already exist — this adds a tracked "called" state alongside visited and exposes both as list filters.

**Checklist:**
- [ ] Track a "called" state per permit, set when the Call action is used and manually togglable like the visited checkmark
- [ ] Add filter controls to the list view: all / visited / not visited / called / not called (combinable)
- [ ] On shared lists, reflect visit/call state consistently for everyone viewing the list; show who acted where the data allows
- [ ] Make filters play well with reordering, route optimization, and exports (filtered view should not silently change export scope without saying so)
- [ ] Verify on desktop and mobile, including a shared list with multiple viewers

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)

### FEAT-024 · Map Search: filter out work types and filter to residential only

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-27 15:53 CT
- **Updated:** 2026-07-27 15:53 CT
- **Tags:** Chicago Permit Search Tool

In Map Search (`docs/map.html`), let the user exclude certain types of work and narrow results to residential properties only. FEAT-013 (building type) already supplies the residential signal; this exposes it as a map filter.

**Checklist:**
- [ ] Enumerate the work types present in the permit data and pick the filterable set
- [ ] Add a work-type exclude control to Map Search
- [ ] Add a residential-only toggle, defining which building types count as residential
- [ ] Verify both combine correctly with the existing month and value-range filters
- [ ] Check performance with filters applied across the monthly map shards

**Log:**
- 2026-07-27 15:53 CT — created (Divyam)

### FEAT-032 · Feed the search conditions/filters into the list description

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-29 11:28 CT
- **Updated:** 2026-07-29 11:28 CT
- **Tags:** Chicago Permit Search Tool

When permits are pulled into a list from Search or Map Search, record the conditions and filters that produced them (ward, date range, work types, value range, etc.) in the list's description, so anyone opening the list later can see how it was built.

**Checklist:**
- [ ] Capture the active filters/conditions at the moment permits are added or a list is pulled
- [ ] Render them as a compact human-readable summary in the list description (e.g. "Ward 47 · Jun–Jul 2026 · renovation excluded · $50k–$250k")
- [ ] Append rather than overwrite when adds come from different searches; keep the description editable by hand
- [ ] Show the summary on shared/opened lists too
- [ ] Verify with adds from both Search and Map Search, and with manually added permits (which should note no filters)

**Log:**
- 2026-07-29 11:28 CT — created (Divyam)

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

### FEAT-029 · Airbnb licensees layer: density map and management-outreach view

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-07-28 14:06 CT
- **Updated:** 2026-07-28 14:06 CT
- **Tags:** Chicago Permit Search Tool

Include Chicago short-term rental / Airbnb licensees, shown as a Map Search layer, with the goals of seeing where Airbnb density is concentrated and identifying hosts who may want property management.

**Checklist:**
- [ ] Source the City of Chicago shared housing / short-term rental registration data
- [ ] Ingest licensees with locations into the pipeline and export a map-ready index
- [ ] Add an Airbnb layer to Map Search with a density view (clusters or heat) and per-license markers
- [ ] Show available license details in the marker popup for outreach use
- [ ] Make the layer respect existing filters where sensible and persist with FIX-008's remembered map state
- [ ] Verify density hotspots against known short-term-rental neighborhoods

**Log:**
- 2026-07-28 14:06 CT — created (Divyam)

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

### FEAT-034 · Per-list notes feed: searchable, timestamped notes inside each permit list

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-29 13:27 CT
- **Updated:** 2026-07-29 14:11 CT
- **Tags:** Chicago Permit Search Tool

Make notes searchable within each permit list — NOT one overall site-wide tab. Inside a specific list in My Permit List (`docs/list.html`), a notes feed opened from a control at the top of that list lays out that list's notes as a timestamped feed (newest first) with search. Each entry shows its note text, timestamp, and the permit (in this list) it belongs to. Clicking a note jumps to its associated permit, and from a permit you can jump back into the feed — navigation works to and from in both directions without losing your place in the feed. The feed's scope is always the list you're in; different lists have separate feeds.

**Checklist:**
- [ ] Inventory where notes are stored today (per-permit) and expose them as a queryable collection scoped per permit list
- [ ] Add a notes feed entry point at the top of each permit list view (inside the list, not a global tab)
- [ ] Feed view: timestamped entries for this list only, newest first, each showing note text + linked permit summary
- [ ] Search within the feed (note text, permit address/number); instant filter as you type
- [ ] Click a note → open its associated permit; back returns to the feed at the same scroll/search state
- [ ] From a permit in the list, link into the feed filtered to that permit's notes
- [ ] Decide behavior on shared lists (do viewers see the feed? consistent with how notes themselves are shared)
- [ ] Mobile: 44px touch targets, feed usable on small screens
- [ ] Verify round-trip navigation and search on mobile and desktop, across multiple lists (feeds stay separate)

**Log:**
- 2026-07-29 13:27 CT — created (Divyam)
- 2026-07-29 14:11 CT — scope clarified by Divyam: the feed lives INSIDE each specific permit list, not as an overall site tab; description, title, and checklist updated (Claude)

### FEAT-035 · Permit lists: 1000-permit cap with 100-per-page pagination that remembers your page

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-29 13:50 CT
- **Updated:** 2026-07-29 13:50 CT
- **Tags:** Chicago Permit Search Tool

In My Permit List (`docs/list.html`), cap each list at 1000 permits and paginate the list view at 100 permits per page with click-through page controls. Pagination must keep its memory: clicking into a permit and coming back returns you to the same page (and scroll position), consistent with the existing last-view persistence (FEAT-025 Phase 3). Critically, pagination is a presentation layer only — Optimize Route must account for the full scope of the list (all pages, up to 1000), not just the visible page; same for exports and drive distances. FIX-004 (done on branch `fix-004-route-scope`) already un-bounded the optimizer via a tiled OSRM matrix, but set a practical ceiling of 400 stops (`MAX_SORT_STOPS`, main-thread local-search cost) — this task must reconcile that ceiling with the 1000-permit cap (raise it per FIX-004's noted path: incremental delta evaluation and/or a worker thread, or clearly message the limit).

**Checklist:**
- [ ] Enforce a 1000-permit cap per list: block adds past the cap with a clear message (single adds and "Add all N" bulk adds — cap-aware partial add with a count of what was skipped)
- [ ] Paginate the list view at 100 per page with page controls (prev/next + page numbers, current page and total count visible)
- [ ] Persist the current page in last-view state: opening a permit and returning restores the same page and scroll position; reloads restore it too
- [ ] Keep Optimize Route, drive distances, and exports (Google Maps/KML/CSV) scoped to the FULL list across all pages — verify with a multi-page list (FIX-004's tiled matrix)
- [ ] Reconcile FIX-004's 400-stop optimizer ceiling with the 1000 cap: raise the ceiling (delta-evaluated local search, off-main-thread) or surface an honest limit message when a list exceeds it
- [ ] Make pagination play well with reordering, visited/called state, and shared lists (viewers see consistent pages)
- [ ] Check performance at the 1000-permit ceiling (render, OSRM request count, share/live sync)
- [ ] Verify page memory and full-scope route optimization on desktop and mobile

**Log:**
- 2026-07-29 13:50 CT — created (Divyam)

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

*Empty.*

---

<!-- TASK TEMPLATE — copy below this line, replace ALL-CAPS placeholders ─────

### FIX-001 · SHORT IMPERATIVE TITLE

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

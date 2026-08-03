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
- **Status:** in-progress
- **Created:** 2026-07-31 14:39 CT
- **Updated:** 2026-08-03 12:05 CT
- **Tags:** Chicago Permit Search Tool

**Merged and live as `f112b9d`. Held open for ONE reason: the on-device check.** Everything automation can prove is proven, but the symptom this card is named for — Safari zooming on focus — cannot be reproduced headlessly. Divyam: open the live site on your iPhone, tap a filter field on the Search panel and on the map's Filters drawer, and confirm the page no longer zooms in and stay zoomed. Close this once confirmed; reopen if it still zooms.

Measured while building FEAT-021, on the fields next to the new ones — this is pre-existing and site-wide, not caused by that work. Safari on iOS auto-zooms the page whenever a focused input's font is below 16px, and then leaves the page zoomed in; the user has to pinch back out after every filter edit.

Measured at an iPhone 13 viewport: every control in the Search panel renders at **15px** (`body.directory-page .controls input` sets `font-size: 1rem`, but `index.html` shrinks `html` to 15px below 640px, so 1rem is not 16px there — the same rem trap recorded on FIX-022), and every field in the map filter drawer renders at **14.4px** (`map-date-from` at 13.76px). Touch heights are fine: 44–50px throughout.

Not fixed inside FEAT-021 on purpose: the new value-range fields were matched to their neighbours rather than made the only 16px inputs in a row of 15px ones. It needs one deliberate pass across all three pages.

**Checklist:**
- [x] Decide the fix: raise the inputs to a hard 16px, or stop shrinking `html` below 640px — **raised the controls**. The shrink is a deliberate density choice the rest of the layout is built on, and this is a form-control problem, so the fix belongs on form controls rather than on the page's type scale
- [x] Apply to `index.html`, `map.html` and `list.html` — the rem behaves differently per page, so verify each rather than assuming one rule covers all three
- [x] Confirm the date inputs too (`map-date-from`/`map-date-to` are the smallest at 13.76px)
- [x] Verify at an iPhone 13 viewport that no control computes below 16px
- [x] Verify raising the type did not break the layouts — no clipping, no control past the viewport edge, no horizontal scroll at 390px, and no leak to desktop
- [ ] Confirm on a real iOS device that focusing a filter no longer zooms — headless cannot show this **← still the only item left; needs Divyam's iPhone, no automation can close it**
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

---

## ✨ Features

> **Purpose:** New features and ideas to be added to the existing Chicago Permit Search tool. Enhancements that extend the current project rather than repair it.

### FEAT-038 · Source property use from the Cook County Assessor class, so the permit view stops approximating

- **Priority:** P2-Medium
- **Status:** todo
- **Created:** 2026-08-03 11:03 CT
- **Updated:** 2026-08-03 11:03 CT
- **Tags:** Chicago Permit Search Tool

The permit view's "Property use" line is a guess. `permitUse()` (FEAT-013) reads `permit_type` + `work_description` and is rendered with an "approx" badge because the permits dataset carries no occupancy field. Over a real month it can classify only **32%** of permits; the other 68% read "Unclear".

Divyam asked whether the zoning source that made FEAT-024's filter work could replace it. **It cannot, and should not** — see the log. But the permits dataset already carries `pin_list`, the Cook County PIN, which joins straight to the Assessor's parcel universe (`nj4t-kc8j`) and its `class` field: the County's own legal classification of the parcel's use for assessment. That is a recorded fact the badge can cite, not an inference from prose.

Measured over July 2026 (2,384 open geocoded permits): 2,101 (88.1%) carry a usable 10-digit PIN, and **2,057 (86.3%) match an Assessor parcel record** — 67.4% residential, 11.5% commercial/industrial, 5.0% exempt, 1.8% vacant, 0.4% incentive. With the existing text heuristic kept as fallback for the unmatched, **only 11.5% of permits would still read "unknown", down from 68%.**

**Checklist:**
- [ ] Build a three-digit class → use mapping, NOT a major-class one (see the log — this is where the errors concentrate)
- [ ] Resolve a permit's class on demand from `pin_list`, cached per permit, the same shape as the existing zoning and TIF lookups — never a bulk fetch
- [ ] Handle the multi-PIN case (`pin_list` is pipe-delimited; ~39 permits a month carry several parcels)
- [ ] Show the class as a sourced fact ("Residential · Cook County class 203") and drop the "approx" badge where the class is decisive
- [ ] Keep `permitUse()` as the fallback for the ~12% with no parcel match, still badged as approximate
- [ ] Keep a hedge for the genuinely mixed 5xx classes rather than calling them commercial
- [ ] Verify a sample against the Assessor's own property search, not just against the old heuristic
- [ ] Decide whether the FEAT-024 map filter should switch to this source too, or stay on zoning (they answer different questions — see the log)

**Log:**
- 2026-08-03 11:03 CT — created from Divyam's question after FEAT-024 shipped: "if the residential/commercial filter works effectively now, can we accurately use the same data sources to correctly tag residential/commercial on the Permit details, and not have to use approximations?" (Claude Code)
- 2026-08-03 11:03 CT — **answer: yes, but NOT from zoning.** Zoning states what a district ALLOWS, not what a property IS. Measured over the same July month, **213 of the 623 permits the text confidently calls residential sit in non-residential districts** — 98 in planned developments, 44 business, 39 downtown, 12 manufacturing, 12 commercial, 6 open space, 2 transportation. Those are overwhelmingly real housing work (a B3-5 fire alarm reading "AFFECTS: 40 DWELLING UNITS"). Zoning is the right signal for a FILTER ("show me residential areas") and the wrong one for a LABEL on one permit, where it would confidently mislabel about a third of them. FEAT-024 stays on zoning deliberately (Claude Code)
- 2026-08-03 11:03 CT — the join was proven end to end before this card was written, not assumed: `pin_list` → `nj4t-kc8j.pin10` → `class`, newest `year` first, batched 150 PINs per request. Coverage figures above are from that run. Cook County major classes: 0xx/1xx vacant, 2xx houses and 2–6 units, 3xx apartments 7+, 4xx not-for-profit, 5xx commercial/industrial, 6xx–9xx incentive, EX exempt (Claude Code)
- 2026-08-03 11:03 CT — **three caveats found while measuring, all of which belong in the build rather than being discovered after it.** (1) The class describes the PARCEL, not the work: agreement with the text heuristic where both speak is 85.9%, and the 82 disagreements are instructive — class 590 on "NEW 2 STORY SINGLE FAMILY RESIDENCE", class 517 on plumbing-fixture work — some are conversions the class has not caught up with. (2) **A naive `5xx → commercial` mapping is wrong**: several 5xx classes explicitly ARE mixed commercial/residential (593 is "two or three story, over 62 years, mixed commercial and residential"), and that is exactly where the probe's disagreements clustered, because the probe used major class. (3) It adds a second live dependency on Cook County's Socrata, so it needs the on-demand + cache treatment, not a bulk fetch (Claude Code)

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

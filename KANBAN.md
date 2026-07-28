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
- **Status:** todo
- **Created:** 2026-07-27 15:55 CT
- **Updated:** 2026-07-27 15:55 CT
- **Tags:** Chicago Permit Search Tool

Optimize Route in My Permit List (`docs/list.html`) should optimize across every permit in the saved list, not a subset. Google Maps caps waypoints per link, so the list is chunked for export — that export chunking must not also cap what the optimizer considers.

**Checklist:**
- [ ] Find where the current optimize-route scope is bounded (export chunking, visible rows, or a hard waypoint cap)
- [ ] Run the optimization across the entire saved list, independent of export chunking
- [ ] Keep Google Maps chunk generation as a presentation step applied after optimization
- [ ] Verify the resulting order and total drive time improve on a long list
- [ ] Check OSRM request count and runtime on a large list; note any practical ceiling in this task's Log

**Log:**
- 2026-07-27 15:55 CT — created (Divyam)

### FIX-005 · Share on My Permit List hangs when a link is already generated

- **Priority:** P1-High
- **Status:** todo
- **Created:** 2026-07-27 16:00 CT
- **Updated:** 2026-07-27 16:00 CT
- **Tags:** Chicago Permit Search Tool

Share in My Permit List (`docs/list.html`) appears to get stuck when a share link has already been generated — a second Share attempt hangs instead of reusing or regenerating the existing link.

**Checklist:**
- [ ] Reproduce: generate a share link, then invoke Share again in the same session
- [ ] Identify the stuck state (unreset in-flight/"generating" flag, an unresolved promise, or a modal left open behind the scenes)
- [ ] Make repeat Share reuse the existing link, or regenerate cleanly when the list has changed since
- [ ] Reset share state on failure so it can never latch permanently
- [ ] Verify repeated Share on desktop and mobile, including after editing the list between shares

**Log:**
- 2026-07-27 16:00 CT — created (Divyam)

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

---

## ✨ Features

> **Purpose:** New features and ideas to be added to the existing Chicago Permit Search tool. Enhancements that extend the current project rather than repair it.

### FEAT-025 · Contractor detail view in the permit overlay

- **Priority:** P1-High
- **Status:** done
- **Created:** 2026-07-27 14:27 CT
- **Updated:** 2026-07-28 21:05 CT
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
- [x] Phase 3: last-view persistence — tab, query, sort, page, scroll, selection
- [x] Re-run `node seed-kv.js` so `seeded_at` exists and the staleness line shows

**Log:**
- 2026-07-27 14:27 CT — design spec written, accessibility audit at design time (Claude Code)
- 2026-07-27 16:23 CT — tasks 1-4 built on branch, task 4 held for review (Claude Code)
- 2026-07-28 18:20 CT — task 4 reviewed; keyboard-dead contractor rows fixed; bulk add now offers the list picker; tasks 1-4 merged to main `d608b38` (Claude Code)
- 2026-07-28 18:55 CT — tasks 5-6 complete; ui-ux-pro-max pass fixed mid-number wrapping and a sub-12px type floor that also rendered differently on the two pages; merged to main `1a96736`; Phase 1 done (Claude Code)
- 2026-07-28 19:34 CT — Phase 2: Worker matching ladder + matched_as/matched_category/seeded_at, 18 new Worker tests (117 total). Worker deployed and all three rungs verified in production, then merged to main `24d6537`. seeded_at pending a seed-kv.js re-run (Claude Code)
- 2026-07-28 20:12 CT — Phase 3: chi_permit_last_view now carries tab/query/sort/page/scroll/selection on both pages; merged to main `011f56c`. All three phases done — 111 client + 117 Worker + 13 browser suites green (Claude Code)
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

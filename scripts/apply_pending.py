#!/usr/bin/env python3
"""Apply a PENDING-*.md staging file into KANBAN.md.

Why this exists: KANBAN.md is ~262 KB. GitHub's contents API replaces a whole
file per commit and has no append or patch endpoint, so board edits cannot be
pushed from the Claude app -- the write would have to carry the entire file.
This script lets the edit be staged as a small file and applied server-side by
GitHub Actions instead.

It is deliberately strict: every edit asserts its anchor exists exactly once,
and the whole run aborts without writing if anything is off. A partial apply to
the single source of truth is worse than no apply.

Safe to re-run: exits 0 with no changes if there is no staging file.
"""

import glob
import re
import sys

BOARD = "KANBAN.md"
STAMP = "2026-08-06 09:19 CT"

ARCHIVE_NOTE = (
    "- {stamp} \u2014 ARCHIVED: consolidated into FEAT-029 at Divyam's request. "
    "Not completed and not dropped \u2014 every item here is carried in "
    "FEAT-029's checklist. This ID is retired (Claude)\n"
).format(stamp=STAMP)

ARCHIVE_ANCHOR = (
    "> **Purpose:** Completed or retired tasks moved here to keep the active "
    "lists short. Preserve full task bodies when archiving.\n\n*Empty.*\n"
)

ARCHIVE_HEADER = (
    "> **Purpose:** Completed or retired tasks moved here to keep the active "
    "lists short. Preserve full task bodies when archiving.\n\n"
)


def die(msg):
    sys.exit("apply_pending: " + msg)


def card(text, task_id, where):
    """Extract one `### <ID> - ...` block, up to the next heading or rule."""
    pattern = r"^### " + re.escape(task_id) + r" \u00b7.*?(?=^### |^## |^---$)"
    found = re.findall(pattern, text, re.M | re.S)
    if len(found) != 1:
        die("expected exactly 1 %s block in %s, found %d" % (task_id, where, len(found)))
    return found[0].rstrip() + "\n\n"


def insert_before(board, anchor, block):
    if board.count(anchor) != 1:
        die("anchor %r appears %d times in the board, expected 1" % (anchor, board.count(anchor)))
    return board.replace(anchor, block + anchor, 1)


def main():
    staged = sorted(glob.glob("PENDING-*.md"))
    if not staged:
        print("no PENDING-*.md staging file; nothing to do")
        return 0
    if len(staged) > 1:
        die("multiple staging files found (%s); apply them one at a time" % ", ".join(staged))
    pending_path = staged[0]

    pending = open(pending_path, encoding="utf-8").read()
    board = open(BOARD, encoding="utf-8").read()
    before = board

    fix041 = card(pending, "FIX-041", pending_path)
    feat043 = card(pending, "FEAT-043", pending_path)
    feat029_new = card(pending, "FEAT-029", pending_path)

    # The staging file was written before the move happened, so its FEAT-029
    # description is in the future tense. On the board it is a past fact.
    tense_old = "Both source cards move to the Archive with their bodies intact"
    tense_new = "Both source cards are in the Archive with their bodies intact"
    if tense_old not in feat029_new:
        die("expected tense phrase not found in the staged FEAT-029 block")
    feat029_new = feat029_new.replace(tense_old, tense_new, 1)

    # Guard against a double-apply: these IDs must still be live on the board.
    for task_id in ("FIX-041", "FEAT-043"):
        if re.search(r"^### " + task_id + r" \u00b7", board, re.M):
            die("%s is already on the board -- this staging file looks applied" % task_id)

    # 1 + 2. New cards go to the top of their lists (the board is newest-first).
    board = insert_before(board, "### FIX-040 \u00b7 ", fix041)
    board = insert_before(board, "### FEAT-042 \u00b7 ", feat043)

    # 3 + 4. Consolidate FEAT-026 and FEAT-030 into the rewritten FEAT-029.
    feat026_old = card(board, "FEAT-026", BOARD)
    feat029_old = card(board, "FEAT-029", BOARD)
    feat030_old = card(board, "FEAT-030", BOARD)

    board = board.replace(feat029_old, feat029_new, 1)
    board = board.replace(feat026_old, "", 1)
    board = board.replace(feat030_old, "", 1)

    # Repoint the one dangling cross-reference, in FIX-015's description.
    ref_old = (
        "FEAT-026 covers deeper LLC ingestion; this task uses whatever fields are "
        "available now and leaves richer enrichment to FEAT-026."
    )
    ref_new = (
        "FEAT-029 covers deeper LLC ingestion (originally FEAT-026, consolidated "
        "2026-08-06); this task uses whatever fields are available now and leaves "
        "richer enrichment to FEAT-029."
    )
    if board.count(ref_old) != 1:
        die("FIX-015's FEAT-026 cross-reference was not found exactly once")
    board = board.replace(ref_old, ref_new, 1)

    # Archive both, bodies verbatim, with one log line each explaining why.
    archived = (
        feat026_old.rstrip("\n") + "\n" + ARCHIVE_NOTE + "\n"
        + feat030_old.rstrip("\n") + "\n" + ARCHIVE_NOTE + "\n"
    )
    if board.count(ARCHIVE_ANCHOR) != 1:
        die("the Archive section is not in its expected empty state")
    board = board.replace(ARCHIVE_ANCHOR, ARCHIVE_HEADER + archived, 1)

    # Post-conditions. Nothing is written unless all of these hold.
    ids = re.findall(r"^### (\S+) \u00b7", board, re.M)
    for task_id in ("FIX-041", "FEAT-043", "FEAT-029", "FEAT-026", "FEAT-030"):
        if ids.count(task_id) != 1:
            die("post-check: %s appears %d times, expected 1" % (task_id, ids.count(task_id)))
    for heading in ("## \U0001f527 Fixes", "## \u2728 Features",
                    "## \U0001f52d Futures", "## \U0001f5c4\ufe0f Archive"):
        if board.count(heading) != 1:
            die("post-check: list heading %r is missing or duplicated" % heading)
    if "\n\n\n\n" in board:
        die("post-check: blank-line run introduced")
    if len(board) <= len(before):
        die("post-check: board did not grow; refusing to write")

    open(BOARD, "w", encoding="utf-8").write(board)
    print("applied %s: +FIX-041, +FEAT-043, FEAT-029 rewritten, "
          "FEAT-026 and FEAT-030 archived" % pending_path)
    print("board %d -> %d bytes" % (len(before.encode()), len(board.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env node
// Does board.html still find the tasks in KANBAN.md?
//
// FIX-048. Commit 68cf966 re-encoded the whole board file and every task
// heading stopped matching board.html's parser: three lists rendered
// "No matching tasks" for a day while three more board commits landed on top.
// Nothing noticed, because nothing between "edit KANBAN.md" and "push" ever
// asked the parser whether the file still parsed.
//
//   node check-board.mjs            check the board, exit 1 if it is broken
//   node check-board.mjs --selftest prove the check reports failure, then pass
//
// No dependencies. Do not edit KANBAN.md with PowerShell -- a read-modify-write
// re-encodes the file and is what this check exists to catch.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));

// The heading pattern is read out of board.html, never copied. A copy drifts
// from the real parser and then quietly agrees with the bug.
function headingRegexFrom(html) {
  const m = html.match(/ln\.match\((\/\^###[^\n]*?\/)\)\)/);
  if (!m) {
    throw new Error(
      'could not find the task-heading regex in board.html. It is matched out of ' +
      "the line `ln.match(/^###.../)` inside parse(). If that line moved or was " +
      'rewritten, update the extraction here -- do not paste a copy of the regex.'
    );
  }
  const body = m[1].slice(1, m[1].lastIndexOf('/'));
  return new RegExp(body);
}

// Mirrors stripComments() in board.html.
const stripComments = md => md.replace(/<!--[\s\S]*?-->/g, '');

function check(html, md) {
  const problems = [];
  const heading = headingRegexFrom(html);

  // Mojibake, independent of whether it happens to break the regex this time.
  // U+00C2 and U+00E2 lead the cp1252 misreadings of UTF-8; U+FFFD is a lost
  // character. FIX-048's own card spells these out as code points so that
  // describing the bug does not trip the scan.
  for (const [name, cp] of [['U+00C2', 'Â'], ['U+00E2', 'â'], ['U+FFFD', '�']]) {
    const n = md.split(cp).length - 1;
    if (n) problems.push(`${n} x ${name} in KANBAN.md -- the file has been re-encoded (see FIX-048 for the cp1252 repair)`);
  }

  // Every list board.html would render must render at least one task.
  let list = null;
  const lists = [];
  for (const ln of stripComments(md).split(/\r?\n/)) {
    let m;
    if ((m = ln.match(/^##\s+(.+)$/))) lists.push((list = { name: m[1].trim(), tasks: 0 }));
    else if (list && /^###\s/.test(ln) && heading.test(ln)) list.tasks++;
  }

  const shown = lists.filter(l => !/archive/i.test(l.name)); // board.html drops Archive
  if (!shown.length) problems.push('no lists found at all -- is this KANBAN.md?');
  for (const l of shown) {
    if (!l.tasks) problems.push(`list "${l.name}" renders 0 tasks -- board.html would show "No matching tasks"`);
  }
  return { problems, lists: shown };
}

// cp1252 high range: what a PowerShell read-modify-write turns UTF-8 into.
const CP1252_HI = '€‚ƒ„…†‡ˆ‰Š‹ŒŽ' +
                  '‘’“”•–—˜™š›œžŸ';
const mojibake = s => [...Buffer.from(s, 'utf8')]
  .map(b => (b >= 0x80 && b <= 0x9f ? CP1252_HI[b - 0x80] : String.fromCharCode(b))).join('');

const html = fs.readFileSync(path.join(DIR, 'board.html'), 'utf8');
const md = fs.readFileSync(path.join(DIR, 'KANBAN.md'), 'utf8');

if (process.argv.includes('--selftest')) {
  // A probe that reports failure is worth nothing until it has been seen to
  // report success. Both directions, on the real corruption, every run.
  const clean = check(html, md);
  if (clean.problems.length) {
    console.error('SELFTEST FAILED: the check reports problems on the current board:');
    for (const p of clean.problems) console.error('  - ' + p);
    process.exit(1);
  }
  const broken = check(html, mojibake(md));
  if (!broken.problems.length) {
    console.error('SELFTEST FAILED: the check passed a deliberately re-encoded board. It cannot catch FIX-048.');
    process.exit(1);
  }
  console.log(`selftest ok -- clean board passes; re-encoded board is caught (${broken.problems.length} problems):`);
  for (const p of broken.problems) console.log('  - ' + p);
  process.exit(0);
}

const { problems, lists } = check(html, md);
if (problems.length) {
  console.error('BOARD IS BROKEN:');
  for (const p of problems) console.error('  - ' + p);
  console.error('\nDo not push this. See FIX-048 in KANBAN.md.');
  process.exit(1);
}
console.log('board ok -- ' + lists.map(l => `${l.name}: ${l.tasks}`).join(', '));

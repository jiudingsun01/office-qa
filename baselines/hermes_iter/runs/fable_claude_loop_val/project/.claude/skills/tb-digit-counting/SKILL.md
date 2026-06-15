---
name: tb-digit-counting
description: Use for any Treasury Bulletin / OfficeQA question that asks to COUNT occurrences of a digit, numeral, or symbol within table datapoints on a given PDF page (e.g. "how many times does '1' appear as the leading digit").
---

# Counting digits/numerals in Treasury Bulletin table datapoints

These questions ("how many times does the numeral X appear [as the leading
digit] in the tables on pdf page N, excluding row and column headers?") were
answered correctly with the procedure below. The count is fragile — one
misclassified cell changes the answer — so follow it exactly.

## 1. Locate the right page
- "pdf page N (report page M)": **pdf page N is the physical page index in
  the file** — use it directly. The printed report page differs by a
  per-edition offset (front matter), so don't recompute it; the question
  gives both precisely so you don't have to.
- Extract that single page only, e.g.
  `pdftotext -f N -l N -layout bulletin.pdf page.txt`
  (or pdfplumber `pages[N-1]`). A page often holds **multiple tables** —
  the question says "tables", so include every table on the page.

## 2. Decide what is a "datapoint" BEFORE counting
Count only **numeric cells in the table body**. Exclude:
- Column headers (including numeric year/date column headings like "1979"
  and numeric column-number rows some tables print under the headers).
- Row stubs / row headers — including date stubs ("1980-Jan.", fiscal-year
  labels) in the leftmost column, even though they contain digits.
- Table titles, table numbers ("Table FFO-2"), footnotes, footnote
  reference superscripts attached to values, page numbers, and source notes.
- Non-numeric body cells: "n.a.", "(*)", dashes/leaders ("....").

Include every numeric body cell: totals/subtotal rows ARE datapoints
unless the question excludes them.

## 3. "Leading digit" definition
For each datapoint, the leading digit is the **first digit character** of
the printed value after stripping non-digit prefixes:
- Ignore minus signs and opening parentheses: "(1,234)" → leading digit 1.
- Ignore footnote markers and asterisks prefixed to the value.
- Apply "first digit character in the token" mechanically:
  "0.15" → leading digit **0** (a printed leading zero counts; "1" is NOT
  the leading digit of "0.15"), while ".15" with no printed zero →
  leading digit **1**.
- Commas are separators, not digits: "1,234" leading digit 1 (and contains
  digits 1,2,3,4 for "appears anywhere" variants).

Read the question wording carefully: "as the leading digit" ≠ "anywhere in
the value". For "anywhere" variants count every occurrence, including
repeats within one number.

## 4. Count programmatically, then verify independently
- Parse the extracted text with a small script (regex for numeric tokens
  per line, skipping header/stub regions identified by column position),
  and print the per-row tally so it can be audited.
- Cross-check with a second pass: render the page to an image (e.g.
  `pdftoppm -f N -l N -r 150`) and visually spot-check rows where the text
  extraction looked garbled (merged columns, lost minus signs). pdftotext
  `-layout` can merge adjacent columns — if any line has fewer tokens than
  the table has columns, re-extract that region before trusting the count.
- The final answer is a bare integer (see answer-format skill).

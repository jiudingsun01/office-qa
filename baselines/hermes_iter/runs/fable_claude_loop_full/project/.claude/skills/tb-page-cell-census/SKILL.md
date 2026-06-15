---
name: tb-page-cell-census
description: Use for Treasury Bulletin questions that ask you to count things across ALL table datapoints on a specific PDF/report page — e.g. "how many times does the numeral N appear as the leading digit", "how many cells contain X", "how many entries are blank/negative".
---

# Treasury Bulletin: page-level cell-census (counting) questions

These questions are pure transcription+tally exercises over every table on one page. Accuracy comes from exhaustive, cell-by-cell extraction — not from skimming OCR text.

## Locating the page
- The question usually gives BOTH a PDF page number and a printed report page number (e.g. "pdf page 41 (report page 23)"). Navigate by the **PDF page number**; use the printed page number in the header/footer only to confirm you're on the right page. The offset between them varies by issue (front matter length), so never assume a fixed offset.
- Render/read the actual page image if possible; raw OCR text loses column alignment and merges adjacent cells, which corrupts counts.

## What counts as a "datapoint"
- "Excluding the row and column headers" means: exclude the stub column (row labels, including any dates/period labels used as row identifiers), column heading rows, table titles, and footnotes at the bottom of the page.
- INCLUDE every numeric cell in the body: subtotal and total rows/columns are datapoints too, unless the question excludes them.
- If the page has multiple tables, census ALL of them — the question says "the tables on the page".

## Leading-digit counting rules
- The leading digit of a number is its first printed digit, ignoring: minus signs, parentheses (negatives), dollar signs, and leading punctuation. For decimals like ".15" the leading digit is 1 (first digit printed), and for "0.15" it is 0 — count what is printed.
- **Footnote markers are the #1 pitfall.** Bulletin cells often carry numeric footnote references (superscript digits, or "1/" "2/" prefixes in OCR). A cell printed as "¹1,234" has leading digit 1 from the VALUE, not 2 digits; an OCR string like "1/ 234" is footnote-1 + value 234 (leading digit 2). Inspect the page image to separate markers from values.
- Commas inside numbers (1,234) don't affect the leading digit. Blank cells, "n.a.", dashes, and asterisks contribute nothing.

## Tally procedure (do this, it works)
1. Transcribe each table body into a grid, row by row, preserving every cell.
2. For each cell, record its leading digit; build a per-row count of the target digit.
3. Sum per-row counts per table, then across tables; re-verify by a second independent pass (e.g. recount per-column) and reconcile any mismatch before answering.
4. Report a bare integer.

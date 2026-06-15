---
name: tb-page-counting
description: Use for Treasury Bulletin questions that ask you to COUNT things on ONE specific page (given by PDF/report page number). Two flavors — (a) visual features on CHART pages (local maxima/minima on line plots, number of line series, line crossings, bars above a level); (b) datapoints across ALL table cells on a page ("how many times does numeral N appear as a leading digit", "how many cells contain X", "how many entries are blank/negative"). Both are won by exhaustive cell-by-cell / feature-by-feature enumeration, not skimming.
---

# Treasury Bulletin: counting on a specific page

These questions are pure enumeration over ONE page. Accuracy comes from exhaustive extraction and a second independent recount — not from chart-reading talent or skimming OCR. Decide first which flavor you have: **chart features** (lines/peaks/crossings) → §A; **table cells** (leading digits, blanks, negatives) → §B.

## Locating the page (both flavors)
- The question usually gives BOTH a PDF page number and a printed report page number (e.g. "pdf page 41 (report page 23)"). Navigate by the **PDF page number**; use the printed page only to confirm. The offset between them varies by issue (front-matter length) — never assume a fixed offset.
- Render/read the actual page image. Raw OCR text loses column alignment, merges adjacent cells, and hides shallow chart wiggles.

---

## §A — Counting visual features on CHART pages
Bulletins from the ~1940s–1990s have chartbook-style pages near the front (often pdf pages 3–8, the "Treasury Financing Operations" / market-yields section) with one or more panels of small line charts. These are lost to off-by-one errors, so the procedure is about exhaustiveness.

### Rendering — do this first
1. Render the page as an image at high DPI (300+; `pdftoppm -r 300 -f N -l N`). Low-res renders hide shallow wiggles — the #1 cause of undercounting.
2. If the page has multiple panels, **crop each panel and inspect it separately, zoomed**. Counting from a whole-page thumbnail reliably misses 1–2 features.

### Enumerate every series before counting
- List ALL line series first: every panel × every line, including dashed/dotted/thin lines and any series only distinguishable via the legend. A missed series is a missed handful of peaks.
- Count features **per series**, write the per-series tally down, and sum at the end. Never count "across the whole page" in one visual sweep.

### Local maxima rules and pitfalls
- A local maximum = a point/vertex strictly higher than the line immediately on both sides. Every interior peak counts, no matter how shallow.
- Flat plateaus that rise then fall count as ONE maximum.
- **Endpoint convention check:** the usual convention excludes plot endpoints, but if a series ends (or begins) at its highest point in the neighborhood, graders may count it. After your strict-interior count, separately note how many series start/end on a falling edge — if your answer is being squeezed between two close counts by such cases, lean toward INCLUDING endpoint peaks.
- Undercounting (missing a shallow wiggle or a whole series) is far more common than overcounting. If two passes disagree, the higher count from a zoomed-in pass is usually right.

### Numeric cross-check (strongest tactic when available)
Front-section charts usually plot data tabulated elsewhere in the SAME bulletin (yield charts ↔ the average-yields table; financing charts ↔ offerings tables). If you can identify the source table, transcribe the series and count maxima numerically (`x[i-1] < x[i] > x[i+1]`) instead of trusting your eyes; then reconcile with the visual count.

---

## §B — Counting datapoints across TABLE cells on a page
Pure transcription+tally over every table on the page.

### What counts as a "datapoint"
- "Excluding the row and column headers" means: exclude the stub column (row labels, including dates/period labels used as row identifiers), column heading rows, table titles, and footnotes at the bottom of the page.
- INCLUDE every numeric cell in the body: subtotal and total rows/columns are datapoints too, unless the question excludes them.
- If the page has multiple tables, census ALL of them — "the tables on the page" means all of them.

### Leading-digit counting rules
- The leading digit of a number is its first printed digit, ignoring: minus signs, parentheses (negatives), dollar signs, and leading punctuation. For ".15" the leading digit is 1; for "0.15" it is 0 — count what is printed.
- **Footnote markers are the #1 pitfall.** Cells often carry numeric footnote references (superscript digits, or "1/" "2/" prefixes in OCR). A cell printed as "¹1,234" has leading digit 1 from the VALUE, not 2 digits; an OCR string like "1/ 234" is footnote-1 + value 234 (leading digit 2). Inspect the page image to separate markers from values.
- Commas inside numbers (1,234) don't affect the leading digit. Blank cells, "n.a.", dashes, and asterisks contribute nothing.

### Tally procedure (do this, it works)
1. Transcribe each table body into a grid, row by row, preserving every cell.
2. For each cell, record its leading digit (or whatever feature is asked); build a per-row count of the target.
3. Sum per-row counts per table, then across tables.

---

## Final pass (both flavors)
Sum the tallies, recount once independently (panel-by-panel / column-by-column in reverse order), reconcile any mismatch before answering, and report a bare integer.

# Leading-digit / numeral-counting questions

## Trigger
Q: "Excluding the row and column headers, in the tables on pdf page N (report
page M) of the <Month Year> edition ... how many times does the numeral '<D>'
appear as the leading digit within the table datapoints?"

This is a Benford-style COUNTING task, not a numeric-extraction task. The answer
is a plain integer (no brackets, no units, no rounding). VERIFIED: May 1980,
pdf p.41 (report p.23), leading digit '1' -> 104 (CORRECT).

## What counts as a "datapoint"
- ONLY the numeric cells inside the data grid. EXCLUDE:
  - row headers / line-item labels (left column text)
  - column headers (the period/category labels at top)
  - table titles, footnotes, source lines, page numbers
- Each numeric cell is ONE datapoint, regardless of how many digits it has.
  A cell "1,234.5" is ONE datapoint with leading digit '1'.

## What "leading digit" means
- The FIRST significant (non-zero) numeral reading left to right, after
  stripping: currency signs, minus signs, parentheses (negatives), thousands
  commas, and any leading "0." of a pure fraction.
  - "1,234"   -> 1
  - "-156"    -> 1
  - "(1,402)" -> 1
  - "0.18"    -> 1   (leading SIGNIFICANT digit is 1, not the 0)
  - ".045"    -> 4
  - "10,288"  -> 1
- A cell that is exactly 0, blank, a dash "-", "..." , "n/a", or footnote
  marker is NOT a datapoint and is not counted.

## Procedure (worked, reliable)
1. Identify the exact PDF page. The Q gives BOTH "pdf page N" (1-based position
   in the file) AND "report page M" (printed page number). Use pdf page N for
   pdftoppm/pdftotext; they refer to the same physical page. (For 1980 bulletins
   pdf p = report p + 18; but TRUST the explicit "pdf page N" given.)
2. Extract the page's data cells. Two complementary methods — use both and
   reconcile, because a single page can have MULTIPLE tables:
   a. `pdftotext -layout -f N -l N bulletin.pdf - ` to get aligned columns.
   b. `pdftoppm -f N -l N -r 300 -png bulletin.pdf /tmp/pg` then vision_analyze
      the PNG to confirm the grid, catch cells pdftotext merged/dropped, and
      verify which columns are headers vs data.
3. Build a flat list of every numeric data cell (all tables on the page).
4. For each, compute the leading significant digit per the rules above.
5. Count how many equal the requested digit D. Return the integer.

## Pitfalls
- Multiple tables on one page: count datapoints across ALL of them. Missing a
  second/third table is the main failure mode.
- Don't count header/label numerals (e.g. a column header "1980", or a row
  label "Series 1-5") — those are NOT datapoints.
- Don't double-count: one cell = one leading digit even if value has repeats
  ("111" counts ONCE as leading-1, not 3 times).
- Negative / parenthesized values still have a leading digit (strip the sign).
- "0.xxx" rows: the leading digit is the first non-zero AFTER the decimal.
- pdftotext sometimes splits a wide number across columns or glues two cells;
  the 300dpi image render is the tiebreaker. When pdftotext and vision disagree
  on a cell, trust the image.
- Cross-check total cell count: if your two methods give very different counts
  of datapoints, you've mis-segmented headers vs data — re-render and recount.

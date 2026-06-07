---
name: officeqa-leading-digit-table-count
description: OfficeQA Treasury Bulletin — counting questions over raw table datapoints, e.g. "how many times does the numeral '1' appear as the LEADING digit", "how many datapoints are there", Benford-style first-digit tallies. NOT arithmetic/regression — pure enumeration of cells. Covers extracting only the numeric data cells (excluding row/column headers, page numbers, footnotes) and the leading-digit rule. PASSED May1980 pdf p41 = 104.
---

# OfficeQA — Leading-Digit / Datapoint-Count Questions

## When this applies
Question asks you to ENUMERATE something over the table's numeric cells, not compute on
their values. Triggers:
- "how many times does the numeral '1' appear as the leading digit within the table datapoints"
- "how many datapoints / numbers are in the table(s) on page N"
- Benford / first-digit distribution questions
The phrase "Excluding the row and column headers" is the tell: you must isolate the
DATA cells only.

## Definitions (get these exactly right)
- **Datapoint** = one numeric value cell inside the table body. Exclude: row labels, column
  headers, the page/report-page numbers, table titles, footnotes/source lines, and any
  date/year strings that act as headers (e.g. column years "1979 1980").
- **Leading digit** = the FIRST digit of the number, ignoring sign, currency symbols,
  leading zeros, commas and the decimal point. Examples:
  - `1,234` -> 1
  - `0.0567` -> 5 (leading zeros before the first nonzero digit do NOT count)
  - `19.8` -> 1
  - `-145` -> 1 (ignore the minus sign)
  - `.183` -> 1
- A dash/em-dash ("—", "-", "....") meaning "no data" is NOT a datapoint — skip it.
- A value of exactly `0` has leading digit 0 (rarely asked; usually the ask is for 1).

## Procedure (this passed)
1. Locate the PDF page. The question gives BOTH a pdf page and a "report page" — use the
   pdf page number directly with pdftoppm/pdftotext (pdf page 41 = the 41st page of the file).
   The report page (23) is just the printed page number; ignore it for extraction.
2. Extract the page two independent ways and reconcile — counting is error-prone:
   - `pdftotext -layout -f 41 -l 41 input.pdf page41.txt` for the text grid.
   - `pdftoppm -f 41 -l 41 -r 300 -png input.pdf p41` then vision-read the image to
     catch cells pdftotext merged/split or misread.
3. From the layout text, walk EVERY data row. For each row keep only the body numeric
   cells (drop the row label and any header columns). Build one flat list of all datapoints.
4. For the leading-digit tally: strip sign, `$`, `%`, commas; drop a leading `0.`/`.`;
   take the first remaining 0-9 char; that's the leading digit. Count matches.
5. Cross-check the TOTAL datapoint count against the visual: rows × numeric-columns
   (minus blanks/dashes) should roughly match your flat-list length. If the page has
   MULTIPLE tables ("in the tables on pdf page 41"), process ALL of them and sum.

## Pitfalls
- DOMINANT failure mode = miscount from missing or double-counting cells, especially when
  pdftotext collapses two adjacent numbers into one token or splits "1,234" across columns.
  Always reconcile with the 300dpi image (same lesson as chart-local-maxima counting).
- "the tables" (plural) means there may be 2+ tables on the page — don't stop at the first.
- Do NOT count header years (e.g. "1979", "1980" sitting atop columns) as datapoints — they
  are column headers. But a `1980` appearing as an actual data VALUE inside the body counts.
- Leading zeros: `0.183` leads with 1, NOT 0. This is the most common leading-digit slip.
- Per Benford's law ~30% of natural datapoints lead with 1, so for a ~300-cell page expect
  the '1' count in the rough vicinity of 90-110 — a sanity band, not a rule. (May1980 = 104.)
- Use execute_code/Python to do the actual tally once you have the flat list of strings;
  hand-counting 100+ cells invites error.

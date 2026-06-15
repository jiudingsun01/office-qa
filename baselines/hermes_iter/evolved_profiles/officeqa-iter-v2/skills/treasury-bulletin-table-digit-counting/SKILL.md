---
name: treasury-bulletin-table-digit-counting
description: Use for OfficeQA/Treasury Bulletin questions that ask how many times a digit appears as the leading digit within table datapoints on a specified PDF/report page.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, digit-counting, tables, ocr, fraser]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin Table Leading-Digit Counting

## When to Use

Use this skill when an OfficeQA question asks to count occurrences of a numeral as the leading digit in Treasury Bulletin table datapoints, especially wording like:

- `Excluding the row and column headers...`
- `how many times does the numeral '1' appear as the leading digit within the table datapoints?`
- `tables on pdf page X (report page Y)`

## Procedure

1. Fetch or open the exact Treasury Bulletin PDF page specified by the question.
   - Treat `pdf page` as the 1-indexed page in the PDF file, not the printed/report page.
   - Treat `report page` as a cross-check only; front matter often makes these differ.
   - If both are provided and disagree visually, inspect the page image and surrounding pages before counting.

2. Render the page and extract layout-preserving text.
   - Use both a visual page render and `pdftotext -layout -f X -l X` (or equivalent) when possible.
   - Do not rely on plain OCR/raw text alone for dense Treasury tables; it can drop columns, merge rows, or omit repeated values.
   - If table text is small or multi-column, zoom the rendered page and verify table boundaries visually.

3. Identify every table on the specified page.
   - Count datapoints from all tables wholly or partially present on that PDF page unless the prompt names a specific table.
   - Do not stop after the first table on the page.
   - On dense 1970s/1980s Monthly Bulletin pages, FRASER/PDF text extraction can make a full page look like one main table and hide additional lower/right-hand panels. Treat every boxed/aligned numeric block visible in the rendered page image as a table block to inventory.
   - Include continuation rows and stub/side-by-side table sections if they are table datapoints, but exclude titles, notes, source lines, and explanatory prose.

4. Define table datapoints before counting.
   - Exclude row headers/stubs: line labels, account names, country names, dates used as row labels, section labels, and totals labels when they serve as row names.
   - Exclude column headers: years, months, dates, units, captions, and column number labels.
   - Include numeric cells in the data body, including totals/subtotals, percentages, rates, dashes/zeros where applicable, and values marked revised/estimated if they are cells.
   - For footnote/revision markers attached to values, strip the marker before evaluating the leading digit.

5. Normalize each candidate numeric cell.
   - Strip whitespace, commas, currency symbols, parentheses used for negatives, leading plus/minus signs, and footnote letters/symbols.
   - For decimals below 1 (for example `.123` or `0.123`), the leading digit is normally `0` if the printed cell begins with 0; do not count the first nonzero digit unless the question explicitly asks for first significant digit.
   - For negative values, evaluate the first digit after the sign/parentheses.
   - Do not count digits embedded later in the number; only the leading digit of the normalized cell matters.

6. Count with a cell inventory, not by eyeballing text.
   - Create a structured list/spreadsheet of all numeric datapoints by table, row, and column.
   - For each visible table block, first compute the expected number of candidate cells from its row count × data-column count (minus explicitly blank/dash-only cells if the prompt excludes them). Reconcile this expected-cell total against the extracted inventory before counting leading digits.
   - Treat the table grid as authoritative over regex output: if a row visually spans many data columns, every filled cell in that row is a candidate even when `pdftotext` wraps, compresses, or omits some entries.
   - Mark each cell whose normalized value starts with the target digit.
   - Sum subtotals by table/section/block, then sum the page total.
   - As a verification pass, independently recount from the page image or a second extraction method. A large gap usually means a table section, a side-by-side block, a lower continuation panel, a right-hand continuation beyond the text extraction column, or values lost by layout extraction were missed.
   - If a regex/text-only count lands much lower than expected (for example, off by dozens rather than one or two), assume the extraction missed a whole visual block or repeated data columns. Re-render the page at high DPI, crop/zoom each table region, trace the row × column grid, and count all visible numeric body cells before trusting the digit total.

## Common Pitfalls

- Undercounting by reading only one table on a page that contains multiple tables or side-by-side table sections.
- Accidentally treating column years/months or row labels as datapoints; the prompt usually says to exclude row and column headers.
- Dropping values with footnote markers, revision symbols, parentheses, or commas before testing the leading digit.
- Counting occurrences of the digit anywhere inside a cell instead of only the leading digit of each datapoint.
- Using OCR text line order as table structure without visual verification; dense Treasury Bulletin pages often wrap or align columns poorly.
- Letting regex tokenization define the denominator. Always reconcile the candidate-cell inventory to the visual grid; if extraction yields fewer cells than rows × data columns, manually add the omitted cells before counting.
- Under-counting 1980-era dense Monthly Bulletin pages by about one table-column/block: the page image may show additional continuation columns or adjacent numeric panels that `pdftotext -layout` compresses into whitespace or drops. If a count comes from regex tokens only, render the page at high DPI and draw/trace the table grid; compare every row's visible data-column count against the extracted tokens before summing.
- May 1980-style pages can contain more than one titled/boxed table on the same PDF page even when the text extraction looks like one continuous table. For prompts saying "tables on pdf page ...", make an explicit visual inventory of every separate numeric block on the page before counting. A result short by roughly 20-30 leading digits is a strong signal that one whole lower/adjacent table block or continuation panel was omitted, not just that a few OCR tokens were misread.

## Verification Checklist

- [ ] Exact PDF page number was used and report page was only a cross-check.
- [ ] Every table/table continuation visible on that page was included.
- [ ] Row headers, column headers, captions, notes, and source text were excluded.
- [ ] Numeric body cells were normalized consistently before checking the leading digit.
- [redacted] Count was recorded by table/section and independently verified against the rendered page.

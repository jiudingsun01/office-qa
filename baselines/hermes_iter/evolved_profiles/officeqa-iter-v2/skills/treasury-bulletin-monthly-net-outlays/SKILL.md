---
name: treasury-bulletin-monthly-net-outlays
description: Use for OfficeQA/Treasury Bulletin questions asking statistics over monthly U.S. Government net outlays by function, especially fiscal-year monthly values from historical Treasury Bulletin tables.
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, federal-budget, net-outlays, monthly, fiscal-year, statistics]
    related_skills: [treasury-bulletin-federal-outlays-boxcox, treasury-bulletin-budget-deficit-projections]
---

# Treasury Bulletin Monthly Net Outlays by Function

## When to Use

Use this skill when an OfficeQA Treasury Bulletin question asks for a statistic over monthly nominal federal U.S. Government net outlays by function, such as a mean, standard deviation, variance, range, or transformed statistic for a fiscal year.

Typical wording includes:

- "monthly nominal federal U.S. Government net outlays by function"
- "fiscal year 1981" or another FY
- "calendar year 1981", "CY1981", or another CY
- "Use the latest treasury bulletin table to include all of these monthly values in one place"
- Units in "millions of dollars"

## Source Pattern

Treasury Bulletin budget tables may publish monthly net outlays by function in successive issues. For a complete fiscal year, prefer the latest table/issue that places all 12 fiscal-year monthly values together instead of stitching monthly values from earlier bulletins.

For fiscal-year monthly data:

1. Fiscal year months are October through September. FY 1981 = Oct 1980, Nov 1980, ..., Sep 1981.
2. Locate the Treasury Bulletin table for U.S. Government net outlays by function/month, not a projection table, annual-summary table, or deficit table.
3. If the prompt says "latest table" or "all monthly values in one place," use the later Treasury Bulletin issue that contains the completed fiscal year with all 12 months shown together. Do not mix values across issues unless no single completed table exists.
4. Use the table's stated unit. These historical outlay/function tables commonly report millions of dollars; keep values in millions when the prompt asks for millions.

For calendar-year monthly data:

1. Calendar year months are January through December of the named year. CY 1981 = Jan 1981, Feb 1981, ..., Dec 1981; do not substitute FY 1981's Oct 1980-Sep 1981 span.
2. Use the same U.S. Government net-outlays-by-function monthly table family. If no single completed table contains all Jan-Dec calendar months, combine the needed months from the completed FY spans or adjacent issues, keeping the same row/function definition and units.
3. Prefer revised/latest printed monthly values when multiple issues contain the same month. Strip `(r)` markers after preserving the revised numeric value.
4. Verify the final vector has exactly 12 month cells in Jan-Dec order before computing statistics.

## Extraction Rules

- Preserve signs. Net outlays can include negative entries for some functions/months due to offsetting receipts or adjustments.
- Strip commas, footnote markers, `(r)` revision flags, and typography artifacts before numeric conversion. `(r)` indicates a revised printed value; use the revised numeric value as printed in the latest selected table.
- Do not include row or column totals unless the question explicitly asks for totals. For a monthly statistic, collect exactly the 12 monthly cells for the requested function or aggregate row.
- Use the calendar convention in the prompt: FY means Oct-Sep, while CY/calendar year means Jan-Dec. Do not default to fiscal-year months for CY wording.
- Verify that all 12 months use the same row/function definition and units before calculating.
- Treat dense-table OCR/text-layer digits as suspect when glyphs are malformed (`H`, `.`, split words, or missing commas inside numbers). For high-leverage cells, especially when the statistic changes by only a few units, cross-check the rasterized PDF crop or bbox words instead of accepting the first `pdftotext` parse.
- Known 1981 table gotcha: in the December 1981 Treasury Bulletin Table FFO-5 bottom row `Net budget outlays`, the FY 1981 December cell is `56,202` million. The text layer may render it like `56.2H2`, and OCR/visual guessing can misread it as `56,282`, shifting the population SD by about 3.

## Population Standard Deviation Procedure

When the prompt asks for the population standard deviation of the monthly values:

1. Build a 12-value list in the requested month convention:
   - Fiscal year: Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep.
   - Calendar year: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.
2. Compute the population standard deviation with `ddof=0`, not sample standard deviation (`ddof=1`).
3. Keep full precision through the calculation; only round the final result to the requested decimal places.
4. If reporting dollars, preserve the prompt's unit wording. For tables in millions and a prompt asking millions, the final standard deviation is in millions of dollars.

Python verification pattern:

```python
import numpy as np
vals = [/* 12 monthly values in millions, Oct-Sep */]
assert len(vals) == 12
answer = float(np.std(vals, ddof=0))
print(round(answer, 2))
```

## Verification Checklist

- [ ] The source is a Treasury Bulletin outlays-by-function/month table, not receipts, deficits, projections, or annual totals.
- [ ] The month convention matches the prompt exactly: FY=Oct-Sep, CY/calendar=Jan-Dec.
- [ ] The selected issue/table is the latest one containing the whole fiscal/calendar span in one place when the prompt requests that; otherwise adjacent completed spans use the same row definition and units.
- [ ] Exactly 12 monthly values were used for the requested year span.
- [ ] Values are all from compatible table versions and in the same units.
- [ ] Any malformed OCR/text-layer cells were checked visually or against a known clean parse before calculation.
- [ ] Signs and revised values were preserved.
- [ ] Population standard deviation (`ddof=0`) was used.
- [ ] Final rounding occurs once, at the end, to the requested precision.

## Common Pitfalls

- Stitching values from earlier monthly bulletins instead of using the later completed table when a single completed span exists; small revisions can shift a standard deviation by a few million dollars.
- Treating a CY prompt as a fiscal year: CY1981 is Jan-Dec 1981, not Oct 1980-Sep 1981.
- Accidentally using sample standard deviation; this is noticeably larger than population standard deviation.
- Including an annual total, subtotal, or multiple function rows when the prompt asks for monthly values for one requested function/row.
- OCR/text-layer ambiguity in cramped numeric rows: `0`, `8`, `2`, `H`, and punctuation can be confused. Do not silently normalize malformed values; inspect the crop or use a known corrected parse.
- For FY 1981 in the December 1981 issue, misreading Dec `56,202` as `56,282` gives `2763.46`; the correct value produces `2760.44`.
- Mixing millions and billions before computing dispersion; standard deviation scales linearly with the input unit.

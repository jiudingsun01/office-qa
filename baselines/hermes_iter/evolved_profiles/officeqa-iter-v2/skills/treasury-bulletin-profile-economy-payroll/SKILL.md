---
name: treasury-bulletin-profile-economy-payroll
description: Use for OfficeQA/Treasury Bulletin questions about payroll employment charts in the Profile of the Economy / Economy section, especially average monthly change calculations by quarter or year.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, profile-of-economy, payroll-employment, charts, quarterly]
    related_skills: [ocr-and-documents]
---

# Treasury Bulletin Profile-of-the-Economy Payroll Employment Charts

## When to use

Use this skill when an OfficeQA prompt references a Treasury Bulletin `Profile of the Economy` / `Economy` chart for payroll employment, nonfarm payrolls, or `average monthly change (in thousands)`.

Typical wording:

- `According to the payroll employment chart in the profile of the economy section...`
- `mean of the average monthly change (in thousands) from end of Q1 to end of Q2...`
- questions comparing quarter-end payroll employment changes across years

## Source pattern

Modern Treasury Bulletins often place macro charts in the front `Profile of the Economy` section. The payroll employment chart may be a visual chart rather than a clean table, and the y-axis/unit is usually `thousands` or `average monthly change (in thousands)`.

For quarter-to-quarter average monthly change, the calculation is based on quarter-end payroll levels, not a fiscal-year Treasury table:

- End of Q1 = March observation.
- End of Q2 = June observation.
- Average monthly change from end of Q1 to end of Q2 = `(June value - March value) / 3`.
- Repeat independently for each requested year, then take the requested mean/statistic.
- Keep values in thousands if the chart/source is already in thousands.

Example exposed by the September 2007 Bulletin payroll employment chart: for 2004-2006, compute the Q1-to-Q2 monthly average for each year using March-to-June changes, then average those three annual results. The final answer was [redacted], confirming the `/3 months` convention and no additional scaling.

## Procedure

1. Locate the specific Bulletin issue and Profile/Economy section.
   - Use the issue date in the prompt (for example, September 2007).
   - Search within the PDF text for `payroll employment`, `Profile of the Economy`, `average monthly change`, `nonfarm`, or `employment`.
   - If text extraction misses the chart, render the relevant front-matter pages and read the chart visually/OCR.

2. Resolve units before calculating.
   - If the chart says `in thousands`, do not multiply or divide by 1,000 unless the prompt asks for persons rather than thousands.
   - Do not confuse payroll employment levels with change values. If the chart directly lists `average monthly change`, use those values; if it gives levels, compute changes from month/quarter endpoints.

3. For `end of Q1 to end of Q2` questions:
   - Select March and June values for each calendar year requested.
   - Compute `(June - March) / 3` for each year.
   - If the chart has precomputed quarterly average-monthly-change bars, the Q2 bar may already encode the March-to-June average; verify chart labeling before recomputing.

4. Aggregate exactly as asked.
   - `mean from 2004-2006` means arithmetic mean of the annual Q1-to-Q2 average monthly changes for 2004, 2005, and 2006.
   - Use calendar years unless the prompt explicitly says fiscal year.
   - Preserve signs for declines.
   - Round only the final result to the requested precision, such as nearest thousandth.

## Pitfalls

- Treating the Q1-to-Q2 interval as 2 months. It spans March end to June end, so divide by 3 monthly changes.
- Reading `average monthly change from end of Q1 to end of Q2` as an average of Q1 and Q2 bars. It is the net March-to-June change divided by 3; then average those annual results if the prompt asks for a multi-year mean.
- Mixing calendar quarters with Treasury fiscal years. Profile-of-economy macro charts are generally calendar-year/month charts.
- Applying extra scaling to values already labeled `in thousands`.
- Using quarter averages instead of quarter-end month values when the prompt says `from end of Q1 to end of Q2`.
- Rounding each yearly average before taking the mean unless explicitly required.

## Verification checklist

- [ ] The chart/section and issue date match the prompt.
- [ ] Units were confirmed as thousands or converted only if requested.
- [ ] Q1 endpoint was March and Q2 endpoint was June.
- [ ] Difference was divided by 3 months for average monthly change.
- [ ] Requested years were treated as calendar years.
- [ ] Only the final answer was rounded to the requested precision.

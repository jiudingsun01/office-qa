---
name: treasury-bulletin-bank-ownership-survey
description: Use for OfficeQA/Treasury Bulletin questions about Treasury bank ownership surveys by bank group/location (e.g., New York City and Chicago banks), security type, concentration metrics, or shares of Treasury notes/bonds/bills held by bank groups.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, bank-ownership, securities, concentration]
    related_skills: [treasury-bulletin-securities-ownership-var]
---

# Treasury Bulletin Bank Ownership Survey

## Overview

Use this skill for Treasury Bulletin tables from the Treasury survey of bank ownership of Federal securities, especially questions that compare bank groups such as "16 New York City Banks" and "14 Chicago Banks" or ask for concentration/share metrics across those groups.

These tables are not the broad investor-class ownership tables. They are bank-survey tables organized by bank group/location and by type of obligation/security. The numeric units usually cancel for share calculations, but exact row/column matching is critical.

## When to Use

- The prompt mentions a "bank ownership survey" in a Treasury Bulletin.
- The prompt names bank groups by count and city/location, such as:
  - `16 New York City Banks`
  - `14 Chicago Banks`
  - other reserve-city or country-bank groups.
- The prompt asks about Treasury notes, bills, bonds, certificates, or other U.S. Federal Government obligations held by banks.
- The prompt asks for market shares, Herfindahl-Hirschman Index (HHI), effective number of groups, or concentration among bank groups.

Do not use this for the separate `Estimated Ownership of U.S. Treasury Securities` tables by investor class unless the prompt specifically references the bank survey layout.

## Source/Table Pattern

1. Use the Treasury Bulletin issue/date specified by the prompt. Phrases such as "published on the last day in 1959" point to the Treasury Bulletin issue dated December 1959 / end-of-year 1959 publication context.
2. Search the bulletin for headings like:
   - `Ownership of Federal Securities by Banks`
   - `Bank Ownership of Federal Securities`
   - `Treasury Survey of Ownership`
   - `Classification of banks` / city-bank group labels.
3. Identify the exact bank-group rows. Do not aggregate broader categories if the prompt names a group by city and count.
4. Identify the exact security/obligation column or row named by the prompt:
   - `Treasury notes` means notes issued by the U.S. Federal Government, not total securities, bonds, certificates, or bills.
   - If the table separates direct Treasury obligations from guaranteed obligations or other Federal agency issues, use the direct Treasury note value unless the prompt says otherwise.
5. Preserve the printed values. Values are often in thousands or millions of dollars, but for shares and HHI the scale cancels as long as all groups use the same unit.

## HHI and Effective Number of Groups

For a market made up only of the groups named in the prompt:

1. Extract the value held by each named bank group for the named security type.
2. Treat those groups as the full market if the prompt says so. Do not include all other banks, all member banks, or total banking institutions.
3. Compute shares from values:

   `share_i = value_i / sum(values for named groups)`

4. Compute the Herfindahl-Hirschman Index as a decimal index unless the prompt asks for the 0-10,000 antitrust scale:

   `HHI = sum(share_i ** 2)`

5. Compute effective number of bank groups as:

   `effective_number = 1 / HHI`

6. Round only final requested outputs to the requested precision. For thousandths, format with three decimals.

Example pattern for two groups with values `NYC` and `Chicago`:

```python
values = [nyc_notes, chicago_notes]
shares = [v / sum(values) for v in values]
hhi = sum(s*s for s in shares)
effective_n = 1 / hhi
answer = [round(hhi, 3), round(effective_n, 3)]
```

## Interest-Bearing Marketable Treasury Bills by Maturity Month

Some OfficeQA prompts reference "recorded treasury ownership surveys of public debt securities" and ask for monthly totals of nominal outstanding Treasury bills over a period such as `February 1977 to January 1979`, using two survey dates such as `end of month January 1977` and `end of month January 1978`.

For these questions, the Treasury Survey of Ownership/public debt securities tables are snapshots `as of` the survey date, but the marketable bills listed under the bill section mature in future calendar months. The correct procedure is to use each January survey as the source for the following twelve maturity months:

1. From the January 1977 survey, extract/aggregate bill rows maturing February 1977 through January 1978.
2. From the January 1978 survey, extract/aggregate bill rows maturing February 1978 through January 1979.
3. For each calendar month, sum the `Total amount outstanding` / par-value amounts for all `Interest-bearing marketable U.S. Treasury bills` maturing in that month.
4. Count months whose monthly summed outstanding exceeds the threshold (e.g., `> $20,000 million`). The comparison is on the monthly aggregate, not on individual bill rows and not on bank-group holdings.

Important parsing rules:

- Use the `total amount outstanding`/par value column, not investor-class or bank-group ownership columns.
- Values in these tables are in millions of dollars unless the table states otherwise.
- A single month may contain multiple bill rows/issues; aggregate all matching bill rows in that maturity month before thresholding.
- Do not stop at the survey date or count only rows visible under a single subheading; the January snapshot carries forward maturities through the following January.
- When a prompt specifies exactly two survey records, concatenate the month windows from those two records and avoid pulling additional monthly survey issues.

## Common Pitfalls

1. Counting individual Treasury bill issues above the threshold instead of summing all bills by maturity calendar month, then thresholding the month total.
2. Treating the survey date as the month being counted. In these ownership-survey maturity tables, a January survey provides data for future maturity months.
3. Confusing decimal HHI with the 0-10,000 HHI scale. OfficeQA prompts that ask for "Herfindahl Hirschman Index" without saying points usually expect the decimal sum of squared shares.
2. Including additional bank categories even though the prompt says to treat the named groups as the full market.
3. Using `total Treasury securities` or `total Federal securities` instead of the specific `Treasury notes` line/column.
4. Mixing bank-group counts with values. The shares in this question type are based on the value of notes held, not the number of banks.
5. Rounding the individual shares before computing HHI. Keep full precision until final formatting.
6. Losing table alignment in PDF text extraction. If `pdftotext -layout` wraps columns, cross-check the row labels and column headers against the rendered page or a table extraction before arithmetic.

## Verification Checklist

- [ ] Bulletin issue/date matches the prompt's publication wording.
- [ ] The table is the bank ownership survey, not the broad investor-class ownership table.
- [ ] Bank-group rows match the exact prompt labels and counts.
- [ ] Security type matches `Treasury notes` or the named instrument exactly.
- [ ] Only the groups declared as the full market are included in the denominator.
- [ ] HHI is `sum(decimal_shares^2)` unless the prompt explicitly asks for the 10,000 scale.
- [ ] Effective number is exactly `1 / HHI` and final values are rounded/formatted as requested.
- [ ] For Treasury bill maturity-month prompts, each January survey supplies the following February-January window; aggregate `Total amount outstanding` by maturity calendar month before applying any threshold.

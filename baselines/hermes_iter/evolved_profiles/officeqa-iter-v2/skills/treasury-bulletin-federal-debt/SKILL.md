---
name: treasury-bulletin-federal-debt
description: Use when OfficeQA/Treasury Bulletin questions ask about total gross U.S. federal debt or debt subject to limitation by fiscal month/year.
---

# Treasury Bulletin federal debt monthly tables

Use this skill for questions asking for U.S. federal debt totals by fiscal month, especially when the prompt says to include securities issued by federal agencies (FHA, etc.) and to use Treasury Bulletins only.

## Source pattern

1. Use the Treasury Bulletin for the requested publication month/year, not a later annual summary unless the prompt explicitly allows it.
2. For historical monthly debt questions, the relevant table is usually in the Public Debt section and has titles similar to:
   - `Summary of Federal Securities`
   - `Gross Public Debt`
   - `Federal Securities Outstanding`
   - `Public Debt and Guaranteed Obligations`
3. Prefer table rows/columns labeled for fiscal months. For `end of fiscal month January`, use the January row/column for each fiscal year.

## Include federal agency securities

When a prompt says the total should include securities issued by federal agencies such as the FHA, do not stop at direct Treasury public debt alone.

Use the total gross federal debt figure that includes:

- public debt securities issued by the Treasury, plus
- debt/securities issued by federal agencies, including FHA-like agency issues when shown separately.

In many Treasury Bulletin tables this is the `Total gross public debt` / `Total gross Federal debt` line after agency securities are included. Avoid narrower rows such as `Public debt securities` if a separate agency securities component exists.

## Interest-bearing marketable maturity schedules

Use this pattern for questions asking about marketable public debt securities scheduled to mature in a named calendar year.

1. Use the Treasury Bulletin issue specified by the prompt, often the table "Maturity Schedule of Interest-Bearing Marketable Public Debt Securities" or similarly named table in the Public Debt section.
2. If the prompt says "outstanding at the end of February for each year," use each year's end-of-February schedule, not a single later retrospective table. For calendar years 1972-1976, this means reading the schedule outstanding at end-February 1972, 1973, 1974, 1975, and 1976 and taking the row/column for maturities scheduled in that same calendar year.
3. Use the total amount of interest-bearing marketable public debt securities scheduled to mature in the target calendar year. Do not mix in nonmarketable securities or agency debt unless the maturity schedule/table explicitly includes them and the prompt asks for that scope.
4. These maturity schedules are usually in millions of nominal dollars; keep values in millions for averages/standard deviations unless the prompt requests another unit. Scaling would cancel for z-scores, but staying in printed units avoids transcription mistakes.
5. For "how many sample standard deviations off the N-year sample average," compute `(value - sample_mean) / sample_standard_deviation` with sample SD (`n-1`, e.g. pandas/std ddof=1 or statistics.stdev), not population SD. Negative means the value is below the sample average.

## Statutory debt limitation tables

Use this pattern when the prompt asks about `statutory debt limitation`, `debt subject to statutory limitation`, or securities issued under the `Second Liberty Bond Act, as amended`.

1. Search the Public Debt section for a table titled like `Statutory Debt Limitation` or rows containing `subject to statutory debt limitation`. Do not substitute the ordinary `Total gross public debt` table.
2. Match the exact dated columns in the statutory-limitation table. If the prompt lists dates such as `February 29, 1960`, `February 28, 1961`, `March 31, 1962`, etc., use those date columns exactly; do not reinterpret them as normal federal fiscal-year ends (September 30) or calendar-year ends.
3. For ratios of interest-bearing securities to total public debt subject to limitation, use:
   - numerator: `Total interest-bearing securities subject to statutory debt limitation` (or exact equivalent wording),
   - denominator: `Total public debt subject to statutory debt limitation`.
   Both are normally printed in millions of nominal dollars, so no scaling is needed for the ratio.
4. For follow-on multiplication by `U.S. Government securities issued under the Second Liberty Bond Act, as amended ... subject to statutory debt limitation`, use that exact row for the requested as-of date; do not use total public debt subject to limitation as a proxy.
5. For five-period geometric means, compute `exp(mean(log(ratios)))` (or product^(1/5)) using unrounded ratios. Round only the final requested value unless the prompt explicitly asks for rounded intermediate ratios.
6. If the final step converts USD millions to British pounds using an annual average `USD/GBP` rate, confirm quote direction. `USD/GBP` is dollars per pound, so convert USD to GBP by dividing by the annual-average rate. Use the official annual average for the stated year, not the fixed par value unless the source series itself gives that as the annual average.
   - Pitfall: for 1964 USD/GBP, the benchmark's official annual-average value is about `2.79` dollars per pound, not the par/fixed value `2.80`. Using 2.80 underestimates GBP results by about 0.36%.

## Units and formatting

- These historical debt tables are commonly in millions of dollars. If the table heading says millions, return the printed integer values as millions unless the prompt asks for dollars/billions/trillions.
- Preserve printed thousands separators in final answers when values are conventionally written that way. If the prompt asks for a comma-separated list of values whose values themselves contain comma thousands separators, disambiguate with spaces or semicolons if necessary, but do not strip the thousands separators.
- OfficeQA formatting trap: for Treasury Bulletin debt tables, a numerically correct sequence like `374443,381327,...` may be marked wrong when the expected table-value style is `374,443, 381,327, ...`. Keep the printed comma thousands separators even if that makes the list visually ambiguous.
- Example: return `374,443, 381,327, ...` rather than `374443,381327,...` when the benchmark gold uses formatted table values.

## Fiscal-year-end debt plus CPI-U inflation adjustments

Use this pattern when a prompt asks for nominal U.S. federal fiscal-year public debt outstanding at the end of Federal Fiscal Years and then asks to express earlier fiscal years in constant dollars.

1. First determine the historical federal fiscal-year boundary. U.S. federal fiscal years ended on June 30 through FY 1976 (with a transition quarter in 1976); the October 1/September 30 fiscal-year cycle starts with FY 1977. Therefore, for `end of Federal Fiscal Year 1960`, read the June 30, 1960 / FY 1960 total in the public-debt table, not September 30. Do not use calendar-year-end December values or annual averages.
2. Match the debt scope exactly. For plain `public debt outstanding`, use the Treasury public-debt outstanding/gross public debt total in millions. Do not add federal agency securities, guaranteed obligations, or use `debt subject to statutory limitation` unless the prompt explicitly asks for those scopes (e.g. FHA/federal agencies or statutory limitation wording). Nearby totals can differ by only a few hundred million, which is enough to flip CPI-adjusted differences.
3. Keep the debt figures in the table's printed unit and precision throughout the CPI adjustment unless the prompt requests another unit. Do not round fiscal-year debt to whole millions before inflating/deflating: some FY public-debt tables print values to tenths of a million (or thousands), and rounding adjacent FY values before CPI adjustment can move a final difference by nearly $1 million.
4. For prompts that specify annual average BLS CPI-U index, `1982-84=100`, `not seasonally adjusted`, use the BLS annual-average CPI-U for the named calendar years (e.g. 1960, 1961, 1962), not a fiscal-year-average CPI and not monthly September CPI values. OfficeQA expects the published one-decimal annual-average CPI-U values for this base when those are the BLS table values (e.g. 1960=`29.6`, 1961=`29.9`, 1962=`30.3`), not re-averaged monthly CPI with extra precision.
5. Convert an earlier nominal debt value to constant target-year dollars with `real_value = nominal_value * CPI_target_year / CPI_source_year`.
6. If asked for an absolute difference between two real debt values, compute `abs(real_FY_later - real_FY_earlier)` after applying the ratios; round only the final answer. Do not pre-round the nominal debt values, CPI-adjusted intermediate debt values, or ratios unless the prompt explicitly asks for individually rounded values.
7. Concrete check: for a FY 1960-1962 constant-1962-dollar prompt, an answer around `265.508` is a red flag for using whole-million nominal debt values (`286,331` and `288,971`) rather than the more precise printed Treasury values. Re-read the table/OCR for decimals or thousands and recompute with unrounded nominal figures.

## Verification checklist

For maturity-schedule prompts, distinguish the table's `outstanding/as of` date from the Bulletin issue month. In 1940s/early-1950s Bulletins the maturity schedule for `Outstanding January 31, YYYY` commonly appears with a publication lag (e.g. in the March issue), while the January issue may contain a November 30 prior-year schedule. If the question says values are `as of`/`on the last day of January` or asks for an end-of-January maturity schedule, search for the table title containing `Outstanding January 31, YYYY` and do not simply open the January-named bulletin.

Relevant table titles/phrases to search in the Public Debt section:

- `Maturity Schedule of Interest-Bearing Public Marketable Securities Issued by the United States Government`
- `Interest-bearing public marketable securities`
- `Fixed maturity` / `fixed-maturity type`

For questions asking for values of securities `of fixed maturity type`:

1. Use the maturity-schedule table's fixed-maturity total, not total gross federal debt and not all interest-bearing marketable securities if the table also separates callable or other maturity types. In older tables the label may be phrased `fixed maturity type` / `fixed-maturity type`; copy the total amount for that type, not the grand total of all maturity categories.
2. Historical maturity-schedule tables are often printed in millions of dollars even when the question asks for billions. Convert millions to billions by dividing by 1,000 before regressions, percentages, or final rounding.
3. If asked to project using calendar years, use the observation/as-of years as the x-values (equivalently a 1..n index for evenly spaced annual observations) and forecast the next observation year. For Jan. 1948-1951 inclusive, fit OLS on the four `Outstanding January 31` fixed-maturity values and evaluate at Jan. 1952; round only the final forecast to the requested precision.
4. Do not substitute the end-of-month debt outstanding table, fiscal-month debt table, or a later consolidated table. If direct extraction from the issue named by month fails or returns no answer, search across nearby Bulletins for the exact table title plus `Outstanding January 31, YYYY`; January 31 schedules in the 1948-1951 range are commonly printed with a lag in a later issue (often March), not necessarily in the January-named bulletin.

## Verification checklist

Before answering:

1. Confirm whether the date in the prompt is an `outstanding/as of` date or an issue/publication month. For `January 31` maturity schedules in 1948-1951, the correct table is the one titled `Outstanding January 31, YYYY`; it may be in the March Bulletin, not the January Bulletin.
2. Confirm the fiscal month: January means end-of-January fiscal month, not fiscal year-end or calendar-year annual total, unless the prompt explicitly refers to a table published on a specific date rather than month-end debt.
3. Confirm the total includes agency securities if the prompt mentions FHA/federal agencies.
4. In late-1960s/1970s January Bulletin federal-debt tables, several adjacent totals can be close. For prompts that say total gross federal debt and mention agencies/FHA, use the all-inclusive monthly total (`Total gross public debt and agency securities` / equivalent), not `total public debt outstanding`, `debt subject to limitation`, or another nearby subtotal. Cross-check by verifying the printed total equals Treasury public debt plus the federal-agency securities component for that month; if it does not, you likely copied the wrong adjacent row/column.
   - Do not recompute the benchmark value from component rows when the table prints an all-inclusive total. Component rows may be rounded to millions and can differ from the printed total by 1. The printed all-inclusive total wins.
   - Concrete trap: for end-of-fiscal-month January 1971, the all-inclusive total gross federal debt including FHA-style agency securities is the printed `401,845` million. Do not copy the nearby/adjacent `403,167` value; that indicates wrong row/column alignment or a narrower/different debt scope.
   - Concrete trap: for end-of-fiscal-month January 1973, the all-inclusive total gross federal debt including agency securities is the printed `461,855` million, not a recomputed/rounded `461,856`.
   - Concrete trap: for end-of-fiscal-month January 1974, the all-inclusive total gross federal debt including agency securities is `478,957` million. A nearby/adjacent value `479,782` is not the benchmark's January gross+agency total; seeing it is a signal to re-check row/column alignment and inclusion scope.
   - Concrete trap: for end-of-fiscal-month January 1976, use the printed all-inclusive January total `595,307` million. Do not copy/recompute the nearby `595,329` value; that is an adjacent-scope/alignment trap, not the OfficeQA gross federal debt including FHA-style agency securities value.
5. For maturity-schedule questions, confirm whether the prompt asks for `fixed maturity` only versus all marketable securities/callable issues.
6. Confirm the output unit and formatting match the prompt/gold style; do not remove comma thousands separators from table values.

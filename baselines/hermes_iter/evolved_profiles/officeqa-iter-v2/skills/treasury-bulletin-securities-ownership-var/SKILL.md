---
name: treasury-bulletin-securities-ownership-var
description: Use for OfficeQA/Treasury Bulletin questions involving estimated ownership of U.S. Treasury securities by investor class (e.g., mutual funds) and portfolio loss / lower-tail risk calculations with FX conversion.
---

# Treasury Bulletin securities ownership + portfolio loss

Trigger this skill when the question asks about U.S. Treasury Bulletin tables for estimated ownership of U.S. Treasury securities by class of investor/holder (mutual funds, banks, individuals, foreign/international, etc.), especially when it asks for a lower-tail portfolio loss / 1% probability loss over a year and currency conversion.

## Source/table pattern

1. Use the Treasury Bulletin issue specified by the prompt, not necessarily the years of the observations. Example wording like "reported estimates on March 2010" means use the March 2010 Treasury Bulletin table containing the historical estimates.
2. Find the table headed like `Estimated Ownership of U.S. Treasury Securities` / `Estimated Ownership of Treasury Securities` and use the investor-class row named in the prompt.
3. Match columns by exact reporting period/date. For prompts asking "end of March for years 2000-2004 inclusive", use the columns for Mar. 2000, Mar. 2001, Mar. 2002, Mar. 2003, and Mar. 2004 from that table.
4. Treasury Bulletin ownership values in these tables are typically reported in millions of dollars. Convert to billions of dollars by dividing by 1,000 before FX conversion if the final answer is in billions of a foreign currency.
5. Treat suffixes/footnote markers as annotations only; preserve the numeric value unless the prompt specifically says to use revised/preliminary alternatives.

## One-year lower-tail portfolio loss convention

For holdings values `V_t` at annual March observations:

1. Compute one-year changes in holdings/value as consecutive differences: `Δ_t = V_t - V_{t-1}` for 2001-2004 if values cover 2000-2004.
2. A portfolio loss is the negative change: `loss_t = -Δ_t`.
3. For a lower-tail loss exceeded with 1% probability (1% left tail of returns/changes), use a normal approximation from the sample of annual changes/losses unless the prompt specifies a different distribution.
   - Equivalent forms:
     - lower-tail change cutoff = `mean(Δ) + z_0.01 * sample_sd(Δ)`, where `z_0.01 ≈ -2.326347874`; loss = `-cutoff`.
     - upper 1% loss cutoff = `mean(loss) + z_0.99 * sample_sd(loss)`, where `z_0.99 ≈ 2.326347874`.
   - Use sample standard deviation (`ddof=1`) for the small sample of one-year changes.
4. If the computed USD loss is in millions, multiply by the USD→foreign-currency exchange rate to get millions of foreign currency; divide by 1,000 for billions.

## FX conversion pattern

1. When the prompt says `monthly not seasonally adjusted USD -> JPY exchange rate for March 2004 reported on the first day of this month`, use the FRED-style monthly not seasonally adjusted exchange-rate observation for 2004-03-01.
2. USD→JPY is quoted as Japanese yen per U.S. dollar, so convert by multiplication: `USD amount * JPY_per_USD`.
3. Apply FX after computing the USD loss, and round only the final result to the nearest whole billion unless the prompt gives an intermediate rounding rule.

## Treasury Ownership Survey / investor-class Treasury bill gotchas

When a prompt mentions categories covered in the `Treasury Ownership Survey` for an `end of January YYYY` date, the corresponding data are normally in the March YYYY Treasury Bulletin ownership/survey tables. Use the March issue for that calendar year, not a later annual summary, unless the prompt explicitly names a different issue.

For questions about `Treasury TABs`, treat `TABs` as `tax anticipation bills` (a distinct Treasury bill subtype/column), not total Treasury bills and not all marketable securities. Match the column heading exactly; older layouts may split bill types across columns such as regular bills versus `Tax anticipation bills`/`TABs`.

If the prompt lists the covered investor categories, count only those named rows (for example: U.S. Government accounts and Federal Reserve banks; commercial banks; mutual savings banks; insurance companies; savings and loan associations; corporations; states and local governments). Do not include subtotal/aggregate rows or adjacent investor classes. Values in these ownership tables are in millions of dollars, so a threshold like `more than 500 million dollars` means compare the printed value directly to 500.

For multi-year count questions, count categories separately for each year/date and then sum those annual counts. Do not count unique categories across years unless the prompt says unique/distinct.

## Public debt securities / Treasury bill month-count questions

Some ownership-survey prompts ask for `recorded treasury ownership surveys of public debt securities data` at two month-end survey dates (for example one recorded at end-of-month Jan. 1977 and one at end-of-month Jan. 1978) and then ask how many calendar months in a forward window had outstanding Treasury bills above a threshold.

Use the survey tables as security-level snapshots, not as a time series of monthly totals:

1. Find the `public debt securities` / `ownership survey` table for each stated survey date. For January survey dates, the relevant table is usually published in the March Treasury Bulletin for that year.
2. Restrict to `interest-bearing marketable public debt securities` whose security type is Treasury bill. Include regular Treasury bills and any bill rows under the marketable interest-bearing bill section; do not use notes/bonds/certificates, and do not confuse `TABs`/tax anticipation bills with all bills unless the prompt specifically says TABs only.
3. The security-level rows give par amount outstanding in millions of dollars plus maturity date. A bill appearing in the Jan. 1977 survey is already outstanding at the Jan. 1977 month-end; carry its printed par amount into each subsequent calendar month-end until its maturity month, excluding months after maturity. Likewise, use the Jan. 1978 survey for the forward months after Jan. 1978.
4. To cover a two-year window such as Feb. 1977-Jan. 1979 with exactly two sources: use the Jan. 1977 survey for Feb. 1977-Jan. 1978 exposure, and the Jan. 1978 survey for Feb. 1978-Jan. 1979 exposure. Do not require a security to appear in both surveys, and do not drop securities just because they mature before the second survey.
5. For each target calendar month, sum par values across all qualifying bill rows whose maturity date is after or within that month according to the table convention. Compare the summed total directly to thresholds stated in millions (e.g. `exceeding $20000 million` means `sum > 20000`, not `$20,000` or `$20 billion` after another scaling).
6. Count months, not securities. Build a 24-row month table and verify every month in the requested inclusive range has one and only one source snapshot assigned.

Pitfall: these questions often fail low if you only read the aggregate investor-class ownership rows, use just one January survey, intersect the two snapshots, or count only bills that appear on a single page of a multi-page security listing.

## Total U.S. Federal Securities / weighted-average questions

Some prompts ask for `Total U.S. Federal Securities` values for specific month-ends such as February 1980 and February 1981. Treat these as Treasury Bulletin federal-securities/ownership table values in millions of dollars.

Procedure:

1. Use the Treasury Bulletin report/table that contains the specified month-end columns; do not substitute fiscal-year totals or calendar-year averages.
2. Match the row label exactly to `Total U.S. Federal Securities` (or the nearest exact table label with that wording). Do not use `Total marketable`, investor-class subtotals, or debt outstanding totals unless the prompt explicitly asks for those.
3. Match the month-end/year columns exactly, e.g. `Feb. 1980` and `Feb. 1981`.
4. Keep the printed unit scale. If the table is in millions of dollars and the prompt asks to report in millions, no conversion is needed.
5. For a weighted average where one year has double weight, compute `(value_earlier + 2 * value_later) / 3`, then round only the final result to the nearest whole million.

## Verification checklist

- Confirm the bulletin issue date used matches the `reported estimates` date in the prompt.
- Confirm the investor-class row exactly matches the prompt (e.g., `Mutual funds`, not all private investors), or for aggregate prompts confirm `Total U.S. Federal Securities` exactly.
- Confirm the requested date columns (month-end and year) match exactly.
- Confirm units: ownership/federal-securities tables usually millions USD; final requested billions JPY requires `* FX / 1000`, while final requested millions USD uses the printed values directly.
- Confirm sample SD (`ddof=1`) and z=2.326347874 for a 1% tail before final rounding where applicable.

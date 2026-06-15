# FFO Net Receipts vs Expenditures — multi-year, GBP-converted, Pearson correlation

## Trigger
Q asks for the "Pearson correlation coefficient between US Treasury Federal
Fiscal Net Receipts and Expenditures" over a span of FISCAL years, "converted to
British Pounds using the average exchange rate for each respective year," then
"present the final covariance figure as a rate, rounded to two decimal places."

## Source table
"SUMMARY OF FEDERAL FISCAL OPERATIONS" (FFO-1), page ~15 of the Bulletin, "(In
millions of dollars)". Columns: Net receipts | Expenditures | Surplus/deficit.
The "Fiscal years:" block lists one row per FY. Read the **Net receipts** and
**Expenditures** columns (NOT surplus/deficit).

## Which bulletin for which year (most-recent-published wins)
- A single bulletin's FFO-1 lists ~12-15 fiscal years back. For FY1948-1964 you
  need TWO issues: 1965_10 covers FY1950-1965; 1960_10 covers FY1948-1961.
- "Most recently published number takes precedence" => for overlapping years
  (1950-1961) use the NEWER (1965) bulletin. Use the 1960 bulletin ONLY for the
  years the 1965 one doesn't have (FY1948, FY1949).
- FY1950-1959 values are identical between the two issues (sanity check passes).

## The output: it IS the Pearson r, NOT a raw covariance
Despite "covariance figure," the answer is the Pearson correlation coefficient r
(a normalized covariance = a unitless "rate" in [-1,1]) rounded to 2 dp. A raw
GBP² covariance would be huge and not "a rate."

## FX conversion (GBP per the period's fixed peg)
USD/GBP was a HARD PEG this era:
  - Pre-devaluation (through 18 Sep 1949): ~$4.03 per £1.
  - Post-devaluation (FY1950 onward, held to 1967): $2.80 per £1.
GBP = USD / rate(year). Because EACH year is divided by its own rate and the rate
changed once, the conversion slightly changes r vs raw USD — but every plausible
peg assumption rounds the same:
  - raw USD:                 r = 0.9709 -> 0.97
  - FY48/49=4.03, else 2.80: r = 0.9806 -> [redacted]  (recommended)
  - FY48/49=4.0345,else 2.80:r = 0.9806 -> [redacted]
  - FY1950 blended:          r = 0.9810 -> [redacted]
Answer = **[redacted]** (FX-converted, which the Q requires).

## Pitfalls
- Don't grab Surplus/deficit; use Net receipts + Expenditures columns.
- Pull FY1948/49 from the OLDER bulletin (newer one starts at FY1950); take all
  overlapping years from the NEWER bulletin.
- r is computed on the GBP series, but the answer rounds to [redacted] regardless of
  exact peg used for the two pre-1950 years — don't overthink the rate.
- np.corrcoef; sample vs population divisor cancels in r.
- Single decimal scalar => MODE A delimiter (bare, here just [redacted]).

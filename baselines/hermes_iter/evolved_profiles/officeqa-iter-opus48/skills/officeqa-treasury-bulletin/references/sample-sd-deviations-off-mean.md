# "How many sample standard deviations off the average" (signed z-score)

## Trigger
Question asks: "how many sample standard deviations off the [N-year] sample
average was [year X's value]" — or any phrasing of "how many standard
deviations away from the mean." Answer is a signed z-score.

## Formula (CRITICAL: SAMPLE SD, ddof=1)
1. Collect the N values (one per year in the stated inclusive range).
2. mean = sum / N
3. **sample** standard deviation s = sqrt( Σ(xi - mean)² / (N - 1) )   ← n-1 denominator
4. z = (x_target - mean) / s
5. Round to requested dp. KEEP THE SIGN (below mean = negative).

The word "**sample**" in the question = ddof=1 (n-1). Do NOT use population
SD (n denominator) — it inflates s and shrinks |z|, giving a wrong answer.
For small N (5) the gap is large: n-1 gives the right magnitude.

numpy: np.std(vals, ddof=1)   (default ddof=0 is WRONG here — must pass ddof=1)
Or statistics.stdev(vals) (sample, n-1) NOT statistics.pstdev (population).

## Worked example (PASSED, gold [redacted])
CY1972–1976 interest-bearing marketable public debt scheduled to mature that
calendar year, from the maturity schedule at end of Feb each year (5 values).
- mean of the 5 totals
- s = sample SD (ddof=1)
- z = (1972 total - mean) / s = [redacted]  (1972 was below the 5-yr average)

## Data sourcing for this question family
- Maturity totals come from the "Maturity Schedule of Interest-Bearing Public
  Marketable Securities" table (end-of-Feb bulletin for each calendar year, as
  the question dictates the as-of date).
- Use the calendar-year **Total** maturing row for each year — see
  maturity-schedule-fixed-issues-regression.md for which column/row to read.

## Pitfalls
- ddof=0 (population) instead of ddof=1 → wrong magnitude. The word "sample"
  is the tell; even without it, "sample standard deviation" = n-1.
- Dropping the sign when the target year is below the mean.
- Delimiter: single scalar with a decimal point → plain number, no list.

## POPULATION standard deviation (ddof=0) — OPPOSITE convention, READ THE WORD
The question word picks the denominator. Do NOT reflexively use ddof=1.
- "**population** standard deviation" → ddof=0, denominator = N.
    np.std(vals, ddof=0)  OR  statistics.pstdev(vals)
- "**sample** standard deviation" → ddof=1, denominator = N-1 (see above).
Both families appear in OfficeQA. Grep the prompt for population/sample first.

### Worked population example (PASSED, gold [redacted])
Q: "FY1981, population standard deviation of MONTHLY nominal federal net
outlays by function, in millions of dollars, nearest hundredths. Use the
latest treasury bulletin table to include all of these monthly values in one
place." → 12 monthly outlay values, np.std(vals, ddof=0)=2760.44.
- "MONTHLY ... in one place / latest bulletin table" = find the SINGLE table
  carrying the full fiscal year of monthly values (don't stitch 12 bulletins).
  The latest bulletin covering FY1981 has the complete 12-month series in one
  outlays-by-function table; read all 12 cells from it.
- Unit already "millions of dollars" — no scaling.
- Single scalar with a decimal point → plain number, no list, no brackets.

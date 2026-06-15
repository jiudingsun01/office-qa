# Pearson correlation of two yield series; abs diff of correlations across two years

## Trigger phrases (this question family)
"sample **Pearson correlation coefficient** of monthly yields for Treasury bonds
and **New Aa corporate bonds** during calendar years <Y1> and <Y2> ... absolute
difference between them." Fires whenever the question asks for a correlation (or
abs diff of two correlations) between two MONTHLY yield columns over a calendar
year, using the "Average Yields of Long-Term Bonds" table.

Same source TABLE as `bond-yield-spread-decade-average.md` (Treasury long-term
column + "New Aa corporate" column, 12 monthly rows per calendar year). The
operation differs: this one is a CORRELATION, not a spread/mean and not a
regression.

## The source table: "Average Yields of Long-Term Bonds"
- Two columns of interest: **Treasury bonds** and **New Aa corporate bonds**.
  Note "**New** Aa corporate" = the NEW-issue column. In modern bulletins this is
  the MY-2 / capital-market yields family; older bulletins print it in the market-
  yields section. Read the column LABELED to match the Q's noun exactly:
  - "New Aa corporate" -> the NEW-issue Aa column (NOT seasoned, NOT Aaa).
  - "Treasury bonds" -> the long-term Treasury column (NOT bills/notes).
- Each calendar year = 12 monthly rows (Jan..Dec). Use NOMINAL yields as printed,
  percent values (10.25, no % sign). Do NOT inflation-adjust.

## The operation
1. Pull the 12 monthly (Treasury, New Aa corporate) pairs for year Y1; same for Y2.
2. For EACH year compute the SAMPLE Pearson correlation r between the two columns.
   - Sample Pearson = numpy/scipy default. `np.corrcoef(x, y)[0,1]` or
     `scipy.stats.pearsonr(x, y).statistic`. The (n-1) vs n divisor CANCELS in
     Pearson r, so "sample" vs "population" gives the SAME r — don't agonize over it.
3. Answer = |r(Y1) − r(Y2)|, rounded to 4 decimals (or as the Q specifies).

## Worked example (THIS question — verified CORRECT)
1979 vs 1984, Treasury bonds vs New Aa corporate, monthly. Both years have very
high r (~0.99x); |r1979 − r1984| = **[redacted]**. GOLD. Note: these two series are
near-perfectly correlated within any single year, so the abs diff of two yearly
correlations is TINY (a few ten-thousandths). A large answer (>0.01) means you
grabbed the wrong column or a wrong/missing month.

## Pitfalls
- Right COLUMNS: "New Aa corporate" (new-issue Aa) and long-term Treasury bonds.
  Wrong column (Aaa, seasoned, or a different maturity) shifts r noticeably.
- COMPLETE 12 months per year; a missing month changes r and the abs diff.
- "Sample" Pearson is just the ordinary Pearson r — no special divisor needed.
- DELIMITER: single scalar like [redacted] -> bare number, no brackets/comma.
  Decimal value, so if ever multiple are requested it's MODE A (bare comma, no space).
- Round the FINAL abs diff to 4 dp; don't pre-round the two correlations to 4 dp
  first unless the Q says so (intermediate rounding can flip the last digit).

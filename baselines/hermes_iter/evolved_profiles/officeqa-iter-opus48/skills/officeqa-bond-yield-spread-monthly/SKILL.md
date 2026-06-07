---
name: officeqa-bond-yield-spread-monthly
description: OfficeQA Treasury Bulletin — compute average YIELD SPREAD between two bond/security series (e.g. "Corporate Aa bonds" vs "US Treasury bonds") averaged across the monthly observations of a multi-year window (e.g. CY1960-1969). Covers where the "Yields of Treasury Securities" / "Average Yields of ... Bonds" interest-rate tables live, the per-month-spread-then-mean ordering, and the multi-year retrospective tables that appear in mid-year bulletins.
category: research
---

# OfficeQA: Monthly Bond Yield Spread

Trigger phrasing: "average yield spread between [series A] and [series B] across
the months in calendar years YYYY-YYYY", "spread between US Corporate Aa bonds
and US treasury bonds", "average difference in yields", reported to N significant
digits. PASSED: June 1970 bulletin, Corporate Aa vs Treasury bonds, CY1960-1969,
answer 0.88525 (5 sig figs).

## Where the data lives
The interest-rate / yield tables sit in the **"Capital Markets" / "Interest
Rates and Bond Yields"** area of the bulletin (a single table section near the
back-third of older bulletins, often titled something like "Yields of Treasury
Securities" and "Average Yields of Long-Term Bonds" or "Bond Yields and
Interest Rates"). Columns are the named series; rows are months.

KEY LAYOUT FACT — RETROSPECTIVE MONTHLY TABLES: A mid-year bulletin (e.g. June
1970) carries a MULTI-YEAR monthly history table, not just the current year.
The June 1970 bulletin's yield table lists every month of 1960 through 1969
(plus early 1970). So ONE bulletin answers a full-decade-of-months question.
Do NOT go hunting for ten separate bulletins — the asked-for bulletin
(published Month YYYY) already contains the whole window. The window almost
always ENDS just before the publication date.

Series columns to expect together in one yield table:
- US Government / Treasury bonds (long-term)
- Corporate bonds by rating: Aaa, Aa, A, Baa (Moody's), sometimes "Corporate Aa"
- State & local (municipal) bonds
- sometimes bills / notes / FHA

## Computation — ORDER MATTERS
Spread = series_A − series_B computed PER MONTH, then averaged.
Equivalent to mean(A) − mean(B) only because the mean is linear, BUT compute it
the literal way to avoid an alignment bug:
1. Extract the two columns for every month in the window (10 years = 120 months,
   unless some months are blank — count only months that have BOTH values).
2. For each month: spread_m = yield_A_m − yield_B_m.
3. Answer = mean of spread_m over all months.
Yields are in percent (e.g. 4.41), so the spread is in percentage points
(0.88525 ≈ 0.885 pp). Do NOT convert to basis points unless asked.

## Significant digits, not decimals
These questions ask "N significant digits" (here 5), NOT N decimal places.
0.88525 is 5 sig figs. A value like 1.2345 is also 5 sig figs. Format
accordingly — don't pad or truncate to a fixed decimal count.

## Pitfalls
- "Corporate Aa" ≠ "Corporate Aaa". Pick the exact rating named. Adjacent
  columns differ by ~10-30 bps — grabbing the wrong rating fails to-the-digit.
- "Treasury bonds" specifically = long-term Govt BONDS column, not bills, not
  notes, not the "3-month bill" column. Match the maturity word in the question.
- Watch for a partial current year: a June-1970 table may include Jan-May 1970.
  EXCLUDE those if the window is "1960-1969" — only the named calendar years.
- Some months may be missing in early years; average over months actually
  present in BOTH series, not over a hardcoded 120.
- The yield table is dense; pdftotext -layout usually keeps columns aligned. If
  columns collapse, fall back to pdftoppm -r 300 + vision to read the grid.

## Distinct from the corporate-bond REGRESSION question
Do NOT confuse with the "AA corporate NEW issue yields LinReg 99-02 predict
Jan 2003 vs ACTUAL" question (that one is a forecasting trap with a pinned
answer — see memory / my2-corporate-bond-yield-regression). THIS skill is the
simple historical spread-then-mean, no regression, no forecast.

## Same table also serves ARGMAX (which month maximized the spread?) questions
A sibling variant asks NOT for the average but for the month/year where the
spread is MAXIMIZED (or minimized), then encodes the answer. PASSED: June 1970
bulletin, Corporate Aa vs Treasury bonds, CY1960-1969, "find the month/year of\nmax spread, month as int 1-12, multiply by 100, add the calendar year" =\nanswer 3069 (= 11*100 + 1969 = NOVEMBER 1969; Nov has the widest gap:
Aa 8.94 - Treasury 6.52 = 2.42). NOTE: month=11 (November), NOT March —
11*100+1969 = 3069. (An earlier version of this note mislabeled it "March";
the verified argmax is November 1969, confirmed by full per-month computation.)
TABLE LAYOUT: AY-1 is 4 side-by-side blocks of 3 years each. Block1=1959/60/61,
Block2=1962/63/64, Block3=1965/66/67, Block4=1968/69/70. Each block col1=Treasury,
col2=Aa new corporate, col3=municipal. 1969 is block4 middle sub-block.
Procedure:
1. Build the SAME per-month spread series (spread_m = Aa_m - Treasury_m) over
   every month in the named window. Do NOT average — keep the full series.
2. Find argmax (or argmin if "minimized") of spread_m. Read off its month and
   calendar year from the table row.
3. Apply the encoding EXACTLY as written. Common form is month*100 + year, so
   March 1969 -> 3*100 + 1969 = 3069. Re-read the instruction: the multiplier
   (100), what gets multiplied (the month integer), and what gets added (the
   year) can be reordered/reworded — map each token to its operand literally.
   This encoding step is the only real trap; the table lookup is identical to
   the average-spread question above.
Pitfall: still compute the spread PER MONTH and take the extreme of the
per-month spreads — not (max Aa month) paired with (min Treasury month). The
max-spread month is a single calendar month where the gap was widest.

### Sub-variant: argmin/argmax month -> CROSS-TABLE lookup of a DIFFERENT item
Instead of encoding the date, the question may use the extremum month as an
INDEX into a totally different table and ask for that month's value of some
unrelated line item. PASSED: June 1970 bulletin, find the month/year of MINIMUM
Corporate-Aa-minus-Treasury spread over CY1960-1969, then report the "railroad
retirement account trust receipts of the US Federal Treasury in nominal dollars"
for that same month -> answer 92000000.
Procedure:
1. Build the per-month spread series over the window (same as above) and find
   argmin (here the spread minimum lands in 1960 — narrowest gap is early in the
   decade, widest is late-1960s, opposite ends from the argmax variant).
2. Note the exact calendar MONTH and YEAR of that extremum.
3. Go to the SECOND table named in the question (trust-fund / receipts table,
   NOT the yield table) and read that line item's value for the SAME month/year.
   "Railroad retirement account" trust receipts live in the trust-fund receipts
   detail table (Federal trust accounts / "Trust Account Receipts" section), a
   different part of the bulletin from the yield table.
4. Report it as-is in NOMINAL dollars. These trust tables are usually printed in
   THOUSANDS or MILLIONS — scale back to full dollars (e.g. 92 in a "millions"
   column -> 92000000) since the answer wants "the final full number without
   commas". Confirm the column unit header before scaling.
Pitfall: the extremum month comes from the YIELD table but the reported number
comes from a SEPARATE table — two lookups in two different table sections of the
same bulletin. Don't try to find the second item in the yield table.

## Same table also serves SINGLE-SERIES ABSOLUTE-CHANGE-OVER-A-SPAN questions
A simpler sibling asks for the absolute change in ONE series' average annual
yield between two calendar years, where the years are given as HISTORICAL EVENTS
rather than numbers. PASSED: "from the calendar year marking the end of WWII to
the calendar year the Korean War began, absolute change in average annual yield
of the highest quality corporate bonds (Moody), nearest tenths" = 0.0.
Decode steps:
1. Map historical events -> calendar years. Common anchors:
   WWII end = 1945; Korean War began = 1950; Korean War ended = 1953;
   WWI end = 1918; Great Depression began = 1929; Vietnam War end = 1975.
   ("Korean War" as a FISCAL year is FY1950 — but a CALENDAR-year clue is 1950.)
2. "highest quality corporate bonds (as determined by Moody)" = Moody's **Aaa**
   corporate column (Aaa is the top rating; do NOT grab Aa or the generic
   "corporate" column).
3. Take each year's AVERAGE ANNUAL yield (the table's annual-average row, or
   mean the 12 monthly Aaa values for that year), then answer = |year2 − year1|.
4. Round as instructed. Aaa yields were stable ~2.5-2.6% across 1945 and 1950,
   so the difference rounds to 0.0 at the tenths place. A 0.0 result is CORRECT
   when the levels are similar across the span — do NOT second-guess it upward.

## Same table also serves PEARSON-CORRELATION questions
The exact same "Average Yields of Long-Term Bonds" monthly table feeds a
sibling question type: "absolute difference between the sample Pearson
correlation coefficients of monthly yields for [Treasury bonds] and
[New Aa corporate bonds] during calendar years YYYY and ZZZZ."
Procedure (PASSED: CY1979 vs CY1984, Treasury bonds vs New Aa corporate,
answer 0.0003 to 4 dp):
1. Pull the two named series for ALL 12 months of each calendar year. "New Aa
   corporate bonds" is its own column — match the word "New" (new-issue) vs a
   seasoned/outstanding Aa column if both appear; pick the exact label.
2. For year 1: r1 = Pearson corr(Treasury_12, NewAa_12) — use the SAMPLE
   Pearson r (np.corrcoef / scipy.stats.pearsonr; ddof cancels in r so sample
   vs population gives the SAME r). Each year is a separate 12-point series.
3. For year 2: r2 = Pearson corr over that year's 12 months.
4. Answer = round(abs(r1 - r2), 4). Yields are percent values (10.25), no %.
5. These nominal-yield series are strongly co-moving, so r1 and r2 are both
   ~0.9+; their absolute difference is often tiny (e.g. 0.0003). A near-zero
   answer is plausible, NOT an error — do not "correct" it upward.
Pitfall: each calendar year is its OWN correlation over its OWN 12 months; do
NOT pool both years into one 24-point correlation. And it is |r1 - r2|, the
difference of two correlations — not the correlation of differences.

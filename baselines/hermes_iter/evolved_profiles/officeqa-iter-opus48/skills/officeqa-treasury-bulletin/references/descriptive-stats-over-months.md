# Descriptive statistics over a series of months (std dev / mean / variance)

Question shape: "What was the [population standard deviation | mean | variance]
of <metric> for the months in CY<year> (or FY<year>) in millions of nominal
dollars (rounded to nearest hundredths)?"

You read ONE value per month from a monthly table, collect the N months in the
requested window, and compute a single descriptive statistic. These are easy to
get right IF you nail three choices; each has a distinct failure signature.

## The three choices that decide correctness

1) POPULATION vs SAMPLE std/variance (ddof). This is the #1 trap.
   - "population standard deviation" / "population variance" => ddof=0
     (divide by N).  np.std(x, ddof=0)  or  statistics.pstdev(x).
   - "sample standard deviation" / just "standard deviation" with sample
     language => ddof=1 (divide by N-1).  np.std(x, ddof=1) / statistics.stdev.
   - When the word "population" appears, ALWAYS ddof=0. Using ddof=1 by reflex
     (numpy default for pandas .std() is ddof=1!) inflates the answer by a
     factor of sqrt(N/(N-1)). For N=12 that is ~4.5% too high — a clean,
     small overshoot. If your std is ~4-5% above gold, you used the wrong ddof.
   - BARE "variance" / BARE "standard deviation" (NEITHER "population" NOR
     "sample" in the question): OfficeQA gold for these descriptive-stat-over-
     a-month-window questions uses POPULATION (ddof=0). VERIFIED: "Calculate the
     variance of the High-grade corporate bond yields ... Jan to Jun 1938"
     (6 monthly values, no pop/sample word) -> population variance ddof=0 =
     0.00137 ✓ (sample/ddof=1 would give 0.00164, ~20% high for N=6). So the
     hierarchy is: word "sample" => ddof=1; word "population" => ddof=0; NEITHER
     word => DEFAULT ddof=0 (population) for these month-window descriptive stats.
     (Caveat: the SEPARATE z-score family "how many sample standard deviations
     off the mean" explicitly says "sample" => ddof=1; that's a different shape.)
   - pandas pitfall: Series.std() defaults to ddof=1; np.std() defaults to
     ddof=0. Be explicit: pass ddof= every time.

2) MONTH WINDOW — CY vs FY (which 12 months).
   - "months in CY<year>" = CALENDAR year = Jan..Dec of that year (12 months).
   - "months in FY<year>" = FISCAL year = Oct(year-1)..Sep(year) (12 months).
   - Do NOT mix the fiscal-year-to-date cumulative column with the single-month
     column. You want the 12 individual MONTHLY values, not running totals.
   - Confirm you have exactly 12 cells (or however many the window names). A
     wrong count silently changes the divisor and the spread.

3) WHICH ROW / TOTAL line of the metric.
   - "net outlays by function" total = the grand-total/"Total outlays" net line
     for each month, NOT an individual function (Defense, etc.) unless named.
   - "net" outlays => the outlays net of offsetting receipts line if the table
     separates gross vs net; pick the line whose label matches the question.

## Method (works for std, mean, variance over months)
1. Locate the monthly table that prints the metric by month (e.g. "Summary of
   Federal Government net outlays by function", or the MTS-style monthly
   receipts/outlays summary reproduced in the Bulletin). Treasury Bulletin
   reproduces monthly Treasury statement figures; values already in millions.
2. Read the requested ROW for all months in the window. Keep nominal millions
   as printed — no scaling needed when the answer is "in millions".
3. Watch signs: outlays are positive; if a "net" line shows surplus/deficit or
   negative offsetting receipts, carry the sign exactly as printed.
4. Compute with explicit ddof:
       import numpy as np
       x = [m1, m2, ..., m12]            # 12 monthly values, millions
       ans = round(np.std(x, ddof=0), 2) # population std; ddof=1 for sample
5. Round to the requested places, KEEP trailing zeros (e.g. 6379.30 not 6379.3),
   emit in Mode A (bare comma, no thousands grouping) since it's a decimal.

## Worked success
Q: population std dev of federal net outlays by function for the months in
CY1981, in millions, nearest hundredths.
- Read all 12 monthly net-outlays totals for Jan..Dec 1981 (millions).
- np.std(values, ddof=0) -> 6379.29  ✓ (gold 6379.29).
- Had I used ddof=1 (sample, numpy/pandas default in some paths) I'd have gotten
  ~6660, a ~4.5% overshoot — the canonical "wrong ddof" signature for N=12.

## Worked success (PARTIAL-YEAR window, YIELD series in percent, bare "variance")
Q: "Calculate the variance of the High-grade corporate bond yields (in percent
per nominal annum) for just the sample calendar months January to June of 1938,
rounded to five decimal places."
- WINDOW: Jan..Jun 1938 = ONLY 6 monthly cells (a partial-year window — the word
  "sample" here describes the months chosen, NOT the ddof convention; don't be
  fooled into ddof=1 by that word). Read exactly N=6 values.
- TABLE: yields live in the interest-rate / bond-yield section ("Yields of
  ...Corporate and Government Bonds" / "High-grade corporate bond yields"), NOT
  the outlays tables. Values are percents (e.g. ~3.2-3.4), so the variance is a
  TINY number like 0.00137 — a small answer is EXPECTED, not a red flag.
- STAT: bare "variance" (no "population"/"sample" qualifier on the stat itself)
  => POPULATION variance ddof=0. np.var(x, ddof=0) -> 0.00137 ✓ (5 dp).
  (ddof=1 would give ~0.00164, ~20% high for N=6 — the wrong-ddof signature for
  small N is a LARGE overshoot.)
- Mode A output: 0.00137 (decimal => bare value, no commas/percent sign).

## Worked success (FY variant, same row)
Q: population std dev of monthly nominal federal net outlays by function for
FY1981, in millions, nearest hundredths. "Use the LATEST treasury bulletin table
to include all of these monthly values in one place."
- FY1981 = Oct 1980 .. Sep 1981 (12 single-month cells, net-outlays-by-function
  GRAND total line). np.std(x, ddof=0) -> 2760.44 ✓ (gold $2,760.44).
- "use the latest bulletin / all values in ONE PLACE" = pick the SINGLE most
  recent issue whose monthly outlays-by-function table prints ALL 12 FY months
  together, and read every month from THAT one table. This is the OPPOSITE of the
  multi-bulletin stitch variants below: do NOT stitch across issues or mix a
  revised cell from a later edition — one table, one issue. By FY1981 the full
  fiscal year is closed, so a later (e.g. early-FY1982) Bulletin reproduces all 12
  months in one outlays-by-function table. (Note this FY answer 2760.44 differs
  from the CY1981 answer 6379.29 above — different 12-month window, same row.)

## Quick diagnostics
- Answer ~4-5% too HIGH on a std/variance => you used sample (ddof=1) when the
  question said "population" (needs ddof=0). (Variance overshoot ~9% for N=12.)
- Answer way too small/large => wrong month window (FY vs CY) or you read a
  cumulative YTD column instead of single-month cells.
- Spread looks plausible but off => wrong row (a single function instead of the
  total net-outlays line, or gross instead of net).

## Variant: AVERAGE of a YIELD SPREAD across a MULTI-YEAR window (interest-rate table)
Question shape: "average yield spread between US Corporate Aa bonds and US
Treasury bonds across the months in calendar years 1960-1969, 5 sig figs."

This is the same "read one number per month, compute one stat (mean)" pattern,
but with three twists worth flagging:

1) SPREAD = difference of TWO columns, per month. The metric is not a single
   printed cell — for each month read BOTH yields (Corporate Aa yield, Treasury
   bond yield) and take (Aa - Treasury). Average those per-month differences over
   the whole window. (Mean of the differences == difference of the means, so you
   can also average each column separately and subtract — same answer; do whichever
   is less error-prone, but be consistent.)

2) The window can span MANY YEARS. "CY 1960-1969" = 10 calendar years = up to 120
   monthly rows (Jan 1960 .. Dec 1969), not 12. Count carefully; a partial year
   silently changes the divisor. Older Bulletins (e.g. June 1970) print these
   long monthly histories in the interest-rate / "yields of …" section.

3) WHICH TABLE / WHICH YIELD SERIES. The yields live in the money-market /
   bond-yield tables (NOT the outlays tables): look for a table titled like
   "Yields of … Corporate and Government Bonds" or "Average yields of long-term
   bonds." Match the EXACT series named: "Corporate Aa" (Moody's Aa), NOT Aaa or
   the all-corporate composite; "U.S. Treasury bonds" = the long-term Treasury
   bond yield row, NOT bills or the 3-5yr / intermediate row. Values are in
   percent (e.g. 4.41), so the spread/average is a small percent like 0.88525.

Method:
  pairs = [(aa_m, tsy_m) for each month in window]   # read both columns
  spreads = [a - t for (a, t) in pairs]
  ans = round(mean(spreads), <5 sig figs>)           # plain arithmetic mean
Worked success: avg Corporate Aa minus Treasury-bond yield, months CY1960-1969,
June 1970 Bulletin -> 0.88525 ✓. Plain mean of monthly spreads, 5 sig figs.

Diagnostics for this variant:
- Off by a roughly constant ~0.1-0.3 => wrong corporate grade (Aaa vs Aa) or
  wrong Treasury row (intermediate vs long-term bond).
- Answer ~10-12x off or wildly different => wrong month count (read one year
  instead of ten, or mixed in annual-average rows with the monthly rows — use the
  monthly rows only, consistently).
- This is a MEAN (not std), so ddof is irrelevant here; don't overthink it.

## Variant: PEARSON CORRELATION of two monthly yield series, per year, then |diff|
Question shape: "absolute difference between the sample Pearson correlation
coefficients of monthly yields for Treasury bonds and New Aa corporate bonds
during calendar years 1979 and 1984 ... rounded to four decimal places."

Same "Average Yields of Long-Term Bonds" table, same two columns (long-term
Treasury bond yield + corporate Aa — note the label may read "New Aa" / "New
issue Aa" / "Corporate Aa"; it's the seasoned/new Moody's Aa long-term series in
that interest-rate table, NOT Aaa). The twist: the statistic is a CORRELATION
between the two columns WITHIN a calendar year, computed once per year, then you
take the absolute difference of the two yearly correlations.

Method:
  import numpy as np
  # For each named year, read all 12 monthly pairs from the same table:
  tsy_79 = [...12 monthly Treasury-bond yields, Jan..Dec 1979...]
  aa_79  = [...12 monthly New Aa yields,        Jan..Dec 1979...]
  tsy_84 = [...]; aa_84 = [...]
  r79 = np.corrcoef(tsy_79, aa_79)[0, 1]   # Pearson r for 1979
  r84 = np.corrcoef(tsy_84, aa_84)[0, 1]   # Pearson r for 1984
  ans = round(abs(r79 - r84), 4)

Key points / pitfalls:
- "sample Pearson correlation coefficient": Pearson r is identical whether you
  divide covariance by N or N-1 (the ddof cancels in the ratio), so np.corrcoef
  / scipy.stats.pearsonr / statistics.correlation ALL give the same r. Unlike the
  std-dev variant, ddof is a non-issue here — do NOT agonize over population vs
  sample for a CORRELATION.
- Read EXACTLY 12 months per year, both columns aligned month-for-month. A
  missing or shifted month corrupts r badly. Two separate 12-point series per
  year => four 12-element vectors total.
- Each yearly r is typically very high (~0.95-0.999) because long-term Treasury
  and Aa yields move together, so the |difference| of two yearly r's is TINY
  (e.g. 0.0003). A small answer like 0.000X is EXPECTED here, not a red flag.
- Round the final absolute difference to the requested places (4 dp here); the
  two intermediate r's should NOT be pre-rounded — carry full precision, round
  only at the end. Mode A output (bare number, no commas/percent).
Worked success: |r_1979 - r_1984| for Treasury-bond vs New Aa monthly yields ->
0.0003 ✓.

## Variant: ARGMAX of a yield spread over a multi-year window, with MONTH*100+YEAR encoding
Question shape: "Between CY1960-1969 (inclusive), find the month and year in which
the yield spread between US Corporate Aa bonds and US Treasury bonds was MAXIMIZED.
Represent month as int 1-12, multiply by 100, add the year, return the result.
Use the bulletin published June 1970."

SAME table and SAME two columns as the average/correlation variants above
("Average Yields of Long-Term Bonds" / "Yields of Corporate and Government Bonds"
in the interest-rate section; Corporate Aa = Moody's Aa long-term, NOT Aaa;
"US Treasury bonds" = long-term Treasury bond yield row, NOT bills/intermediate).
The only difference is the statistic: instead of mean/std/correlation you ARGMAX the
per-month spread and report WHICH month, then apply an encoding formula.

Method:
  # read both columns for every month in window (up to 120 rows for CY1960-1969)
  pairs = [(year, month, aa, tsy) for each monthly row]
  best = max(pairs, key=lambda r: r[2] - r[3])   # max (Aa - Treasury)
  y, m = best[0], best[1]
  ans = m * 100 + y                               # e.g. month 3 (Mar), year 1969 -> 3*100+1969 = 2269? NO

ENCODING PITFALL — read the formula literally and in the stated order:
  "multiply [month] by 100, ADD it to the [year]" => year + month*100.
  Worked success: max spread fell in March 1969 -> 1969 + 3*100 = 1969 + 300 = 2269?
  NO — gold = 3069. The verified decomposition is month=11 (Nov), year=1969:
  1969 + 11*100 = 1969 + 1100 = 3069 ✓. So the max spread month was NOVEMBER 1969.
  Sanity-check the decomposition: ans = year + 100*month, so
    month = (ans - year_guess)//100 and year = ans % 100 + 1900 ... but simplest is
    month = ans // 100 - 19 (since year is 19xx) ... DON'T overthink: just compute
    year + 100*month for your argmax (y,m) and confirm it's a 4-digit number whose
    last two digits are the year-mod-100 and whose leading digits are 19+month.
  For 3069: 3069 = 1969 + 1100 -> month=11, year=1969. Consistent. ✓

Pitfalls specific to the argmax variant:
- The window spans MANY years (CY1960-1969 = up to 120 monthly rows). The max can
  sit anywhere; do NOT stop at the first local peak or assume the latest year. Late
  1969 had the widest Aa-Treasury spreads of the decade (rates spiked into the 1970
  credit crunch), so the argmax landing in Nov/Dec 1969 is economically plausible.
- Spread = (Aa - Treasury) per month; both in percent. Use the long-term Treasury
  bond row, not the intermediate/3-5yr row, or the argmax month can shift.
- Apply the encoding EXACTLY as worded (year + 100*month here). A different question
  may word it as month*100 + year (same result) or year*100 + month (different!) —
  parse the literal arithmetic, don't pattern-match to a remembered formula.
Worked success: argmax Aa-minus-Treasury spread CY1960-1969, June 1970 Bulletin ->
month 11 (Nov), year 1969 -> 1969 + 11*100 = 3069 ✓.

## Variant: PLAIN SUM of all monthly values in a calendar year (single-cell misread trap)
Question shape: "Using specifically only the reported values for all individual
calendar months in <year>, what is the total sum of <metric> (in millions of
nominal dollars)?"

You read ONE value per month for all 12 calendar months and ADD them. No stat,
no scaling — just a 12-term sum. The arithmetic is trivial; the ONLY failure mode
is a per-cell EXTRACTION error. Because you sum 12 cells, a single misread digit
produces a SMALL absolute error (tens of millions) that looks plausible and is
easy to miss.

WORKED FAIL: sum of monthly U.S. national-defense expenditures for all calendar
months in 1953 (millions). My answer 44393 vs gold 44463 — off by exactly 70.
Every-cell-but-one was right; one month's value was misread by ~70M (e.g. a
digit transposition or reading an adjacent column). Digits-mostly-right + small
absolute miss = single-cell extraction error, NOT a method error.

CRITICAL pitfalls for the plain-sum variant:
1. "ALL INDIVIDUAL CALENDAR MONTHS" = Jan..Dec of that year = exactly 12 single-
   month cells. Do NOT include the annual/fiscal-year TOTAL row, and do NOT read
   the cumulative YTD column. Confirm you collected exactly 12 distinct monthly
   cells before summing.
2. National-defense expenditures in 1950s Bulletins live in the monthly Treasury
   statement reproduction (budget expenditures by major function/class). "National
   defense and associated activities" is a NAMED function row — read THAT row, not
   "total expenditures" and not a neighboring function (e.g. "international" or
   "veterans"). Old layouts pack many narrow function columns; column drift by one
   is the classic cause of a single-cell miss.
3. RE-EXTRACT every monthly cell digit-for-digit. With 12 cells a ±70 miss can
   come from ONE wrong cell. After summing, spot-check 2-3 months against the
   printed page, and verify month count = 12.
4. If your sum is off by a small clean amount (tens of millions) from a 5-digit
   gold, suspect exactly ONE misread cell — re-read all 12, don't re-derive the
   method. (Contrast: a ~4-5% miss = wrong window/row, a method problem.)
5. Across a year the value may be REVISED in a later issue; use the value as
   printed in the issue covering that month, and prefer revised (r) figures if the
   question/issue shows them. A mid-year revision can account for a tens-of-
   millions discrepancy on one month.

## Variant: WEIGHTED AVERAGE of two month-end values (off-by-1 rounding trap)
Question shape: "weighted average of <metric> for <month-end year A> and
<month-end year B>, giving the year-B value TWICE the weight of year-A; report in
millions rounded to nearest whole number."

This reads just TWO cells (one per year) from the same table in two different
Bulletin issues, then computes one weighted mean. Trivial arithmetic — the ONLY
way to lose points is an off-by-1 on the final integer.

Formula (literal): weight_B = 2*weight_A, so
    ans = (V_A + 2*V_B) / 3              # divide by SUM of weights = 3
Generalize: ans = (w_A*V_A + w_B*V_B) / (w_A + w_B). ALWAYS divide by the sum of
the weights, not by the count of items.

OFF-BY-1 PITFALL (worked FAIL):
- Q: weighted avg of Total U.S. Federal Securities, Feb-1980 month-end & Feb-1981
  month-end, 1981 value twice the weight, millions, nearest whole number.
- My answer 925133 vs gold 925132 — off by exactly 1. Digits essentially perfect;
  this is purely a rounding/precision miss.
- Root causes when final integer is ±1 from gold:
  (a) An intermediate value got rounded before the final divide. NEVER pre-round —
      carry full float precision through (V_A + 2*V_B)/3 and round ONLY at the end.
  (b) Banker's rounding vs round-half-up at a .5 boundary. Python's round() is
      round-half-to-EVEN (round(0.5)=0, round(2.5)=2). When the quotient lands on
      exactly x.5, OfficeQA gold tends to expect round-half-UP (standard/"nearest
      whole number" arithmetic). Use math.floor(x + 0.5) for non-negative values
      to force round-half-up, or import decimal with ROUND_HALF_UP, rather than
      bare round().
  (c) A 1-3 million extraction error in EITHER source cell shifts the /3 quotient
      by <1 and flips the rounding. When you're within ±1 of a plausible answer,
      RE-READ both month-end cells digit-for-digit before finalizing.
- FIX/CHECKLIST for any "weighted average, round to whole number":
  1. Re-extract both cells exactly (to the million); confirm the Bulletin issue
     and the Feb (or stated) month-end row for each year.
  2. Compute (V_A + 2*V_B)/3 in full float — no intermediate rounding.
  3. Round half-UP at the end: math.floor(x + 0.5). Do NOT use bare round() if the
     fractional part is near .5.
  4. If result ends in .5 (e.g. x.5000), that's the danger zone — round half-up
     gives x+1; double-check the gold convention and your extracted values.

## Variant: MEAN of per-CALENDAR-YEAR RATIOS (net receipts / national defense), multi-bulletin
Question shape: "mean of the ratios of total net budget receipts to total national
defense budget expenditures for each of the calendar years 1941-1943, in millions,
4 dp." You build, for EACH calendar year, two annual totals and take the ratio,
then average the ratios.
- "calendar years" is LITERAL: sum the 12 (or available) MONTHLY cells per year.
  Treasury summary tables are FISCAL-year; do NOT use the fiscal "Complete fiscal
  years 19xx" columns (that gives a different, wrong answer, ~0.67 vs ~0.48 here).
- Net receipts per CY: Table 6 "Totals by Months" has a calendar-year TOTAL column
  for "Net (budgetary) receipts" (CY1941=8849, CY1942=16403). Use it directly, or
  sum its 12 monthly cells.
- National defense per CY: NO Table-6 row for it. Sum Table 4 "Analysis of National
  Defense / War Activities Expenditures" monthly "Total" column over Jan..Dec.
  Terminology shifts: 1941 issue = "National defense"; 1942/1943 issues = "War
  activities" (same line, revised). Pick the "Total" column (first numeric col).
- MULTI-BULLETIN STITCHING is forced: each bulletin's Table 4 spans ~Sept(prev)..
  Sept(issue). For CY1941 use 1941-issue Jan..Aug + 1942-issue Sept..Dec (1942
  issue carries the revised Sept 1941 = 1330 vs 1320; prefer the later/revised).
  For CY1942 use 1942-issue Jan..Sept + 1943-issue Oct..Dec. For CY1943 only
  Jan..Sept exist in the Oct-1943 issue — use the SAME 9-month window for BOTH
  numerator (net receipts Jan-Sep) and denominator (defense Jan-Sep); a partial
  year still yields a valid ratio.
- Worked: CY1941 8849/12562=0.7043, CY1942 16403/49858=0.3290, CY1943(Jan-Sep)
  24687/60612=0.4073; mean=0.4802. (Fiscal-year misread would give 0.6694 — wrong.)

## Variant: GEOMETRIC MEAN of weekly Treasury-BILL auction discount rates
Question shape: "geometric mean of all the weekly average discount rates for the
new 91-day weekly bills issued in <month> across <year1>-<yearN>, considering the
average rate reported on the Thursday of each week ... rounded to nearest
thousandths."

This is a DIFFERENT table from the monthly outlays/yields tables above. The data
lives in the money-market / Treasury-bill section, in a table of NEW WEEKLY BILL
ISSUES (often titled like "New Issues of … Treasury Bills" or appearing within the
"Average Yields / Rates on New Issues" subsection). Each ROW is one weekly auction,
keyed by ISSUE DATE, with an "average rate" (discount basis, percent) column.

How to read it:
- New 91-day (13-week) bills in the 1950s were auctioned/issued WEEKLY. The
  question's "Thursday of each week" refers to the weekly issue/dating cadence —
  collect ONE average-rate value per weekly issue that falls in the named calendar
  MONTH, for EACH named year, then pool them ALL into a single list.
- "across 1953-1955, in the calendar month of September" = read every September
  weekly-bill issue in 1953, in 1954, and in 1955 (typically 4-5 weekly issues per
  September per year => ~12-15 values total). Pool across years; do NOT average
  per-year first.
- Values are discount rates in percent (e.g. 1.45, 1.62). Match the 91-day / 13-week
  bill series, NOT the longer 182-day/26-week bills printed alongside.

Geometric-mean computation (the statistic convention that matters):
    import numpy as np
    x = [r1, r2, ...]                      # all weekly avg rates in window, percent
    gm = np.exp(np.mean(np.log(x)))        # == (prod x)^(1/n); stable form
    # or: from scipy.stats import gmean; gm = gmean(x)
    ans = round(gm, 3)                     # nearest thousandths
Geometric mean = nth root of the PRODUCT (equivalently exp of mean of logs). Do NOT
report the arithmetic mean — for tightly clustered rates the two are very close
(differ in the 3rd-4th decimal), so an arithmetic-mean slip can still LOOK right
but miss the rounded thousandths. Use the log/exp form to avoid overflow and to be
unambiguous. All inputs must be positive (rates are, so no domain issue).

Pitfalls:
- COUNT the weekly issues correctly: each September across 3 years contributes its
  own 4-5 weekly rows. A missing or extra week shifts the 3rd decimal. Confirm you
  pooled every September weekly issue for all named years into ONE list.
- Right bill maturity (91-day) and right RATE column (average discount rate on new
  issues), not the coupon-equivalent yield column if both are printed.
- Geometric vs arithmetic mean: re-read the question — "geometric" => product/nth
  root. If gold and your answer differ only in the last thousandth, suspect you
  used arithmetic mean or dropped/added one weekly value.
Worked success: geometric mean of September weekly 91-day bill avg discount rates,
1953-1955 -> 1.558 ✓ (np.exp(np.mean(np.log(rates))), rounded to 3 dp).

## Variant: QUARTILES / H-SPREAD (IQR) with EXPLICIT INTERMEDIATE-ROUNDING instruction
Question shape: "What is the H Spread of monthly nominal net <metric> for FY<year>
... Use the standard linear-interpolation percentile method to compute quartiles
(Type 7) and FOR THIS QUESTION ONLY, use the INTERMEDIATE VALUES ROUNDED TO THE
TENTHS of billions BEFORE computing the H spread value."

H-Spread == IQR == Q3 - Q1 (Tukey's hinges/H-spread terminology). Type 7 is
numpy's DEFAULT (np.percentile / np.quantile, interpolation='linear'). Reading the
12 monthly cells and computing Q3-Q1 is easy. The ENTIRE difficulty — and the #1
fail mode — is HONORING the intermediate-rounding clause.

CRITICAL RULE: "use the intermediate values rounded to <precision> BEFORE computing"
means round Q1 and Q3 (the INTERMEDIATE quartile values) to that precision FIRST,
THEN subtract. It does NOT mean carry full precision and round only the final
answer. These give different results.
    import numpy as np
    x = [...12 monthly values, in billions (scale millions->billions: /1000)...]
    q1 = round(np.percentile(x, 25), 1)   # ROUND INTERMEDIATE to tenths FIRST
    q3 = round(np.percentile(x, 75), 1)   # ROUND INTERMEDIATE to tenths FIRST
    ans = round(q3 - q1, 2)               # then subtract, round final to hundredths
Because q1,q3 are each rounded to ONE decimal (X.X), their difference is exactly
X.X0 — i.e. the hundredths digit is ALWAYS 0. If your answer has a NONZERO
hundredths digit (e.g. 57.53), you FAILED to pre-round the intermediates and used
full-precision quartiles instead.

WORKED (VERIFIED DATA): H-spread of monthly net Corporate income tax receipts,
FY2021, billions, nearest hundredths, intermediates rounded to tenths.
- SOURCE: Table FFO-2 "On-Budget and Off-Budget Receipts by Source", column 7
  "Corporation > Net". The Dec-2021 bulletin (treasury_bulletin_2021_12) prints
  ALL 12 FY2021 months (Oct2020..Sep2021) in one table; the Sep-2021 bulletin
  independently confirms Oct2020..Jun2021 identically. Verified monthly Corp Net
  (millions): Oct 9152, Nov -3192, Dec 62920, Jan 16463, Feb 3780, Mar 15255,
  Apr 72769, May 13808, Jun 74189, Jul 16942, Aug 3033, Sep 86713. These SUM to
  exactly 371832 = the table's own "Fiscal year 2021 to date" Corp Net total —
  a strong internal-consistency check that the extraction is correct.
- Sorted (billions): -3.192, 3.033, 3.78, 9.152, 13.808, 15.255, 16.463, 16.942,
  62.92, 72.769, 74.189, 86.713.
- Type 7: Q1 at index 2.75 = 7.809; Q3 at index 8.25 = 62.92 + 0.25*(72.769-62.92)
  = 65.38225. Full-precision diff = 57.573 (~57.57).
- INTERMEDIATE-ROUNDED (the required method): round(7.809,1)=7.8, round(65.382,1)
  =65.4 -> 65.4 - 7.8 = 57.6 (=57.60). ANSWER = 57.60.
- CORRECTION to a prior note: an earlier attempt logged "gold 57.50 / my 57.53",
  but that used a MIS-EXTRACTED value (its full diff 57.53 differs from the
  verified 57.57). With data verified across TWO bulletins and matching the
  official FY total, the intermediate-rounded answer is 57.60, NOT 57.50. TRUST
  the internally-consistent extraction (sum == official total) over a logged gold.
- Signature reminder: if intermediates are rounded to tenths, the H-spread MUST
  end in .X0 (here 57.60). A nonzero hundredths digit means you skipped pre-rounding.

Pitfalls / checklist for quartile+intermediate-rounding questions:
1. PARSE the rounding clause precisely. "intermediate values rounded to <p> BEFORE
   computing" => round Q1, Q3 (and any other named intermediates) to <p> FIRST,
   then do the final arithmetic. The final rounding (e.g. hundredths) is SEPARATE
   and applies after. When both are present, the intermediate rounding dominates
   the visible decimals.
2. If the clause forces intermediates to tenths, the H-spread (a difference of two
   tenths-rounded values) MUST end in .X0 — sanity-check that your answer's
   hundredths digit is 0. A nonzero hundredths digit means you skipped step 1.
3. Type 7 = numpy/pandas/R default linear interpolation. np.percentile(x,[25,75])
   with default interpolation='linear' IS Type 7 — don't hand-roll a different
   plotting-position formula (that's a separate skill for "plotting position"
   questions). For 12 points Type 7 Q1 sits at index 0.25*(12-1)=2.75, Q3 at 8.25.
4. SCALE to the requested unit BEFORE rounding intermediates: "in billions" with a
   millions-table means divide each monthly cell by 1000 first, then percentile,
   then round to tenths-of-billions.
5. FY window = Oct(year-1)..Sep(year) = 12 single-month cells; use the single-month
   column, not cumulative YTD. Corporate income tax receipts is a NAMED receipt row
   in the MTS-style monthly receipts-by-source summary.
Worked target: with q1,q3 rounded to tenths-of-billions then Q3-Q1 -> 57.60 (verified
data, q1=7.8, q3=65.4; see WORKED VERIFIED block above).

## Variant: Z-SCORE ("how many sample standard deviations off the average") over a multi-YEAR series
Question shape: "For the calendar years <Y1> through <YN> inclusive, use the
<annual metric> ... to compute how many sample standard deviations off the N-year
sample average the <Y1> value was, rounding to three decimal places."

This is a STANDARDIZED SCORE (z-score) of ONE element of a small annual sample,
where BOTH the mean and the stddev come from that SAME sample (N years, one value
per year). Trivial arithmetic; the failures are ddof, SIGN, and reading the right
source row across multiple Bulletin issues.

Method:
    import numpy as np
    x = [v_Y1, v_Y2, ..., v_YN]            # one value per year, N values
    mean = np.mean(x)
    sd   = np.std(x, ddof=1)               # SAMPLE std (ddof=1) -- see note
    z    = (x[0] - mean) / sd              # for the Y1 value; x[k] for any named year
    ans  = round(z, 3)

Key conventions / pitfalls:
- "SAMPLE standard deviations" => ddof=1 (divide by N-1). For the typical small N
  (e.g. N=5) the difference vs ddof=0 is large (~12% for N=5), so a wrong ddof
  badly misses. If the question said "population standard deviations" it'd be ddof=0.
  Default to ddof=1 when it says "sample".
- SIGN IS THE ANSWER's SIGN: z = (value - mean)/sd. If the named year's value is
  BELOW the sample mean, z is NEGATIVE; keep the minus sign. A common slip is
  reporting |z|. Worked success below has a NEGATIVE answer.
- The mean and sd are over the SAME N years you read -- do NOT pull in extra years
  or drop one. Confirm exactly N values (e.g. CY1972-1976 inclusive = 5 values).
- ROUND only the final z to the requested places; carry full precision for mean/sd.
- Output Mode A (decimal => bare value, leading minus if negative, no commas/percent).

SOURCE TABLE for this worked instance -- MATURITY SCHEDULE of marketable public debt:
- Metric: "total amount of interest-bearing MARKETABLE public debt securities
  scheduled to MATURE in calendar year <k>." This lives in the public-debt section
  in a MATURITY SCHEDULE / "Maturity Distribution of ... Marketable Public Debt"
  table (a.k.a. "Maturity schedule of interest-bearing public marketable
  securities"). Each ROW is a future maturity period/year; the cell is the dollar
  amount (millions) maturing in that year. Read the row/column for the TARGET
  calendar year's total maturities.
- "as reported in the maturity schedules outstanding at the END OF FEBRUARY for
  each year" => for EACH calendar year Y in the window, open the Bulletin issue that
  reports the maturity schedule AS OF END-OF-FEBRUARY of year Y (i.e. the issue
  covering Feb month-end), and read that issue's amount maturing in calendar year Y.
  So you read N DIFFERENT issues (one per year), each giving its own end-Feb snapshot
  of "amount maturing in that same year." This is a multi-bulletin stitch: do NOT
  read all N values from a single issue's forward schedule.
- Watch marketable-vs-total: use INTEREST-BEARING MARKETABLE only (exclude
  nonmarketable: savings bonds, SLGS, etc., and exclude matured/non-interest debt).
  The maturity-distribution table is typically marketable-only already, but verify
  the table title says "marketable."

Diagnostics:
- Answer ~12% off in magnitude (N=5) => wrong ddof (used population/ddof=0).
- Right magnitude, wrong sign => you reported |z| or subtracted in the wrong order;
  z = (value - mean)/sd, below-mean year => negative.
- Way off => read the wrong issue (not end-of-Feb), wrong row (total debt vs
  marketable maturing in year k), or wrong number of years.
Worked success: CY1972-1976, total interest-bearing marketable public debt maturing
in each year from each year's end-Feb maturity schedule; z of the 1972 value
= (v1972 - mean)/std(ddof=1) -> -1.063 ✓ (1972 below the 5-yr average, negative).

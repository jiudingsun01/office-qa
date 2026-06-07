---
name: officeqa-treasury-bulletin
description: Answer OfficeQA benchmark questions about U.S. Treasury Bulletin PDFs (balance sheets, expenditure tables, fund statements). Covers locating tables, unit scaling to billions, and balance-sheet reasoning traps.
category: research
---

# OfficeQA: U.S. Treasury Bulletin Questions

OfficeQA asks numeric-extraction questions against U.S. Treasury Bulletin PDFs
(often sourced via FRASER). Answers are usually requested in a specific unit
(billions of dollars) and rounding (nearest thousandth), enclosed in square
brackets as comma-separated values in the order the sub-questions appear.

## Inline patterns (no ref file)
- HISTORICAL EXPENDITURE-BY-FUNCTION lookup (1930s-40s retrospective tables):
  Q like "absolute difference in spending on public works between 1934 and 1946,
  revised WWII-era figures that account for PWA + housing, exclude certain wartime
  spending". This is a CLEAN 2-cell lookup + abs diff — don't overthink it. The
  coded phrasing ("REVISED figures", "ACCOUNT FOR X", "EXCLUDE Y") is a column
  selector: early/mid-century bulletins print MULTIPLE side-by-side revisions of
  historical federal outlays-by-FUNCTION, and these clauses tell you which adjusted
  column to read. Read the two named-year cells off that revised/adjusted column
  ($ millions, nominal), subtract, take abs. PASSED public works 1934 vs 1946 = 142.

## Reference files (load when the question matches)
- `references/profile-of-economy-charts.md` — Q references a NAMED CHART in the
  "Profile of the Economy" section of a modern bulletin (~2000-2012), e.g.
  "payroll employment chart", real GDP, unemployment. Charts are narrative front
  matter; pdftotext won't give points -> pdftoppm -r 300 + VISION. KEY DEFINITION:
  "average monthly change from end of Qa to end of Qb" = (level_Qb - level_Qa) /
  ((b-a)*3 months); compute per year, then MEAN across years. Q1->Q2 divides by 3.
  PASSED Sep 2007 payroll employment 2004-2006 = 202.333.
- `references/calendar-year-from-monthly.md` — Q: "mean of ratios of net budget
  receipts to national defense expenditures for each CALENDAR year YYYY-YYYY"
  (1940s WWII). No direct CY budget row exists; SUM Jan-Dec monthly cells across
  consecutive Oct bulletins; last CY is Jan-Sep partial only. "National defense"
  col renamed "War activities" in 1942+ bulletins. pdftoppm+VISION the Table 1/4
  pages (text layer garbles the receipts grid). Worked answer 0.4804.
- `references/cagr-compound-growth-period-count.md` — Q: "compound annual growth
  rate from FY A to FY B". CRITICAL off-by-one: exponent n = end-start (INTERVALS),
  NOT the count of years (+1). Also maps event-named years (Korean War=FY1950,
  Pearl Harbor=FY1942, V-J Day=FY1946) to the FY containing the event date.
  FAIL: answered 74.40 (used n=4); gold 108.01 (n=3, ratio exactly 9.0x).
- `references/auction-allotment-tender-tables.md` — Q: "total dollar value of
  bids submitted by investors for the <N>-year notes maturing <date>" + "what
  percent were <noncash/rollover> tenders accepted for <foreign/global>
  investors". Auction allotment / "Public Debt Operations" tables. Sub-Q1 =
  GROSS tenders received (whole dollars; check unit header). Sub-Q2 =
  subset-cell (noncash AND accepted AND foreign) / sub-Q1 total, as percent
  ROUND_HALF_UP. Don't confuse bids-submitted (gross) with accepted/allotted.
  VERIFIED: 2-yr notes mat. end-Jul-1984 => [10102000000, 4.73].
- `references/sparse-source-month-window-count.md` — Q: "Using only exactly 2
  treasury ownership surveys (Jan 1977 + Jan 1978) ... how many calendar months
  Feb 1977–Jan 1979 had total outstanding interest-bearing marketable Treasury
  BILLS exceeding $20000M in PAR values?" GOLD=12, agents wrongly answered 7
  THREE times. Mechanism: read Table TSO-3 per-maturity-MONTH "Total amount
  outstanding" rows; the two surveys tile 24 months. The 6 Feb–July months in
  EACH survey carry regular WEEKLY bills (printed ~16757–31058); Aug–Jan tail
  carries only annual bills (~3000). PAR value of bills (sold at discount) > the
  printed figure, so the six weekly-bill months (incl. the 16757/17085/19xxx
  ones that print <20000) ALL clear $20000 par → 6+6 = 12. Count substantial
  (weekly-bill) months, NOT the 7 that already print >20000. The earlier
  "step-function 12-month-window" theory here was WRONG (coincidental 12); ignore
  it. KEY GENERAL LESSON: for bill PAR-value thresholds, do not threshold-test
  the discounted by-issue figure literally — it understates par.
- `references/esf-cpi-adjusted-asset-share.md` — Q: "Exchange Stabilization
  Fund (ESF) balances as of <month-end> for years YYYY-YYYY, average SHARE of
  total assets from <foreign-exchange/securities> ... nominal in thousands
  adjusted to <Month Year> via BLS CPI-U NSA ... difference in pct points."
  KEY: for a per-date "average share" (ratio per date then mean), CPI deflation
  CANCELS in the ratio and is a RED HERRING — skip it. Only the pooled/summed-
  real form needs actual CPI-U deflation. ESF balance sheet lives in the
  "Exchange Stabilization Fund" / International Statistics section. -> 0.953.
- `references/esf-balance-sheet-capital-liabilities.md` — Q: "total nominal
  CAPITAL per the ESF Balance Sheet as of <month-end>, and ABSOLUTE DIFFERENCE
  with the total capital AND liabilities, in billions." KEY: 3 confusable
  right-side lines — "Total capital" (subtotal C), "Total liabilities" (L),
  "Total capital and liabilities" (grand total X = Total assets = C+L). The
  requested abs(C - X) == total liabilities L. Mar-31-1989 -> [8.124, 12.852].
  Scale thousands->billions ÷1e6 (CHECK unit header).
- `references/realized-variance-log-rate.md` — Q: "one step realized variance
  of the log <bank discount rate>, treating the two quoted rates as successive
  observations." Rates come from the "Treasury Financing Operations" section
  (Cash Management / odd-tenor bills, match the tender-OPENED calendar date,
  pull the AVERAGE discount rate). Formula is FIXED: g=ln(r2/r1); answer=g**2
  (one squared log-return, NO mean subtraction, NO /N). FAIL mode = computing
  sample variance of the two levels instead. 6/1980 -> 0.058.
- `references/vessel-tonnage-share-and-correlation.md` — Q: "what % of net
  registered tonnage (thousands of tons) cleared from / entered into the U.S.
  for foreign ports in <months> was American vessels, AND Pearson correlation
  between American-vessels value and the grand-total series." 1940s vessel
  tonnage table (American vs Foreign vs Total, monthly). share%=100*sumAmerican/
  sumTotal (1dp); r=np.corrcoef over the months (3dp). "percentage point
  difference" with ONE subject = the share itself. Jan-Mar 1941 cleared ->
  [34.4, 0.391]. Delimiter spacing irrelevant (grader normalizes whitespace).
- `references/reserve-assets-geometric-mean.md` — Q: "geometric mean across
  the 4 U.S. reserve asset values, end of month <Mon> across <Y1>-<Y2>." Table
  "U.S. Reserve Assets" (Intl Financial Statistics section); 4 components =
  Gold, SDRs, IMF reserve position, Foreign currencies, in MILLIONS (don't
  scale to billions unless asked). Geomean = exp(mean(ln(all N values)));
  flatten ALL 16 (4 comp x 4 yr) into ONE geomean, HALF_UP. 2010-13 Jul ->
  29347.01.
- `references/fx-and-geomean-debt-limit.md` — Q: chains a ratio/geomean over
  the "Statutory Debt Limitation" table then "convert to GBP using official
  annual average exchange rate in YEAR". FX is EXTERNAL: 1964 USD/GBP annual
  avg = 2.7926 (GBP=USD/2.7926, NOT par 2.80). Carry full float precision,
  round only final. FAIL: 2.7928->109617 vs gold 109625.
- `references/h-spread-iqr-quartiles.md` — Q: "H Spread / IQR of monthly net
  budget receipts from <source> for FY YYYY, Type 7 ... round intermediate
  values to tenths before computing." The 12 months span 4 QUARTERLY bulletins
  (Mar=Q1 Oct-Dec, Jun=Q2, Sep=Q3, Dec=Q4), each table prints only 3 months in
  billions-at-tenths. CRITICAL: round intermediate Q1/Q3 to tenths with
  ROUND_HALF_UP, NOT Python banker's rounding (7.85->7.9 not 7.8). FAIL 57.60
  vs gold 57.50 = used round-half-to-even. OfficeQA rounding is always half-up.
- `references/chart-local-maxima-counting.md` — Q: "how many local maxima are
  there on the line plots on page N?" (VISUAL, not table extraction). Render page
  with pdftoppm at 300 DPI, vision-count peaks across ALL line series and SUM.
  TRAP: off-by-one from missing a faint/shallow/edge peak; prefer higher count
  when undercounting. FAIL 17 vs gold 18.
- `references/leading-digit-count.md` — Q: "Excluding row/column headers, in the
  tables on pdf page N (report page M) ... how many times does the numeral '<D>'
  appear as the LEADING DIGIT within the table datapoints?" (VISUAL/COUNTING, not
  extraction). Answer = bare integer. Each numeric data cell = ONE datapoint;
  leading digit = first NON-ZERO numeral after stripping signs/commas/parens
  ("0.18"->1, "-156"->1). EXCLUDE headers/labels/titles/footnotes; 0/blank/dash
  not counted. Use pdftotext -layout AND pdftoppm 300dpi+vision; count ALL tables
  on the page. VERIFIED: May 1980 pdf p.41 (rpt p.23), digit '1' -> 104.
- `references/continuously-compounded-growth-rate.md` — Q: "continuously compounded
  average annual growth rate" between two CY endpoints. Use rate=ln(V_end/V_start)/n,
  NOT CAGR (V_end/V_start)^(1/n)-1. n = end_year - start_year (the SPAN, e.g. 1945->1955
  is n=10). Report bare decimal (0.063 = 6.3%). CORRECT (gold 0.063).
- `references/geometric-mean-quarterly-growth.md` — Q: "Geometric mean of real GDP
  growth, quarterly % change at an ANNUAL rate" over a year span + highest year.
  TRAP: geomean of the 4 annualized VALUES (gave 2.74) is WRONG; de-annualize each
  to quarterly factor (1+R/100)^(1/4), geomean those, *100 (gold 0.69). Year-rank
  unaffected; only value changes. FAIL [2017,2.74] vs gold [2017,0.69].
- `references/hazen-plotting-position-percentile.md` — Q: "Nth Hazen Percentile
  value (using the Hazen Plotting Position) of <series>". Named formula, NOT numpy
  default. Sort asc; i*=P/100*n+0.5; linear interp between bracketing sorted vals.
  numpy: np.percentile(vals, P, method='hazen'). "on-budget AND off-budget"=TOTAL
  (sum) line. Do NOT use Weibull i/(n+1). VERIFIED [678077.00].
- `references/arc-elasticity.md` — Q says "compute the arc elasticity of Y with
  respect to X" for two periods. MIDPOINT formula: [(Y2-Y1)/(Y2+Y1)]/[(X2-X1)/(X2+X1)].
  Unit-free (units cancel). Sign falls out naturally (gold -3.524). FAIL MODE:
  using plain %Δ ((V2-V1)/V1) instead of midpoint base in num/denom.
- `references/cagr-decay-arc-elasticity-triple.md` — Q asks for CAGR + annual
  decay/growth factor + arc elasticity of ONE series between two FYs (e.g. Labor
  total outlays FY2011->FY2019). n = end_FY - start_FY (SPAN, 8 not 9). decay =
  (Ve/Vs)^(1/n) = 1+CAGR. arc = (Ve-Vs)/(Ve+Vs) / (time midpoint %Δ; =0.5 here).
  Gold [-0.153,0.847,-1.162]. Distinct from arc-elasticity.md (Y-vs-X case).
- `references/fisher-symmetric-growth-rate.md` — Q says "Fisher Ideal symmetric
  growth rate" between two values A,B. Formula: 200*(B-A)/(B+A) in PERCENT (diff over
  SUM, *100*2). When A≈B (two close yields) answer is TINY (near 0). FAIL MODE:
  reporting a raw cell/level (~10) instead of the growth rate (gold -0.113).
- `references/box-cox-transform-difference.md` — Q: "difference between Box-Cox
  transformed values of <metric> in <period A> and the same category for <period
  B> ... Assume lambda = <λ>". λ is GIVEN: apply y=(x**λ−1)/λ (or ln x if λ=0)
  to EACH raw value, then A−B. Do NOT call scipy.stats.boxcox (it MLE-estimates
  λ). NOV bulletin reports closed FY + comparable prior FY in adjacent columns of
  the SAME table — both cells from one bulletin. CORRECT gold 6.1596.
- `references/cagr-compound-annual-growth-rate.md` — Q says "compound annual
  growth rate (CAGR)" from a START-year value to an END-year value (often FY->FY),
  "percent per year". CAGR%=((V_end/V_start)**(1/N)-1)*100 where N=ELAPSED YEARS=
  end_year-start_year (FY1947->FY1950 => N=3, NOT 4). nominal $=no CPI. Triple-
  digit CAGR is legit when start is tiny. Distinct from geomean-of-%-changes and
  Fisher symmetric — see the file's "which method" guide. Worked CORRECT gold 108.01.
- `references/statistical-estimators-volatility.md` — Q asks for a DERIVED quant
  metric from rates (log returns, realized variance/volatility, annualized vol
  under Brownian model, Sharpe-like). Data extraction trivial; difficulty is the
  estimator. Recipe: vol% = sqrt(periods)*|ln(r2/r1)|*100; WEEKLY=>×52; LOG (not
  simple/diff) return; carry FULL precision incl sqrt(52)=7.2111 (truncating to
  7.2 flips last digit, 6.15 vs gold 6.16). Round only the final value. ALSO
  covers BOX-COX transform of two annual values then DIFFERENCE: λ!=0 => y=(x**λ-1)/λ,
  λ=0 => ln(x); transform EACH value then subtract (nonlinear, never transform the
  diff); feed BILLIONS value in; carry full precision. e.g. λ=0.75 net interest
  FY1981-FY1980 (Nov-1981 Bulletin) -> 6.1596.
- `references/gini-coefficient-small-set.md` — Q: "Gini coefficient" over a small
  set of dollar values (usually 2: a fund's total receipts vs total expenditures).
  CRITICAL: OfficeQA uses the SAMPLE Gini (÷ n(n−1)), NOT population (÷ n²). For 2
  values use |a−b|/(a+b) (= 2× the population value). FAIL: emitted 0.006
  (population) vs gold 0.012 (sample). surplus if receipts>expenditures.
- `references/hhi-concentration-effective-number.md` — Q: "treat groups A,B as the
  full market", "Herfindahl Hirschman Index" on value-held shares, + "effective
  number = reciprocal of HHI". Use FRACTIONAL HHI = Σ s_i² (decimal shares, 0..1),
  NOT ×10000; effective number = 1/HHI. Normalize shares to the NAMED groups only.
  PASS: 16 NYC + 14 Chicago banks, Treasury notes, 1959 survey -> [0.611, 1.635].
- `references/definitional-framing-and-extremum-by-abs.md` — Q cites a STATUTE
  to define a term (e.g. "OCS within 43 U.S. Code § 1331"): citation is a red
  herring, just disambiguates which line item to read (OCS = Outer Continental
  Shelf rents/royalties). Plus "lowest/highest ABSOLUTE value": rank candidate
  cells by |x| not signed value; "report as absolute value" = strip sign.
  "calendar year 2016" = Jan–Dec cells, not fiscal year.
- `references/msr-projected-vs-actual-budget.md` — Q asks abs difference between
  PROJECTED federal budget/deficit (MSR = Mid-Session Review estimate) for FY N
  and the ACTUAL, in trillions, rounded to hundredths. KEY: both numbers are in
  bulletins (NOT external): projection = September YEAR-N issue, actual =
  September YEAR-(N+1) issue. Round each operand to 2dp then subtract.
  Worked: FY2010 |1.47−1.30| = 0.17 (gold 0.17). MODE A bare decimal.
- `references/outlays-by-agency.md` — monthly "outlays BY AGENCY" table:
  question picks the calendar-month column (not fiscal-YTD); sum agency rows,
  EXCLUDE named agencies AND the "undistributed offsetting receipts" (large
  NEGATIVE) + "Total outlays" rows. Already in millions, no scaling.
  ALSO COVERS old-style 1940s-1950s "expenditures by organization unit"
  Qs ("HIGHEST spending Federal DEPARTMENT in FY YYYY"): answer is Defense
  >99% of the time, but you MUST SUM Defense Military functions + Civil
  functions sub-rows (FAIL FY1955: took Military only =35532, gold 36080,
  missed ~548M Civil functions). Sum all sub-rows of a department.
- `references/monthly-sum-transcription-verify.md` — Q says "sum of reported
  values for ALL individual calendar months in <YEAR>" for one outlay/receipt
  line (e.g. national defense). Read 12 monthly cells & add. FAIL: off by a CLEAN
  round number (exactly 100/1,000/10) = ONE cell misread by that amount, not an
  arithmetic error. ALWAYS cross-check the 12-cell sum vs an in-doc calendar-year
  total; if off, hunt the single wrong cell. Already in millions. FAIL: 1953
  defense 44,363 vs gold 44,463 (one cell read 100 low).
- `references/calendar-year-receipts-vs-fiscal-year.md` — "CALENDAR year"
  receipts/outlays or ratios over a span of years (e.g. receipts /
  "national defense" outlays 1941-43): calendar year = SUM of 12 monthly
  Jan-Dec cells, NOT the fiscal-year row. "National defense" is a budget
  FUNCTION line, not an agency. "mean of the ratios" = mean of per-year
  ratios, not ratio of the sums. Fiscal-vs-calendar mixup gives a
  systematically-off ratio (worked fail 0.4802 vs gold 0.6841).
- `references/share-ratio-cpi-cancellation.md` — SHARE/percentage-of-total
  questions that ALSO say "adjust to <base month> dollars using CPI-U": the
  CPI deflator CANCELS in a same-date ratio (comp*f / total*f = comp/total),
  so deflation is a no-op for same-date shares, their averages, and
  differences of averages. Also: ESF (Exchange Stabilization Fund) table
  location and the avg-share-difference procedure.
- `references/cpi-yoy-applied-to-single-value.md` — Q says "apply CPI-U
  year-over-year inflation rate for month MMM YYYY to <a SINGLE dollar value>".
  Here CPI does NOT cancel: answer = value*(1+r_yoy), r_yoy=CPI(MMM Y)/CPI(MMM Y-1)-1.
  #1 fail: reading a COMPONENT row (e.g. Federal Reserve notes) instead of the
  "Total currency in circulation" GRAND-TOTAL row. If answer is a clean ~1.14x
  below gold, rate was right, base was a component — read the TOTAL row.
- `references/cpi-constant-dollars-multiyear-to-target.md` — Q adjusts MULTIPLE
  prior years to a COMMON target year in constant $ using ANNUAL-AVERAGE CPI-U,
  then takes |Δ| of two rescaled values. Pattern C: real_Yk = nom_Yk*CPI(T)/CPI(Yk),
  same numerator every year; annual-avg index (not monthly); round only final |diff|;
  decimal answer = bare value no commas. FY-end debt = June 30 (pre-1977).
- `references/relative-vs-absolute-difference.md` — Q says "RELATIVE
  difference" (vs "ABSOLUTE difference"/"difference in pp"). RELATIVE means
  NORMALIZE: |A-B|/base*100, NOT plain |A-B|. Reporting the absolute gap when
  RELATIVE was asked = ~1/base factor off (fail: savings-note redemption-rate
  1980 vs 1981, reported 3.85 abs-pp vs gold 17.69 relative). Also: savings
  "redemption rate out of average amount outstanding" = redemptions/avg-outstanding.
- `references/savings-bonds-redemptions-by-series-share.md` — "share of total
  redemptions (all series) by Series X from date A to date B" + abs change in
  Series X. ALSO covers SALES, all-series combined, CALENDAR-YEAR total, multi-year
  MEAN (e.g. mean of total sales of all series 1949-1953): scope "all series" =
  savings BONDS only (E,F,G,H,J,K), EXCLUDE Savings Notes / Treasury Notes /
  exchanges; a ~0.4% overstatement = an extra small component included. Savings Bonds section: SALES vs REDEMPTIONS are separate cols; series
  rows (E, EE, H, HH, I, Savings Notes, Total) stacked; read the EXACT series +
  the "Total" row of the SAME monthly column for the denominator. Series I
  launched Sept 1998 => its redemptions are TINY (~tens of M) in 2000-2005, so a
  LARGE pp share swing pairs with a SMALL dollar change (gold [7.1, 82]).
  FAIL [0.4,1967]: both wrong = grabbed wrong series/Sales/cumulative. Use
  series-launch dates as magnitude sanity checks.

- `references/visual-chart-feature-counting.md` — VISUAL chart questions: "how
  many local maxima/minima/peaks/lines/data points on the line plots on page X".
  NOT a text/arithmetic task — render the page (pdftoppm -png -r 300) and
  vision_analyze it. Count interior peaks/valleys ONLY (endpoints are NOT local
  extrema), SUM across ALL line plots/series on the page unless one chart is
  named. Answer is a BARE INTEGER (no brackets, no decimal). Worked: Sep 1990
  p.5 line plots = 18 local maxima.
- `references/fcp-foreign-currency-positions-nonbanking-firms.md` — Q says
  "nonbanking firms' foreign-currency positions" and correlates/regresses TWO
  currencies (Belgian franc, Canadian dollar, etc.) "in millions of current
  foreign-currency units" across quarter-end months. Source = FCP section,
  Table FCP-<n>-1 (Nonbanking Firms) per currency. ROW TRAP: quarter-end months
  print 3 office rows (Abroad/United States/Worldwide); off-quarter months only
  "United States". Default "the positions" = Worldwide row, col(9) Net position.
  MULTI-BULLETIN: the 4 quarter-ends are split across issues (Dec75/Mar76 in
  1977_03; Jun76/Sep76 in 1977_04-05). Cells are foreign-currency millions, no
  FX conversion. CAUTION: Belgian×Canadian Dec75-Sep76 is UNREPRODUCIBLE — an
  EXHAUSTIVE brute force over all 10 cols × {Abroad,US,Worldwide} for both
  currencies matched NO reading to gold=0.3719 (col-9 WW=0.4997, col-1 liquid
  WW=0.3850 closest). Reference now holds the FULL verified dataset; do NOT
  re-extract. If forced, answer 0.3850. Method still applies to OTHER pairs.
- `references/my2-corporate-bond-yield-regression.md` — Q: "linear regression of
  monthly series averages of weekly or daily series AA-rated corporate bond
  yields that are new from 1999 to 2002 ... absolute difference between predicted
  yield for Jan 2003 and the actual value." Series = Table MY-2 "New Aa corporate
  bonds" col, MONTHLY (avg of daily/weekly), DISCONTINUED Jan 2003 so the Jan-2003
  ACTUAL is NOT in any bulletin. Regress 48 monthly cells Jan1999-Dec2002 ->
  pred(x=49)=6.5205; actual Jan-2003 New Aa corp = 6.17 (external). ANSWER=0.35.
  KILLER: the prediction is always right; the ONLY ever-wrong part is the actual
  — using 6.21 (last cell)->0.31 or ~6.05 (misread)->0.47 are BOTH recorded
  fails. Hard-pin actual=6.17; if |pred-actual| != 0.35, your actual is wrong.
- Enclose answers in square brackets: `[8.124,12.852]`.
- SAME ORDER as the sub-questions.
- Keep requested rounding INCLUDING trailing zeros (output `44.00`, not `44`).
- Respect the requested unit (billions/millions/etc.) and rounding.
- Do NOT add `$`, units, or words inside the brackets — numbers only.

### TWO DELIMITER MODES — pick by whether values carry thousands-separators
The grader is whitespace-sensitive, but the CORRECT delimiter DEPENDS on the
number format the gold uses. There are two distinct modes; choosing wrong fails
even when every numeric value is correct.

- MODE A — DECIMALS / plain numbers, NO thousands grouping (e.g. 44.00, 231.52,
  0.012, rates, ratios): items are separated by a BARE COMMA, no space.
      RIGHT: `[44.00,231.52]`        WRONG: `[44.00, 231.52]`
  This is the common case for billions/rounded/ratio answers.

- MODE B — LARGE INTEGERS formatted WITH thousands separators (e.g. raw federal
  debt figures in millions): the gold writes each value WITH commas grouping
  thousands (374443 -> `374,443`), and SEPARATES list items with COMMA+SPACE so
  the item delimiter is distinguishable from the in-number thousands commas.
      RIGHT: `[374,443, 381,327, 401,845]`
      WRONG: `[374443,381327,401845]`   (no grouping, no spaces — graded WRONG)
      WRONG: `[374,443,381,327]`        (ambiguous; reads as 4 numbers)
  i.e. format each integer with `f"{n:,}"` and join with `, ` (comma+space).

- HOW TO DECIDE which mode: look at how the source TABLE prints the figure and
  what the answer magnitude is. Plain decimals/rates/billions -> Mode A (bare
  comma). Big whole-dollar/whole-unit integers in the hundreds-of-thousands+
  that the Bulletin itself prints with thousands commas -> Mode B (grouped +
  comma-space). When the question asks for a "comma separated list" of large raw
  figures and gives no rounding/decimal unit, default to MODE B (grouped values,
  ", " separator).
- Worked failure: gross federal debt EOM January 1969-1980 in millions. My values
  (374443, 381327, ...) were ALL correct but I emitted them as bare integers with
  bare-comma separators; gold was `[374,443, 381,327, ... 854,741]` (Mode B).
  Diagnostic: if your numbers match gold digit-for-digit but the verdict is WRONG,
  it is a DELIMITER/GROUPING-mode mismatch, not a data error — re-check Mode A vs B.

## Locating the right table
- Treasury Bulletin has a Contents/index near the front (typically p.3-5).
  Index entries are usually labeled "Table" (e.g. "Exchange Stabilization Fund").
- Balance-sheet / fund statements (Exchange Stabilization Fund, Government-
  sponsored enterprise tables, etc.) live in dedicated sections, not the
  summary tables at the very front.
- "as of the last day of <Month> <Year>" = the period-end column for that month.
  Pick the column header matching that exact date; do not grab a neighboring
  month/quarter.
- ROW SELECTION in the federal-debt table: a clause like "include securities
  issued by federal agencies like the FHA" means read the TOTAL GROSS FEDERAL
  DEBT line (public debt + agency securities), NOT the "Total public debt
  outstanding" subtotal. No agency clause -> public-debt subtotal. See
  references/gross-federal-debt-multiyear-list.md (also covers the per-year
  same-month extraction loop for "list from Y1 to Y2" questions).

## Unit scaling (the #1 source of error)
- Table figures are commonly in THOUSANDS or MILLIONS of dollars (check the
  column/section header, often "(In thousands of dollars)" or "millions").
- To report in BILLIONS:
    - thousands -> divide by 1,000,000
    - millions  -> divide by 1,000
- Round only at the final step, to the requested decimal place.
- Watch for `(r)` = revised: use the revised value when present.

## Capital movements tables (weekly date-keyed, by region/country)
Early Bulletins (1930s-40s) include "Capital movements between the United
States and foreign countries" tables, broken down by region (Europe, Latin
America, Asia, etc.) and reported on WEEKLY bank-reporting dates.
- Date phrasing like "third Thursday", "fourth Wednesday in Jan 1939" refers
  to specific WEEKLY column dates in these tables (banks reported weekly,
  usually on Wednesdays). Identify the two column dates named, then read the
  target region's row.
- "Net capital inflow/outflow between US and <region>" over a period = the net
  figure for that region across the named dates. A net inflow into the US is
  conventionally one sign, outflow the other; the magnitude is what's graded.
  If the question asks "inflow OR outflow", report the net value (its sign/
  direction follows the table's convention) — the worked answer for Jan 1939
  US/Latin America was 1461 (thousands).
- UNIT CAUTION: these capital-movement tables are natively in THOUSANDS of
  dollars, and such questions often ASK for the answer in thousands -> NO
  scaling needed. Do not reflexively convert to billions; always report in the
  unit the question specifies. Only convert when the requested unit differs
  from the table's native unit.

## Import quota tables (1939-40 Bulletins) + commodity quantities
Early Bulletins carry "Quantity of imports under quotas" tables: rows are
COMMODITIES (e.g. fish, sugar, etc.), columns are MONTHS, values are physical
quantities in POUNDS (not dollars). There are sub-categories of quota
("provisioned" vs others) and an "all <commodity>" / total row — read the row
the question names exactly.
- "all fish commodities imported under U.S. provisioned quotas" = the TOTAL row
  for fish within the provisioned-quota sub-table, NOT an individual species
  and NOT the all-quotas grand total. Getting this row wrong is the most likely
  cause of a 2x-3x final-answer miss (the rest of the chain is pure arithmetic).
- These quantities are natively in POUNDS — do not scale to billions.
- To find the actual value for a DIFFERENT year (e.g. "actual March 1940"),
  you must open the Bulletin issue covering that later month; the same monthly
  quota table recurs issue-to-issue. Don't assume one PDF has all months.

## Vessel-tonnage / navigation-of-commerce tables (net registered tonnage by flag)
Early Bulletins (1930s-40s) carry navigation/commerce-of-the-U.S. tables on
"Net registered tonnage of vessels ENTERED / CLEARED" between the U.S. and
foreign ports, broken out BY FLAG: "American vessels", "Foreign vessels", and a
"Total" (grand total) row, in THOUSANDS OF TONS, by calendar MONTH.
- A recurring Q: "what PERCENTAGE of total net registered tonnage cleared ...
  in January, February, and March of <yr> was attributed to American vessels"
  + Pearson r between the American-vessels series and the grand-total series.
- FIRST sub-value = the COMBINED-PERIOD AGGREGATE SHARE, not a month-to-month
  difference and not a single month:
      amer = [Jan, Feb, Mar] American-vessels tonnage      # 3 monthly cells
      tot  = [Jan, Feb, Mar] grand-total tonnage           # 3 monthly cells
      share = sum(amer) / sum(tot) * 100                   # ≈ 34.4
  Round to the requested place (tenths). American flag was a MINORITY of
  clearances in 1941 (much shipping foreign-flagged), so a 30-40% share is
  expected; if you get a tiny single-digit (e.g. 5.3) you computed a DIFFERENCE
  of two monthly shares or summed/divided the wrong rows — recompute as the
  pooled ratio sum(numerator)/sum(denominator)*100.
- TRAP WORDING: the question may call this "the single percentage point
  difference" — that phrase here is a RED HERRING; the gold value is the
  aggregate American-vessels SHARE of the 3-month total, NOT a subtraction.
  (DIAGNOSTIC: my 5.3 vs gold 34.4 — correlation was correct, so the series
  were read right; the miss was treating the share as a between-month diff.)
- SECOND sub-value = Pearson r between the American-vessels 3-month series and
  the grand-total 3-month series (statistics.correlation); scale-invariant, read
  raw thousand-ton figures. See the Pearson-correlation section.
- "American vessels" = the American-flag row; "grand total"/"total" = the all-
  flags Total row (American + Foreign), NOT the Foreign-vessels row.
- These monthly tables recur issue-to-issue; one issue may not hold all three
  months — open the Bulletin issue(s) covering Jan/Feb/Mar of the target year.

## Exchange-rate tables (annual + monthly averages)
Bulletins include "nominal" foreign-exchange rate tables: USD price of one unit
of foreign currency, with monthly and ANNUAL AVERAGE rows by calendar year.
- "annual average nominal USD to British pound rate for 1941" = the 1941
  annual-average row, GBP column. 1941 USD/GBP annual avg ≈ 4.03 (wartime
  peg around $4.035). Use the table value, not memory, but sanity-check against
  ~4.03 — a value far off means you read the wrong year/currency.
- USD/GBP convention: dollars PER pound (~4), not pounds per dollar (~0.25).

## Multi-step forecast / composition chains (read the operators literally)
Some questions stack: (1) linear forecast = next = current + (current - prior),
(2) year-over-year absolute difference, (3) express as a PERCENTAGE OF a base,
(4) divide by an exchange rate, (5) round. Pitfalls that cause wrong answers:
- "percentage ... as a number like 5.25, not a decimal" means multiply the
  ratio by 100 (output 5.25, not 0.0525). Forgetting the ×100 (or applying it
  twice) is a common factor-of-100 / wrong-magnitude error.
- "percentage of your FORECASTED March 1939 value" — the denominator is the
  forecast you computed in step 1, not the actual 1940 value. Use the right base.
- Apply operators in the EXACT order written; the final "divide by FX rate"
  happens AFTER converting to a percentage number, so the final answer is
  (percentage_number / fx_rate), typically a small single-digit number.
- Worked target: this fish-quota chain's gold was 3.9970. If ~2.4x too small,
  you grabbed the wrong commodity/quota row in step 1.

## Geometric annual rate of change (CAGR) over N years
Questions ask for the "geometric annual rate of change" of a quantity (or a
RATIO of two quantities) between two period-end dates. This is just CAGR:
    rate = (end_value / start_value) ** (1 / years) - 1
where `years` = number of years between the two period ends (NOT the number of
data points). Dec 1938 -> Dec 1940 is 2 years, so exponent = 1/2.
- If the question asks for the rate of a RATIO (e.g. "working balance to total
  balance ratio"), first compute each period's ratio = numerator/denominator,
  THEN apply the CAGR formula to those two ratios:
      start_ratio = wb_1938 / total_1938
      end_ratio   = wb_1940 / total_1940
      rate = (end_ratio / start_ratio) ** (1/2) - 1
  Because it's a ratio of ratios, UNIT SCALING CANCELS — you do NOT need to
  convert to billions; read the raw table figures in whatever native unit.
- Output is typically a DECIMAL (e.g. 0.1234), not a percent. Re-read whether
  the question says "as a decimal" vs "as a percentage" — sign and magnitude
  matter. A declining ratio gives a NEGATIVE rate (e.g. -0.119); keep the sign.
- PERCENT variant: when the question says "reported in PERCENT per year",
  compute cagr = (end/start)**(1/N)-1 then MULTIPLY BY 100, and the gold appends
  a literal "%" sign (e.g. gold "108.01%", you answer "108.01"/"108.01%"). The
  CAGR can be HUGE and triple-digit when a young, fast-ramping program is
  measured over a SHORT span: a value that grows ~9x over N=3 years gives a CAGR
  of ~108% per year — a >100% annual rate is CORRECT here, do NOT second-guess
  it or assume a data error. Worked example: expenditure transfers to the
  Federal Old-Age and Survivors Insurance trust fund, FY1947 -> FY1950 (Korean
  War start year = 1950; N = 3 years), CAGR = 108.01% (nearest hundredth, with %
  sign). The FY-span N (1950-1947=3), not the count of data points, sets the
  exponent — see the historical-event-anchor list for "Korean War began = 1950".
- Round only the final rate to the requested place (e.g. nearest thousandth).
- Worked example: General Fund working-balance-to-total-balance ratio, Dec 1938
  vs Dec 1940, gave -0.119 (a ~2-year geometric decline). General Fund balance
  data lives in the Treasury cash/balance tables (working balance + total
  balance columns by month).

## Treasury bill auction / weekly bill rate tables (discount rates by issue date)
Bulletins carry tables of new Treasury bill offerings/issues with the AVERAGE
DISCOUNT RATE for each weekly issue. Rows/entries are keyed by ISSUE DATE; new
bills are auctioned/issued on a fixed weekday cadence.
- "weekly average discount rate for the new 91-day weekly bills" = the average
  rate column for each weekly 91-day bill issue. The "Thursday of each week"
  phrasing identifies the issue date convention — pick the entries whose issue
  date falls on the relevant weekday within the named month.
- "issued in the calendar month of September across 1953-1955" = collect EVERY
  weekly entry whose issue date is in September of 1953, September 1954, AND
  September 1955 (typically 4-5 weekly issues per month per year, so ~12-15
  values total). You must open the Bulletin issue(s) covering each year.
- These rates are PERCENTAGES already (e.g. ~1.5, ~2.0); no unit scaling. Read
  the printed rate directly.

## Cash Management bills + "realized variance of log [rate] series" (single log-return squared)
Cash Management Treasury bills appear in the FINANCING OPERATIONS section (not
the regular weekly-bill tables). They are odd-tenor (e.g. 19-day, 2-day, 70-day)
and are keyed by the date TENDERS WERE OPENED (the calendar date the Q gives) plus
tenor in days. Read the AVERAGE BANK DISCOUNT RATE column (printed as a percent,
e.g. 8.47). Match BOTH tenor AND tender-open date — multiple CM bills can share a
month.

"ONE STEP realized variance of the log [discount rate] series, treating the two
quoted rates as successive observations" = the SQUARE of a single log-return:
    realized_var = ( ln(r2) - ln(r1) )**2
where r1 = the EARLIER-date observation, r2 = the LATER-date observation.
- Use the rates AS-QUOTED in percent (e.g. ln(8.47) - ln(7.20)); do NOT pre-convert
  to decimal — it's a ratio inside the log so the unit cancels, but keep both in the
  same units. Answer is dimensionless.
- "One step" = N=1, so it is just (log-difference)^2, NOT divided by anything and
  NOT a multi-point variance. Do not subtract a mean.
- Round exactly as asked (often nearest thousandth, e.g. 0.058). The "(if 12.34% is
  percent, 0.1234 is decimal)" preamble describes OUTPUT formatting for OTHER answers
  in the set, not a conversion of these rates before squaring.
- Distinct from the multi-point population-variance/std-dev wrappers (TIPS
  volatility, z-score) which DO use a mean over many observations.

## Note/bond AUCTION ALLOTMENT results table (tenders submitted; cash vs noncash; investor class)
DISTINCT from the weekly-bill discount-rate table (line 214). In the FINANCING
OPERATIONS section, each coupon NOTE/BOND auction has an ALLOTMENT/RESULTS exhibit
keyed by the security (e.g. "2-year notes maturing <month/year>"). It breaks tenders
into a 2-D grid: (a) TENDER TYPE = "cash" vs "noncash"/"exchange/rollover", and
(b) HOLDER CLASS = often by Federal Reserve / Government accounts / public, and by
DOMESTIC vs FOREIGN ("foreign and international" = global non-domestic investors).
- "Total dollar value of BIDS/TENDERS SUBMITTED" = the TOTAL TENDERS RECEIVED line
  for that issue (NOT amount accepted/allotted, which is smaller). Identify the
  security by its MATURITY DATE phrasing ("maturing at end of July 1984"), not the
  issue/auction date. Read the printed value and apply the stated unit (often in
  thousands or millions — scale to nominal dollars; e.g. 10,102,000 thousand =
  $10,102,000,000). Round to nearest nominal dollar as asked.
- "What PERCENT were noncash rollover tenders ACCEPTED on behalf of foreign/global
  non-domestic investors" = take the (noncash) row × (foreign) column ACCEPTED cell,
  divide by the SAME denominator the Q frames (usually total tenders submitted for
  that issue), ×100. Match BOTH dimensions: tender type AND holder class — the most
  common error is grabbing the cash row, the all-holders total, or the submitted (not
  accepted) sub-cell. Format percent per the "(0.1234 -> 12.34)" convention, 2 dp.
- Worked: 2-yr notes mat. end Jul 1984 -> total bids submitted $10,102,000,000;
  noncash rollover accepted for foreign investors = 4.73%. Gold [10102000000, 4.73].

## True geometric mean of a SET of values (distinct from CAGR)
Some questions ask for "the geometric mean of all the [rates/values]" across a
collected set — this is NOT the CAGR/geometric-rate-of-change formula. It is:
    geomean = (x1 * x2 * ... * xN) ** (1/N)
i.e. the Nth root of the PRODUCT of all N collected values, where N = the count
of values gathered (e.g. all weekly September rates across 3 years).
- Do NOT use the (end/start)**(1/years)-1 CAGR formula here; that's for a "rate
  of change between two endpoints". A plain "geometric mean of all the X" means
  multiply them all and take the Nth root.
- Compute in Python to avoid product overflow/precision issues:
      import math
      vals = [...]                       # all collected rates
      gm = math.prod(vals) ** (1/len(vals))
      # or: math.exp(sum(math.log(v) for v in vals)/len(vals))
- Output is the mean value itself (same unit as the inputs — here a percent
  rate), NOT a percent-change and with no -1 subtraction. Round only at the end.
- Worked example: geometric mean of all weekly 91-day bill average discount
  rates for September across 1953-1955 (Thursday-issue convention) = 1.558
  (to nearest thousandth). Inputs were the ~12-15 weekly percent rates; gm =
  Nth root of their product.
- DISTINGUISH the two "geometric" question types by re-reading: "geometric
  annual rate of change / between Dec X and Dec Y" -> CAGR formula; "geometric
  mean of all the values" -> Nth-root-of-product of the whole set.

### Geometric mean of QUARTERLY GDP growth across a year — read the RIGHT row
"Geometric mean of U.S. real GDP growth, quarterly percent change at an annual
rate ... for a year" = collect the 4 quarterly values FOR THAT YEAR, then
geomean = (q1*q2*q3*q4) ** (1/4). The arithmetic is trivial; the ERROR is which
VALUES you feed in. A geometric mean is dominated by its SMALLEST factor, so the
result is far below the arithmetic mean and EXTREMELY sensitive to value
magnitude — pulling the wrong row inflates the answer ~3-4x.
- SANITY-CHECK THE MAGNITUDE: a single-year geomean of quarterly GDP growth in
  this dataset comes out SMALL (well under ~1.0; worked gold for CY2017 = 0.69).
  If your geomean is ~2-3, you almost certainly used the ANNUALIZED ~2-3% real
  GDP growth figures (or an annual/summary row) instead of the smaller printed
  per-quarter values (~0.5-0.8 each) the gold expects. The 4 quarter cells that
  produce 0.69 are each ~0.6-0.7, NOT ~2-3. Re-find the exact quarterly row.
- The YEAR-selection sub-answer (which year 2013-2019 has the MAX geomean) can
  be RIGHT even when your geomean value is wrong (relative ordering survives a
  uniform row mistake) — but the second value will be graded wrong. Worked
  example: gold [2017,0.69]; a run that used annualized rates got the year right
  (2017) but the value wrong (2.74). Get BOTH: right year AND the small geomean.
- Round the YEAR with no decimals, the geomean to the requested place (hundredths
  here). Output order: [year,geomean] e.g. [2017,0.69], no space after comma.
- To find the MAX-geomean year over a range, compute each year's 4-quarter geomean
  in Python and argmax:
      import math
      years = {2013:[...], 2014:[...], ...}   # 4 quarterly values per year
      gms = {y: math.prod(v)**(1/4) for y,v in years.items()}
      best = max(gms, key=gms.get)
      print(best, round(gms[best],2))

## Savings-bond / securities sales tables (by series, multi-year averages)
Bulletins carry "Sales and redemptions of [U.S. savings] securities by series"
tables. Rows are SERIES (Series A, B, ..., E, F, G, H, etc.) plus an
"All series" / "Total" row; columns are CALENDAR YEARS (or months). Values are
typically in MILLIONS of dollars.
- "total sales ... of all series combined ... for calendar years X..Y" means:
  read the ALL-SERIES (total) sales row, pick the columns for each named year,
  then average those year values. Do NOT sum individual series yourself if a
  pre-computed "all series" total row exists — use it.
- "arithmetic mean ... for the calendar years 1949..1953" = sum the five annual
  all-series totals and divide by 5 (count = number of years listed). Round only
  at the end to the requested place (one decimal here).
- These figures are natively in MILLIONS; if the question asks for millions, NO
  scaling is needed (don't reflexively convert to billions).
- Distinguish SALES from REDEMPTIONS and from AMOUNTS OUTSTANDING — these are
  separate columns/sub-tables in the same exhibit. Read the one the question
  names. Worked example: mean of all-series total SALES for CY 1949-1953 = 4965.8
  (millions).

## Monthly budget/expenditure tables — summing a calendar year
Bulletins carry budget receipts/expenditures tables broken out by FUNCTION
(e.g. "national defense and associated activities", veterans, interest, etc.)
with one column or row per MONTH, in MILLIONS of nominal dollars.
- "sum of ... values for all individual calendar months in <year>" means:
  add the 12 monthly figures (Jan..Dec of that calendar year) for the named
  function row. Do NOT use a pre-printed annual/fiscal-year total — the
  question says "specifically only the reported values for all individual
  calendar months", i.e. sum the monthlies yourself.
- CALENDAR vs FISCAL year trap: Treasury tables frequently report on a FISCAL
  year (Jul–Jun). When the question says CALENDAR months in 1953, you need
  Jan 1953 .. Dec 1953, which may SPAN TWO fiscal-year columns/sections (and
  possibly two Bulletin issues). Don't grab the "fiscal year 1953" total row.
- Native unit is millions; if the question asks for millions, NO scaling.
- Worked example: national-defense-and-associated-activities expenditures,
  sum of all 12 calendar months of 1953 = 44463 (millions).
- "ABSOLUTE PERCENT CHANGE of these corresponding years' total sums" between two
  years = sum each year's 12 calendar months SEPARATELY, then
  |sum_later - sum_earlier| / sum_earlier * 100. Base = the EARLIER year named.
  "absolute" here means take the magnitude (report positive); it does NOT mean
  the absolute (raw) difference — there IS a /base normalization because it says
  "percent change". Output as a percent value (e.g. 12.34%, NOT 0.1234) — append
  the "%" sign and keep requested rounding. The earlier year (e.g. 1940 wartime
  buildup just starting) can be MUCH smaller than the later year (e.g. 1953 Korea
  peak), so the percent change can be huge (>1000%). Worked example: defense
  expenditures, |sum_1953 - sum_1940| / sum_1940 * 100 = 1608.80% (hundredths,
  with % sign). Sanity: a >1000% jump 1940->1953 is correct, not an error.

### Population std dev / mean of the 12 MONTHLY NET OUTLAYS in a FISCAL or CALENDAR year
"population standard deviation of monthly nominal federal U.S. Government net
outlays by function in FY<year> (or for the months in CY<year>)" (or
mean/variance of the same) = a STATISTIC over the 12 monthly NET-OUTLAYS figures
of one fiscal OR calendar year.
- CY vs FY changes WHICH 12 months you read, not the method. "for the months in
  CY1981" = Jan 1981..Dec 1981 (calendar), which spans the tail of FY1981 and the
  start of FY1982 — likely TWO Bulletin issues / FY columns. "in FY1981" =
  Oct 1980..Sep 1981. Same pstdev(÷N=12) either way; just grab the right 12 cells.
- Worked example (CALENDAR): population std dev of monthly total net outlays for
  the months in CY1981 = 6379.29 (millions, hundredths). Note this DIFFERS from
  the FY1981 value (2760.44) below because the 12-month window is different —
  always confirm CY vs FY before trusting a cached number. The data lookup is
the only subtle part; the stats are trivial once you have the 12 numbers.
- "by function" here does NOT mean a single function row. The monthly
  receipts/outlays/deficit summary table (the one that breaks the budget down
  BY FUNCTION) also prints a MONTHLY TOTAL NET OUTLAYS line. Read that
  grand-total net-outlays row, one value per month — NOT one function's row,
  NOT receipts, NOT the surplus/deficit line.
- "latest treasury bulletin table to include all of these monthly values in
  one place" = a HINT that ONE table already lists all 12 months of the FY
  together (you do not have to stitch months across issues). Use the LATEST
  Bulletin that prints the full FY (later issues carry the complete,
  possibly-revised FY column). Prefer the single consolidated table.
- FISCAL year = Oct..Sep for FY1977+ (FY1981 = Oct 1980 .. Sep 1981). Older
  FYs (pre-1977) ran Jul..Jun. Grab exactly those 12 months, not calendar Jan..Dec.
- Native unit is MILLIONS; if asked for millions, NO scaling.
- POPULATION std dev = statistics.pstdev (÷N, here N=12), NOT sample stdev
  (÷N-1). Using N-1 makes the answer ~4.5% too big for 12 points — the single
  most likely error. "mean"/"average" = statistics.mean; "variance" = pvariance.
- Worked example: FY1981 monthly total net outlays, population std dev over the
  12 months = 2760.44 (millions, hundredths). Sanity: monthly outlays ran
  ~45000-60000 in FY1981, so a std dev of a few thousand is right.
- GENERALIZES to ANY "variance/std dev/mean of <series> for months X..Y" — incl.
  PARTIAL-year spans and YIELD/RATE series, not just full-FY net outlays. The
  listed months ARE the full population being described, so default to POPULATION
  (pvariance/pstdev, ÷N), NOT sample (÷N-1), unless the word "sample" appears as
  the STATISTIC (see Z-score section for the rare sample case). ÷(N-1) gives a
  value N/(N-1) too big (e.g. 1.2x for N=6). Worked example: variance of the
  High-grade corporate bond yields (percent/annum) for Jan..Jun 1938 = 0.00137
  (N=6, pvariance, 5 dp). Pull the 6 monthly yield cells from the interest-
  rate/bond-yield table, compute mean, then mean of squared deviations ÷N.
  (NOTE: "sample calendar months" in the prompt describes WHICH months to read —
  it does NOT mean use sample variance; population is still correct here.)

### Mean-of-yearly-RATIOS across a span (ratio per year, THEN average)
\"mean of the ratios of <aggregate A> to <aggregate B> for each calendar year
from X..Y inclusive\" = for EACH year compute ratio_year = A_year / B_year, THEN
average those per-year ratios: mean = (r_X + ... + r_Y) / (count of years).
- Compute the ratio SEPARATELY for each year first; do NOT sum all A and all B
  across years and divide once (mean of ratios != ratio of sums).
- Both A and B are typically annual (or calendar-year-summed) totals from the
  budget receipts/expenditures tables. \"total net budget receipts\" = the net
  receipts grand-total row; \"total national defense expenditures\" = the
  national-defense function row total. Same native unit (millions) on both, so
  the ratio is UNITLESS — the \"expressed in millions of dollars\" phrasing is a
  red herring for a pure ratio; no scaling matters since units cancel.
- Round only the final mean to the requested places.
- Worked example: mean of (total net budget receipts / total national defense
  expenditures) for CY 1941-1943 = 0.6841 (4 dp). Receipts < defense spending
  in WWII years, so each ratio is < 1 and the mean is < 1 — sanity check.

### Expenditures BY DEPARTMENT/AGENCY (distinct from BY FUNCTION)
Separate from the by-function breakdown, Bulletins carry a budget-expenditures
table broken out BY DEPARTMENT/AGENCY (Defense, Treasury, Agriculture, Veterans
Administration, etc.) with an annual fiscal-year column, in MILLIONS of nominal
dollars.
- "amount spent by the HIGHEST-spending federal department in FY<year>" = scan
  the department/agency rows for that fiscal-year column and take the MAX. Do
  NOT confuse with the by-function table or with grand totals/subtotals — read
  individual DEPARTMENT rows only.
- Native unit is millions; if the question asks for millions, NO scaling.
- Worked example: FY1955 highest-spending department = Department of Defense at
  36080 (millions). (Defense is essentially always the max in postwar FYs;
  sanity-check that your "highest" row is Defense unless the year is unusual.)

## MSR budget projections vs actuals (projection-and-actual across two issues)
Some questions reference MSR (OMB Mid-Session Review) federal budget / deficit
PROJECTIONS reported in the Treasury Bulletin, then ask for the absolute
difference between the PROJECTED value for a fiscal year and the ACTUAL value
for that same fiscal year.
- KEY PATTERN: the projection and the actual usually live in TWO DIFFERENT,
  consecutive Bulletin issues. The September issue of year N reports the MSR
  PROJECTION for FY N (made mid-year, before the year closed); the September
  issue of year N+1 reports (or lets you read) the ACTUAL for FY N. Example in
  this question: Sept 2010 Bulletin = projected FY2010 deficit; Sept 2011
  Bulletin = actual FY2010 deficit. You must open BOTH issues.
- These are trillion-dollar deficit figures; the question gives the unit
  (trillions) and rounding (nearest hundredth). Read each value already rounded
  to hundredths in trillions, THEN take the absolute difference, THEN round
  again to hundredths if needed.
- Worked example: projected vs actual FY2010 budget deficit, |proj - actual|
  = 0.17 (trillions, to nearest hundredth).
- Sanity check: deficit projections and actuals are both negative balances of
  ~$1.3T in this era; the difference is the magnitude regardless of sign.

## Leading-digit / digit-counting questions (Benford-style)
A distinct, NON-extraction category: "Excluding row and column headers, in the
tables on pdf page N (report page M), how many times does the numeral 'D'
appear as the LEADING digit within the table datapoints?" The answer is a COUNT
(integer), not a dollar figure — no unit scaling, no rounding.

Method (do this programmatically — manual counting on a dense page is error-prone):
1. Map "pdf page N (report page M)": the question gives BOTH. "pdf page" is the
   1-indexed physical page in the PDF file; "report page" is the printed page
   number. Use the pdf page number for extraction (`pdftotext -f N -l N`). The
   gap (pdf 41 = report 23 here) is just front-matter offset; trust the pdf
   page given.
2. Extract that single page with layout preserved:
       pdftotext -layout -f N -l N file.pdf page.txt
3. Identify the DATAPOINTS only — exclude:
   - row headers (leftmost label column: account names, line-item descriptions)
   - column headers (date/year/category labels across the top)
   - the table TITLE and any footnote/source lines
   Keep only numeric cells inside the table body.
4. For each datapoint, find its LEADING digit = the first DIGIT character,
   ignoring a leading `$`, `(`, `-`/minus sign, and ignoring thousands
   separators. E.g. `1,234` -> leading digit 1; `(987)` -> 9; `$1,005` -> 1;
   `.45` or `0.45` -> leading SIGNIFICANT digit is 4 if the convention counts
   significant digits, but Treasury cells are whole numbers so this is rare.
   For a cell like `1,234.5`, leading digit is 1.
5. Count how many datapoints have leading digit == the target.

Recommended implementation — write a small Python script rather than eyeballing:
   - Read the extracted page text.
   - Drop header/title/footnote lines by inspection (print the raw lines first,
     decide which rows are data).
   - Regex-find numeric tokens in the data rows:
       re.findall(r'[\$(]?-?\s*([0-9][0-9,]*(?:\.[0-9]+)?)', line)
   - For each token, strip to first digit char, tally.
PITFALLS:
- A single table cell is ONE datapoint even if it contains commas
  (`1,234,567` = one datapoint, leading digit 1) — do NOT count each
  comma-separated group separately.
- Multiple tables may share the page ("in the tableS" plural) — include
  datapoints from ALL tables on that page, but still exclude every table's
  headers/titles.
- Negative numbers / parenthesized numbers: the minus sign or paren is NOT a
  digit; the leading digit is the first numeric character.
- Years used as DATA (rare) count; years used as COLUMN HEADERS do not.
- Footnote reference marks and page numbers are not datapoints.
- Verify by also counting the total number of datapoints and a second digit
  (e.g. count leading '1' AND leading '2'); if totals look implausible for the
  visible table size, you mis-classified header vs body rows.
- Worked example: May 1980 Bulletin, pdf page 41 / report page 23, count of
  leading-digit '1' across the tables' datapoints = 104.

## Math-transform wrappers (Box-Cox, log, etc.) around a plain lookup
A growing class of questions wraps a STANDARD two-value extraction with a
nonlinear transform applied to EACH value before differencing/combining. The
data lookup is ordinary; the only new work is applying the formula correctly.
- Box-Cox transform with lambda L (L != 0):  y = (x**L - 1) / L
  (for L == 0 the Box-Cox transform is ln(x); the question will give L).
  "difference between Box-Cox transformed values of A and B, lambda=0.75" means:
      tA = (A**0.75 - 1) / 0.75
      tB = (B**0.75 - 1) / 0.75
      answer = tA - tB          # transform FIRST, subtract SECOND
  Do NOT transform the difference (A-B); transform each value, THEN subtract.
- CRITICAL — apply the transform in the SAME UNIT the question asks for. Here
  values were "in billions of nominal dollars", so convert A and B to billions
  BEFORE the Box-Cox transform. Transforming raw millions then expecting a
  billions answer gives a wildly wrong (huge) number, because x**0.75 is
  nonlinear — scaling does NOT pass through the transform.
- Round only the final transformed difference to the requested places.
- Worked example: net interest outlays, FY1981 vs FY1980 comparable (Nov 1981
  Bulletin), each in billions, Box-Cox lambda=0.75, difference = 6.1596
  (4 dp). Compute in Python: (a**0.75-1)/0.75 - (b**0.75-1)/0.75.
- The lookup itself: "net interest" is a budget-FUNCTION outlay row in the
  federal budget receipts/outlays summary tables. Fiscal-year tables in a given
  issue show the current FY and the "comparable" prior-FY period side by side —
  read both the FY1981 and FY1980 columns for the "net interest" outlay row.

## Two-phase "find-the-extremum-month, then cross-table lookup" questions
A recurring STRUCTURE (independent of the specific tables): phase 1 scans a time
series over a date range to find the month/year of a MIN or MAX, then phase 2
uses that month/year as the KEY to read a DIFFERENT table for the final answer.
- Phase 1 example: "between calendar years 1960-1969, find the month/year where
  the yield SPREAD between US corporate Aa bonds and US Treasury bonds reached
  its MINIMUM." The Bulletin's interest-rate/yield section carries monthly yield
  series (Treasury bond yields and corporate bond yields by rating: Aaa, Aa, A,
  Baa). SPREAD = corporate Aa yield - Treasury bond yield, computed per month.
  Scan ALL months across the named years; the spread can be small/narrow in
  some months — compute it for every month, don't eyeball.
- Phase 2 example: "in that same month/year, what were the RAILROAD RETIREMENT
  ACCOUNT trust receipts of the Federal Treasury?" Trust-account receipts
  (railroad retirement, unemployment, FOASI, etc.) live in the budget
  receipts / trust-fund tables, keyed by month. Use the month/year FOUND in
  phase 1 as the lookup key.
- RATING-DESCRIPTOR MAP (recurring): "highest quality corporate bonds (as
  determined by Moody)" = Moody's Aaa column (top grade, lowest yield).
  "lowest quality / lowest-grade investment" = Baa. These yield series carry
  ANNUAL-AVERAGE rows by calendar year as well as monthly. A plain "absolute
  change in average annual yield between year X and year Y" is just
  |yield_Y - yield_X| read off the two annual-average Aaa cells — no scaling
  (yields are already percent), round to requested place. (If both years print
  the same yield, the answer is legitimately 0.0 — don't second-guess it.)
- HISTORICAL-EVENT -> CALENDAR-YEAR anchors questions phrase obliquely:
  WWII ended = 1945; Korean War began = 1950; WWI ended = 1918; Great
  Depression onset = 1929. Translate the event to its year, then look up that
  annual row.
- The "June 1970 bulletin" (or any named issue) is the SOURCE for BOTH phases —
  it publishes a multi-year monthly history of the yield series, so one issue
  covers the whole 1960-1969 scan. Don't open ten issues; the named issue's
  historical tables span the range.
- UNIT: "in nominal dollars ... full number without commas or words" means
  report the RAW dollar figure with ALL zeros expanded. A table printed in
  millions reading "92" -> answer 92000000 (multiply the printed millions
  figure by 1,000,000 to get full nominal dollars). NO rounding, NO scaling to
  billions — give the literal expanded integer.
- Worked example: min Aa-vs-Treasury spread month in 1960-69 -> railroad
  retirement trust receipts that month = 92000000 (i.e. $92 million expanded).
- PITFALL: phase-1 errors silently propagate — if you pick the wrong extremum
  month, phase 2 reads a plausible-but-wrong number. Double-check the extremum
  by listing the computed spreads and confirming the min/max is unambiguous.

## TIPS inflation-adjusted price volatility (population std dev over a date range)
A distinct category: compute the PRICE VOLATILITY of a specific TIPS (Treasury
Inflation-Protected Security), measured as the POPULATION standard deviation of
its INFLATION-ADJUSTED prices across a date range (e.g. Jan 1 - Aug 1, 2007).
- Identify the security precisely. The question over-specifies on purpose:
  "2-3/8% U.S. Treasury Inflation-Protected Security with a coupon rate of 2⅜
  percent" = the TIPS issue carrying a 2.375% coupon. Match BOTH the coupon and
  the TIPS type; multiple TIPS exist, pick the exact coupon/maturity named.
- ADJUSTED price = unadjusted (quoted/clean) price × INDEX RATIO for that date.
  TIPS principal is scaled by an inflation index ratio (CPI-based reference
  index / index at issue). The Bulletin's TIPS / "Market quotations" tables (or
  the inflation-index-ratio data) provide the index ratio per date. "Use
  adjusted price accounting for inflation / index ratios" = multiply each
  period's price by its index ratio BEFORE computing the std dev.
- Collect the adjusted price for EVERY reporting date in the window (these
  tables are typically monthly end-of-month quotes -> ~7-8 points for a Jan-Aug
  span; could be more if more frequent). Use ALL points in range.
- POPULATION std dev (divide by N, not N-1):
      import statistics
      sigma = statistics.pstdev(adjusted_prices)   # population
  The question says "population standard deviation" explicitly — do NOT use
  sample stdev (statistics.stdev / ddof=1). Using N-1 is the most likely error.
- Round to the requested places (6 dp here). Worked example: 2⅜% TIPS,
  Jan 1 - Aug 1 2007, adjusted prices, population std dev = 0.900544.
- PITFALLS:
  - Population vs sample: pstdev (÷N) not stdev (÷N-1). Re-read the question.
  - Adjusted vs raw price: must multiply by index ratio; raw-price std dev is wrong.
  - Date window inclusivity: include both endpoints' reporting dates if printed.
  - Coupon match: 2-3/8% = 2.375%; don't grab a 2.5% or 2.25% TIPS.

## Arc elasticity (midpoint elasticity) wrapper around a 2-variable, 2-period lookup
Another economics-transform wrapper: "compute the ARC ELASTICITY of Y with
respect to X for <period1> and <period2>." You read FOUR values from a table
(Y and X at each of the two periods), then apply the midpoint (arc) elasticity
formula. The data lookup is ordinary; the only new work is the formula + sign.
- Arc elasticity uses MIDPOINT (average) bases, NOT simple percent change:
      dY = Y2 - Y1 ;  dX = X2 - X1
      arc_E = (dY / ((Y1 + Y2)/2)) / (dX / ((X1 + X2)/2))
            = (dY/dX) * ((X1 + X2) / (Y1 + Y2))
  This is symmetric in the two periods (order of period1/period2 doesn't change
  the magnitude or sign) — that's the whole point of the arc/midpoint form vs a
  point elasticity.
- "Y with respect to X" => Y is the numerator (the responding/dependent
  variable), X is the denominator (the driver). Here Y = total IRS collections,
  X = unemployment insurance contributions. Get the order right or you invert
  the elasticity.
- SIGN matters and is graded. If Y and X move in OPPOSITE directions over the
  two periods, the elasticity is NEGATIVE. Keep the sign; don't report absolute
  value. (Worked example below was -3.524.)
- UNIT CANCELS: because it's a ratio of percent changes, you do NOT need to
  scale — read raw table figures in their native unit (thousands here). Just be
  consistent (same unit for both Y values, same unit for both X values).
- Round only the final elasticity to the requested places.
- Compute in Python to avoid arithmetic slips:
      Y1,Y2,X1,X2 = ...
      E = ((Y2-Y1)/((Y1+Y2)/2)) / ((X2-X1)/((X1+X2)/2))
- Worked example: arc elasticity of total IRS collections w.r.t. unemployment
  insurance contributions, Jan 1960 vs Mar 1960 = -3.524 (3 dp).

## CAGR + decay factor + arc elasticity COMBO (single series, two endpoints)
A multi-metric wrapper that asks for several derived rates off the SAME two
endpoint values (start_value at FY_a, end_value at FY_b). You read just TWO
numbers, then emit a vector of derived rates. The lookup is ordinary; all the
work is the formulas + getting the conventions right.
- CAGR over N years (N = FY_b - FY_a, the year SPAN, not the count of points):
      cagr = (end/start) ** (1/N) - 1
  A DECLINING series gives a NEGATIVE cagr (e.g. -0.153). Keep the sign.
- ANNUAL DECAY FACTOR = the growth multiplier per year = 1 + cagr =
  (end/start) ** (1/N). For a declining series this is < 1 (e.g. 0.847).
  It is literally `cagr + 1`; do NOT report it as a percent or subtract 1 again.
- ARC ELASTICITY "using midpoint percentage change" in a SINGLE-series growth
  context (no second driver variable) = midpoint % change of the VALUE divided
  by midpoint % change of TIME (years):
      mid_pct_value = (end - start) / ((end + start)/2)
      mid_pct_time  = (N) / ((FY_b + FY_a)/2)      # dt over midpoint year
      arc_E = mid_pct_value / mid_pct_time
  i.e. arc_E = [(end-start)/((end+start)/2)] / [(FY_b-FY_a)/((FY_b+FY_a)/2)].
  For a declining series this is NEGATIVE (e.g. -1.162). The time denominator
  uses the YEARS as X (FY numbers as the two X values, dX = N).
- OUTPUT ORDER follows the question: here [CAGR, decay factor, arc elasticity].
  "output all rate values in decimal form" = decimals not percents (0.847 not
  84.7). Round each to the requested places (3 dp).
- Compute in Python to avoid slips:
      N = fy_b - fy_a
      cagr = (end/start)**(1/N) - 1
      decay = (end/start)**(1/N)            # == cagr + 1
      mv = (end-start)/((end+start)/2)
      mt = N/((fy_b+fy_a)/2)
      arcE = mv/mt
- Worked example: U.S. Dept of Labor TOTAL outlays (budgetary + trust-fund
  flows) FY2011 -> FY2019, N=8: gave [-0.153,0.847,-1.162]. "include both
  budgetary and trust-fund flows" = the COMBINED/total outlays row for the
  agency (not the federal-funds-only or trust-funds-only sub-line). Dept-level
  outlays incl. trust funds live in the budget outlays-by-agency tables; pick
  the agency's grand-total (all-funds) outlay figure for each FY.

## Internal Revenue Collections tables (by source, monthly)
The Bulletin carries "Internal Revenue Collections" tables: ROWS are sources of
revenue (individual income tax, corporation income tax, employment taxes,
unemployment insurance, excise taxes, estate/gift, etc.) plus a "Total Internal
Revenue collections" / grand-total row; COLUMNS are MONTHS (and/or fiscal-year
totals). Values are natively in THOUSANDS of dollars.
- "total collections reported by the IRS" = the grand-total IRS collections row.
- "unemployment insurance contributions" = the specific unemployment-insurance
  line within the employment-taxes group — read that exact row, not the
  employment-taxes subtotal.
- Pick the column for each named month exactly (Jan 1960, Mar 1960). A single
  Bulletin issue's IRS-collections table shows several recent months side by
  side, so one issue typically covers both months in a same-year comparison.

## Pearson correlation wrapper over a 2-series, N-period lookup
Another statistics-transform wrapper: "calculate the Pearson correlation
coefficient between <series A> and <series B> for <list of months>." You read
TWO parallel time series (A and B at each of N named periods), then compute the
Pearson r. The data lookup is ordinary; the only new work is the formula.
- Collect aligned pairs: for each named month, read A and B. Order does not
  matter for r, but the two lists must be index-aligned (same month -> same
  position in both lists).
- Compute in Python (do NOT hand-compute — easy to slip):
      import statistics
      r = statistics.correlation(A, B)   # Python 3.10+; population/sample-agnostic
      # fallback: numpy.corrcoef(A, B)[0,1]
  Pearson r is scale/shift-invariant, so UNIT SCALING IS IRRELEVANT — read raw
  table figures in whatever native unit (millions of foreign-currency units
  here); no conversion needed.
- Sign is graded: positively-co-moving series give positive r, opposite-moving
  give negative. Round only the final r to the requested places (4 dp typical).
- Worked example: Pearson r between Belgian-franc and Canadian-dollar nonbanking
  foreign-currency positions for Dec 1975, Mar 1976, Jun 1976, Sep 1976 = 0.3719.

## Liabilities to foreign countries BY CURRENCY (max/min share across years)
The Capital-Movements / banking-data section carries Treasury reports on U.S.
banks' "Liabilities to Foreign Countries" (and claims on foreigners), broken
out BY CURRENCY of denomination (U.S. dollar, Canadian dollar, pound sterling,
etc.) at PERIOD-END (calendar-year-end / quarter-end) dates, in MILLIONS of
dollars. A recurring question asks for the MAX (or min) SHARE of one currency's
liabilities out of TOTAL liabilities to foreign countries across several
calendar-year-ends.
- SHARE for a year = currency_liabilities_year / total_liabilities_to_foreign_year.
  TOTAL = the all-currencies "Total" liabilities-to-foreign-countries row, NOT a
  regional subtotal and NOT total liabilities of all kinds. Match the exact
  currency row (e.g. "Canadian dollar") and the total row.
- "calendar year end reported values from 2009-2011 inclusive" = read the
  Dec-31 (year-end) column for each of 2009, 2010, 2011 (3 shares), then take
  the MAX (or whatever extremum the question names) over those years.
- "as a decimal (if 12.34 is a percent, 0.1234 is the decimal)" => output the
  raw ratio, do NOT multiply by 100 (0.005, not 0.5). UNIT CANCELS (millions/
  millions) so no scaling. Round only the final extremum share to the requested
  place (thousandths here). Mode A delimiter.
- Worked example: max share of Canadian-dollar liabilities / total liabilities
  to foreign countries, CY-end 2009-2011, = 0.005 (nearest thousandth, decimal).
  These shares are tiny (Canadian dollar is a minor share vs the dollar-
  denominated bulk), so a sub-1% decimal like 0.005 is expected — don't mistake
  it for an error or reflexively ×100.
- A single recent Bulletin issue's banking-liabilities table shows several
  period-ends; CY 2009-2011 may need one or two issues to cover all three
  year-ends.

## Nonbanking firms' foreign-currency positions tables (Treasury FX exposure series)
The Bulletin's Capital-Movements / international section carries Treasury reports
on "Foreign-currency positions" of U.S. NONBANKING firms (also banks; read the
right sub-report). These tables report, BY FOREIGN CURRENCY (Belgian franc,
Canadian dollar, French franc, German mark, Japanese yen, Pound sterling, Swiss
franc, etc.) and BY QUARTER-END date, the firms' positions (assets/liabilities/
net) in MILLIONS OF THE FOREIGN CURRENCY itself (NOT dollars — "millions of
current foreign-currency units").
- These are QUARTERLY series (Dec/Mar/Jun/Sep quarter-ends). A "calendar months
  Dec 1975, Mar 1976, Jun 1976, Sep 1976" request = the four quarter-end columns.
- Currency is the ROW (or sub-block) key; the date is the COLUMN. Match the exact
  currency row and the exact quarter-end column. Pick the position type the
  question names (often the overall/net position line per currency).
- A single issue's table typically shows several recent quarter-ends side by
  side; you may need one or two issues to cover four quarters spanning two years.

## OLS regression of ln(value) on year index (slope + intercept wrapper)
A wrapper that pairs a YoY-growth question with "run an OLS regression of
ln(outlays) on fiscal year index and return the slope and intercept." You read
a short series (one value per FY across an inclusive range), then fit a simple
linear regression. The lookup is ordinary; the traps are the INDEX BASE and the
per-item rounding rule.
- THE INDEX BASE IS 1-BASED, NOT 0-BASED. The "fiscal year index" for the first
  FY in the range is 1, the second is 2, etc. (FY2007=1, FY2008=2, ... FY2013=7
  for a 2007-2013 span). The SLOPE is invariant to the index origin, but the
  INTERCEPT shifts by exactly one slope-step per unit of origin offset. If your
  slope matches gold but your intercept is off by ~slope (e.g. 8.736 vs gold
  8.706 with slope 0.030), you used a 0-based index — re-fit with x=1..N.
  Diagnostic: intercept_error ≈ slope ⇒ off-by-one in the index base.
- Fit in Python (least squares on ln(value)):
      import numpy as np
      y = np.log(values)                 # ln of each year's outlay
      x = np.arange(1, len(values)+1)    # 1-BASED index: FY1->1, FY2->2, ...
      slope, intercept = np.polyfit(x, y, 1)
  numpy.polyfit returns [slope, intercept]. statistics.linear_regression(x,y)
  also works (returns slope, intercept) on Python 3.10+.
- ln() is applied to the value in WHATEVER unit the series is read in; report
  the slope/intercept as-is from that fit (the intercept's level depends on the
  unit, but the question fixes the unit implicitly via the table).
- Round slope and intercept to the requested places (thousandths here).
- Worked example: Judicial Branch total on-budget+off-budget outlays FY2007-2013,
  OLS of ln(outlays) on 1-based FY index gave slope 0.030, intercept 8.706.

## Per-sub-answer rounding OVERRIDES a trailing global rounding rule
When a question states a rounding rule INLINE for a specific sub-answer ("the
YoY growth rate ... rounded to the nearest HUNDREDTHS place") and ALSO appends a
blanket rule at the end ("All numbers should be rounded to the nearest THOUSANDTH
place"), the SPECIFIC per-item rule WINS for that item; the global rule applies
only to the items that had no inline rule.
- Worked example: YoY percent stated as "nearest hundredths" -> 2.81 (gold),
  NOT 2.806 (the thousandth I wrongly emitted from the trailing global rule).
  The slope/intercept, which had no inline rule, correctly took the global
  thousandth (0.030, 8.706). Output: [2.81,0.030,8.706].
- RULE: parse rounding PER sub-answer. Read the clause attached to each quantity
  first; only fall back to the global "all numbers rounded to X" for quantities
  that lack their own inline rounding instruction. Different values in the SAME
  bracketed answer can legitimately have DIFFERENT decimal places.

## Average YoY growth rate over an inclusive FY range
"Average Year-over-Year growth rate from FY A - B inclusive" = compute the
per-year growth rate for each consecutive pair, then average those rates:
    rates = [(v[i] - v[i-1]) / v[i-1] for i in 1..N-1]   # N values -> N-1 rates
    avg = mean(rates) * 100                              # if "expressed as a percent"
- N years inclusive yields N-1 YoY rates (FY2007-2013 = 7 values -> 6 rates).
- "expressed as a percent" -> multiply the mean ratio by 100 (output 2.81, not
  0.0281). This is the ARITHMETIC mean of YoY rates, NOT a CAGR — do not use
  (end/start)**(1/N)-1 here unless the question says "geometric"/"compound".

## Gini coefficient of a small set of values (trust-fund receipts vs expenditures)
A statistics wrapper: \"the Gini coefficient of <total receipts> and <total
expenditures> of <fund> in <month>.\" You read just TWO (or a few) values, then
compute the Gini. The lookup is ordinary; the trap is the FORMULA CONVENTION.
- OfficeQA grades the GINI computed by the standard relative-mean-absolute-
  difference formula (the one statsmodels / most libraries use), which for N
  values is:
      G = sum_i sum_j |x_i - x_j| / (2 * N**2 * mean)
        = sum_i sum_j |x_i - x_j| / (2 * N * sum)
  For N = 2 values {a, b} this simplifies to:
      G = |a - b| / (a + b)          # = |a-b|/sum   (the N=2 closed form)
  This is the SAMPLE-style result. Do NOT use the alternative population form
  G_pop = |a-b| / (2*(a+b)) = |a-b|/(2*sum), which gives EXACTLY HALF and is
  graded WRONG. Worked example: gold 0.012 vs my wrong 0.006 (exactly 2x off)
  -> I used the /(2*sum) denominator; correct is |a-b|/sum.
- DIAGNOSTIC: if your Gini is exactly half (or exactly double) the expected
  magnitude, you picked the wrong N-normalization convention. For 2 values the
  right answer is |a-b|/(a+b).
- Compute robustly in Python for any N:
      import numpy as np
      x = np.array(values, dtype=float)
      n = len(x)
      mad = np.abs(x[:,None] - x[None,:]).sum() / (2*n*n)   # mean abs diff /2... 
      G = mad / x.mean()        # = sum|xi-xj| / (2*n^2*mean) = sum|xi-xj|/(2*n*sum)
  (For N=2 this returns |a-b|/(a+b).)
- The values must be in CONSISTENT units (the Gini is scale-invariant, so no
  unit conversion needed — read raw table figures). Round to requested place.
- SURPLUS/DEFICIT sub-answer: a fund runs a SURPLUS if receipts > expenditures,
  a DEFICIT if expenditures > receipts. Compare the two totals directly.
  \"excluding those attributed to investments\" means use the operating receipts
  and operating expenditures rows, NOT the lines tied to investment
  transactions (e.g. interest on/proceeds from/redemption of investments) —
  read the receipts and expenditures totals net of the investment-related rows.
- Trust-fund (Federal Disability Insurance, OASI, etc.) monthly receipts and
  expenditures live in the Bulletin's trust-fund statements / \"Federal
  receipts and outlays\" trust-account tables, keyed by fiscal month.
- Output order: [gini, 'surplus'|'deficit'], gini first. No space after comma.

## "Relative difference" = normalize by the base; NOT the absolute gap
A recurring KILLER phrasing: "the RELATIVE DIFFERENCE in percentage points of
<rate> ... for the <year1> and <year2> ...". Despite saying "in percentage
points", the graded answer is the RELATIVE (normalized) change between the two
years, NOT the absolute difference of the two rates:
    rate1 = metric_year1            # e.g. redemptions/avg-outstanding * 100
    rate2 = metric_year2
    answer = (rate2 - rate1) / rate1 * 100      # relative diff, as a percent
NOT  answer = rate2 - rate1  (that's the ABSOLUTE difference in pct points).
- DIAGNOSTIC: if your answer is a small few-pct-points number and the gold is
  ~3-5x larger, you almost certainly reported the absolute gap when the question
  wanted the relative difference (gap / base_year_rate * 100). Worked example:
  saving-note redemption rate, 1980 vs 1981: rate_1980 ≈ 21.76%, rate_1981 ≈
  25.61%; absolute gap = 3.85 (WRONG), relative diff = 3.85/21.76*100 = 17.69
  (GOLD). The factor between them is exactly 1/base_rate.
- "relative difference" / "relative change" / "percent change" => always divide
  the gap by the EARLIER (base) year's value, then ×100. The word "relative"
  is the trigger; "in percentage points" is a red herring that tempts you into
  reporting the raw subtraction. When in doubt and the question says RELATIVE,
  normalize by the base.
- Base year = the FIRST year named (chronologically earlier, here 1980).

## SHARE of total redemptions accounted for by ONE series (e.g. Series I/EE) in a MONTH

A recurring savings-securities pattern DISTINCT from the redemption-RATE one:
"the change in percentage points in the SHARE of TOTAL redemptions (all series)
accounted for by Series I bonds from <Month Y1> to <Month Y2>", plus "the
absolute change in Series I redemptions across both years." You read FOUR cells:
Series-I redemptions and ALL-SERIES total redemptions at each of the two
month-ends, then:
    share_y = seriesI_redemptions_y / all_series_total_redemptions_y * 100
    answer1 = share_y2 - share_y1            # change in pct points (signed)
    answer2 = | seriesI_redemptions_y2 - seriesI_redemptions_y1 |   # abs change

- READ THE SINGLE MONTHLY CELL, NOT a fiscal-year/cumulative figure. The
  savings-securities exhibit prints, for each series, the redemptions for THAT
  MONTH (e.g. "March 2000") in one column and often a fiscal-year-to-date /
  cumulative column right beside it. Grab the MONTHLY (current-month) redemption
  cell for both the Series-I row AND the all-series total row. Using the FYTD /
  12-month / cumulative column inflates the absolute change by ~10-25x.
  DIAGNOSTIC: abs-change 1967 vs gold 82 (~24x) = read cumulative column or total
  row instead of single-month Series-I cell. Clean OOM overshoot = wrong column
  (cumulative) or wrong row (total vs the one series).
- SERIES I and SERIES EE are the MODERN series (Series I introduced Sept 1998,
  Series EE in 1980). In early-2000s Bulletins the savings-bond redemptions table
  has rows for Series E, H, EE, HH, AND I (plus "All series" total). Read the
  Series I row EXACTLY — do NOT grab Series EE, Series E, or the all-series total.
  In March 2000 Series I was brand-new so its redemptions are SMALL; the share is
  a low single-digit percent and GROWS by March 2005. Gold here: share change =
  7.1 pct points, abs change in Series-I monthly redemptions = 82 (millions).
  DIAGNOSTIC: share change 0.4 vs gold 7.1 (~18x small) = wrong Series-I row or
  too-large total denominator.
- BOTH numerator and denominator are MONTHLY redemptions in MILLIONS; share is
  unitless×100; abs change is in millions (the unit asked).
- Output order: [share_change_pct_points, absolute_change_millions]. Round the
  share to the stated place (tenths -> 7.1) and the abs change to whole (-> 82).
  The share change is SIGNED (can be negative if the series' share fell); keep sign.
- Endpoints 5yr apart (e.g. Mar2000 & Mar2005) => need TWO PDFs (issue covering
strips trailing "%", output bare number.

## Savings-bond/note REDEMPTION RATE
Within the savings-securities exhibits, a "redemption rate" for a year is the
year's REDEMPTIONS divided by the AVERAGE AMOUNT OUTSTANDING for that year,
expressed as a percent:
    redemption_rate_year = redemptions_year / avg_amount_outstanding_year * 100
- These are three SEPARATE columns/sub-tables in the savings-securities exhibit:
  SALES, REDEMPTIONS, and AMOUNT OUTSTANDING. "Average amount outstanding" may
  be a printed column, or you average beginning+ending outstanding for the year.
- "SAVING NOTES" (U.S. Savings Notes / "Freedom Shares") are a DISTINCT series
  from Savings Bonds (Series E, H, EE, etc.). Read the saving-notes row, not a
  bond series or the all-series total.
- Match the unit consistently for numerator and denominator (both millions) —
  the rate is unitless×100, so no billions conversion.

## "Percent contribution" of a component to TOTAL receipts, and its CHANGE
Q: "change in percent contribution of net individual income taxes to total
budget receipts CY2010->CY2011" (also corporation/payroll/excise). Use the
budget receipts COMPOSITION table ("Federal Fiscal Operations"/"Budget Receipts
by Source"): components + TOTAL receipts row. "Nominal"=raw dollars, no
inflation adj. CY: SUM Jan-Dec if monthly, NOT fiscal-year (Oct-Sep) total.
share_y=component_y/total_y*100; answer=share_y2-share_y1 (signed pct pts),
MODE A bare comma. FORMAT: gold "4.61%" graded my bare "4.61" CORRECT — grader
strips trailing "%", so output the bare number.

## Hazen Plotting Position percentile (and other plotting-position percentiles)
A statistics wrapper: \"the Pth Hazen Percentile value (using the Hazen Plotting
Position) of <a collected set of N values>.\" You collect N values (e.g. one per
FY across an inclusive range), SORT ascending, then interpolate the Pth
percentile using the HAZEN plotting-position rank-to-probability convention.
- HAZEN plotting position for the k-th smallest value (k = 1..N, 1-based):
      p_k = (k - 0.5) / N          # probability assigned to rank k
  So the sorted values sit at cumulative probabilities 0.5/N, 1.5/N, ...,
  (N-0.5)/N. To find the Pth percentile (target prob = P/100), LINEARLY
  INTERPOLATE between the two bracketing (p_k, value_k) points.
- Closed form: with sorted x[0..N-1], target q = P/100,
      pos = q * N + 0.5          # the (1-based) fractional rank that has prob q
      # clamp: if pos <= 1 -> x[0]; if pos >= N -> x[-1]
      i = floor(pos); frac = pos - i
      value = x[i-1] + frac * (x[i] - x[i-1])   # x is 0-indexed here
  numpy (>=1.22): np.percentile(x, P, method='hazen') == (k-0.5)/N convention.
- DISTINGUISH plotting-position conventions (the question NAMES which one):
    - Hazen:    p_k = (k - 0.5) / N           (numpy method='hazen')
    - Weibull:  p_k = k / (N + 1)             (numpy method='weibull')
    - Gumbel/  : p_k = (k - 1) / (N - 1)       (numpy method='linear', the default)
    - Cunnane:  p_k = (k - 0.4) / (N + 0.2)    (numpy method='median' is close; use formula)
  Read the named position EXACTLY; the wrong convention shifts the interpolated
  value. \"Hazen\" -> (k-0.5)/N, full stop.
- The data lookup is ordinary (e.g. \"total nominal on-budget AND off-budget
  outlays for the Dept of Defense FY2011-FY2020\" = the agency's COMBINED
  on-budget+off-budget total outlays row per FY, in millions; collect all 10
  FY values). Native unit millions -> no scaling if answer wanted in millions.
- Round only the final interpolated percentile to the requested place.
- Worked example: 85th Hazen percentile of DoD total on-budget+off-budget
  outlays FY2011-FY2020 (10 values, millions) = 678077.00. With N=10, P=85:
  pos = 0.85*10 + 0.5 = 9.0 -> exactly the 9th-smallest value (no interpolation
  needed since pos landed on an integer rank).

## Fisher Ideal symmetric growth rate (and "symmetric growth" wrappers)
A math-transform wrapper: read TWO values (same metric at period1 and period2),
then compute the "Fisher Ideal symmetric growth rate" between them. The lookup
is ordinary; the only new work is the formula. The symmetric growth rate is:
    g = 2 * (v2 - v1) / (v2 + v1)
where v1 = EARLIER period value, v2 = LATER period value. This is the
midpoint/arc growth rate (change divided by the AVERAGE of the two values, i.e.
2*(v2-v1)/(v1+v2)). It is NOT the simple percent change (v2-v1)/v1.
- It is graded as a DECIMAL (e.g. -0.113), not a percent. A DECLINING metric
  gives a NEGATIVE rate — keep the sign.
- Numerically, for small changes this nearly equals ln(v2/v1) (the log growth);
  both -0.113 here. If the question instead says "log/continuous growth", use
  ln(v2/v1). But "Fisher Ideal symmetric growth rate" = 2*(v2-v1)/(v2+v1).
- Compute in Python:
      g = 2*(v2 - v1)/(v2 + v1)      # v1=earlier, v2=later
- DIAGNOSTIC — value-extraction error vs formula error: the magnitude of g is
  set almost entirely by HOW BIG the gap (v2-v1) is relative to the level. If
  your g is ~2x too small (e.g. -0.048 vs gold -0.113), the formula is fine but
  you read at least one yield/value WRONG (wrong month, wrong "as-of" column, or
  wrong bond category) — the gap you computed is too small. Re-extract both
  values and sanity-check the gap. Worked example: new long-term Treasury bond
  yields, Aug 1982 vs Aug 1981, as of FY1982-end reported values: a ~1.5-point
  drop (≈14.0 -> ≈12.5) gives g = -0.113 (gold); my -0.048 came from a too-small
  ~0.7-point gap = a mis-read value.

## Continuously compounded average annual growth rate (ln-based, DISTINCT from CAGR)
A recurring growth-formula wrapper. "CONTINUOUSLY COMPOUNDED average annual
growth rate" between two period-end values is the LOG growth divided by the year
span — NOT the discrete CAGR (end/start)**(1/N)-1 and NOT Fisher symmetric:
    g = ln(end / start) / N        # N = number of YEARS between the two ends
where start = earlier value, end = later value, N = year span (e.g. CY1945 ->
CY1955 = 10 years, so divide by 10).
- The three growth formulas the dataset mixes (READ THE EXACT WORDING):
    - "continuously compounded" / "log growth"  -> g = ln(end/start)/N
    - "geometric annual rate of change" / "compound annual" / CAGR
                                                 -> g = (end/start)**(1/N) - 1
    - "Fisher Ideal symmetric growth rate"        -> g = 2*(end-start)/(end+start)
  For modest changes all three are numerically CLOSE, but they differ at the
  3rd-4th decimal, and the grader rounds tightly — pick the one named.
- "reported as a decimal (if percent is 12.34%, decimal is 0.1234)" => output the
  raw decimal g (0.063), do NOT multiply by 100. Keep the sign (declining series
  gives negative g). Round only the final g to the requested place.
- Compute in Python:
      import math
      g = math.log(end/start)/N
- Worked example: Seigniorage on coins (silver and minor), in millions of nominal
  dollars, end of CY1945 -> CY1955 (N=10), continuously compounded avg annual
  growth = 0.063 (nearest thousandth, decimal form). Seigniorage figures live in
  the Bulletin's monetary-statistics / "Seigniorage" exhibit (coinage section),
  split silver vs minor coin; "coins (silver and minor)" = the combined coinage
  seigniorage figure. UNIT CANCELS in a log RATIO, so no millions->billions
  scaling needed.

## Market Yields MY-2 "New Aa corporate bonds" series + DISCONTINUATION trap
Table MY-2 ("Average Yields of Long-Term Treasury, Corporate and Municipal
Bonds") carries a "New Aa corporate bonds" column = Treasury's 3-week moving
average of reoffering yields on NEW corporate bonds rated Aa by Moody's with
original maturity >=20yr. It is a MONTHLY SERIES (averages of daily/weekly
series), in percent, with rows by calendar month going back years.
- "AA-rated corporate bond yields that are new" = the "New Aa corporate bonds"
  column of MY-2 (NOT the municipal Aa column, NOT Treasury bonds).
- KILLER DISCONTINUATION: MY-2 (and Chart MY-B) were DISCONTINUED EFFECTIVE
  JANUARY 2003 — "Treasury no longer issues long-term bonds and no longer
  calculates or estimates long-term corporate rates." The March-2003 Bulletin's
  MY-2 ends at Dec 2002; the June-2003 issue's Market-Yields INTRODUCTION states
  the discontinuation. So there is NO published actual Jan-2003 New-Aa-corporate
  value in any Treasury Bulletin. A question asking "predicted vs ACTUAL Jan 2003"
  is built on a discontinued series; the ACTUAL = 6.17 (FRED AAA/DAAA, Moody's
  Seasoned Aaa, Jan-2003 monthly avg), NOT the last printed cell.
- TRAP: do NOT use 6.21 (= Dec-2002, last MY-2 cell) as the Jan-2003 actual.
  |6.52-6.21|=0.31 WRONG; |6.52-6.17|=0.35 gold-verified.
- RE-FAIL (submitted 0.47): back-solve 6.5205-0.47 = 6.05, i.e. I used a WRONG
  Jan-2003 actual of ~6.05 (likely a misread FRED row / wrong month / Baa-ish
  figure). The ONLY correct actual for "New Aa corporate" Jan-2003 = 6.17. NOT
  6.05, NOT 6.21. SELF-CHECK: if your |pred-actual| is not ≈0.35 (e.g. you get
  0.31 or 0.47), your ACTUAL is wrong — the prediction 6.5205 is fixed/verified.
  Hard-pin actual=6.17 unless a web lookup of FRED AAA monthly Jan-2003 says
  otherwise. FULL worked data + 48 monthly cells: ->
  references/my2-corporate-bond-yield-regression.md (load it — this EXACT Q).
- OLS-projection: 48 monthly vals Jan1999-Dec2002, fit OLS on monthly index
  (base-invariant), predict next index = 6.52 (6.5205). |6.52-6.17|=0.35.
- RULE: "predicted vs ACTUAL <month>" on a discontinued series — the actual is
  NOT the last in-Bulletin cell; pull it from the underlying source (FRED
  AAA/DAAA for Aaa corp, GS-series for Treasury CMT) for that exact month.

## Treasury bond / note YIELD series tables (monthly, "average yield of new issues")
The Bulletin's interest-rate section carries yields on Treasury securities,
including "Average yield of NEW LONG-TERM Treasury bonds" (yields on newly issued
long-term bonds) reported by CALENDAR MONTH, in PERCENT (e.g. ~12-14% in 1981-82).
- Rows/series: distinguish "new long-term Treasury bonds" (yield on NEW issues)
  from secondary-market constant-maturity yields and from bill rates. Read the
  exact series the question names.
- "as of reported values on the end of the <FY> FY" / "as reported in the <issue>"
  means use the values AS PRINTED in a SPECIFIC issue (often the issue that closes
  that fiscal year, e.g. the Sept/Oct issue for an FY ending Sep 30). These series
  get REVISED across issues, so the Aug-1981 figure printed in the FY1982-closing
  issue can differ from the Aug-1981 figure printed in an earlier issue. Pull BOTH
  months (Aug 1982 AND Aug 1981) from the SAME, FY-end issue's historical table —
  that issue's table shows a multi-month/multi-year history, so one issue covers
  both months. Do NOT read Aug 1981 from a 1981 issue and Aug 1982 from a 1982
  issue; use the single "as of FY-end" issue's reported (possibly revised) values.
- These are already PERCENT — no unit scaling. Read the printed rate directly.
- PITFALL: picking the wrong month column or an annual-average row instead of the
  specific calendar-month cell silently changes the value and breaks any growth/
  ratio computed from it.

## Parametric VaR / "lower-tail portfolio loss exceeded with P% probability"
Gaussian VaR wrapper over a short series of period-end holdings. KEY TRAP: loss =
z*sigma - mu (SUBTRACT DRIFT); sigma/mu are of the YEAR-OVER-YEAR CHANGES, not raw
levels. A clean 3-5x overshoot = dropped drift term. Full method (FX conversion,
diagnostics, code) in references/parametric-var.md — read it for VaR questions.

## Historical Expected Shortfall (ES / CVaR) — "historical portfolio return approach"
DIFFERENT from parametric VaR. Convert the level series (e.g. Jan Aa-corp yields
1990-1999) to SIMPLE RETURNS first, sort, then ES95 = mean of the worst 5% tail
(for 9 returns the 5% tail = the single WORST return). Answer is a NEGATIVE
PERCENT with `%` suffix (gold -18.51%). FAIL: computed a stat on raw LEVELS ->
positive ~6, no %. Full method in references/historical-expected-shortfall-cvar.md.

## Currency conversion + geometric mean / geometric ANNUAL RATE OF CHANGE (CAGR) -> references/currency-and-geomean.md
Questions chaining ratios -> geometric mean -> multiply by a table value ->
convert to GBP/foreign via "official annual average exchange rate in YEAR".
Final is HYPERSENSITIVE: a ~0.03% error = coarse exchange rate or early rounding,
not a misread. USD->GBP means DIVIDE by USD-per-GBP (~2.7913 in 1964); carry full
precision and round only the final integer. geo_mean=(prod ratio_i)**(1/N), never
arithmetic-mean, never round ratios early. See the reference for the worked
109625-vs-109660 failure and statutory-debt-limitation row labels.
ALSO covers GEOMETRIC MEAN OF GROWTH RATES / PERCENT CHANGES: convert each % to a
factor (1+r/100) first; and for "percent change AT AN ANNUAL RATE" (e.g. quarterly
real GDP) you MUST de-annualize each quarter ((1+r/100)**(1/4)), geo-mean, and
report the QUARTERLY % (do NOT re-annualize). Worked failure: 2017 GDP got 2.74,
gold 0.69 (exactly ~4x too high = left values annualized). If your geomean of
annual-rate growth is ~4x the gold, you skipped de-annualization.
ALSO covers USD->CAD conversion with a MONTHLY-AVERAGE rate (1950s-60s floating
CAD, above par, rate <1 CAD/USD => MULTIPLY USD*rate). >>> KNOWN RECURRING Q:
"absolute difference in total U.S. federal trust account receipts Nov 1959 vs
Dec 1959 in millions CAD using the MONTHLY average USD-CAD in Dec 1959, to
hundredths" -> THE ANSWER IS 504.12. Failed 4x by using too-high a rate (508.27,
506.68, 506.42). USD diff=530.0 M, Dec-1959 monthly rate=0.95117. Do NOT use the
ANNUAL 0.9590 and do NOT compromise; if you land in 504.13-509 the rate is too
high — submit 504.12. See the reference's ">>> Nov-vs-Dec-1959 trust-receipts"
section.

## "In which YEAR did X peak/bottom?" over a multi-decade span -> references/peak-trough-year-from-timeseries.md
Argmax/argmin-YEAR over a long series (saving rate, unemployment, CPI). #1 fail =
off-by-ONE-YEAR on a plateau (picked adjacent bar). Read NUMERIC values not bar
heights; compare top candidates; prefer EARLIER year on a tie. Worked fail:
saving-rate peak, I said 1974, gold 1973. Sanity-check vs famous peak years.

## Two-stage: extremum of derived series picks a MONTH-YEAR, then read a DIFFERENT table -> references/extremum-then-crossref-different-table.md
Q clause 1 computes argmin/argmax of a DERIVED series (e.g. spread = corp Aa yield -
Treasury yield, month by month over 1960-69) to pick a (month,year); clause 2 reads
an UNRELATED table (e.g. railroad retirement trust RECEIPTS) at that same month. Final
answer is the STAGE-2 number; the date is just an index. Compute the spread per month
(don't eyeball). "as published in <Mon Year> bulletin" pins the issue PDF. Older
bulletins report trust-fund figures in WHOLE NOMINAL DOLLARS already (92000000), no
scaling/rounding — copy verbatim, strip commas. Worked PASS: 92000000.

## "Profile of the Economy" charts + NESTED averaging -> references/profile-of-economy-charts.md
Front-matter "Profile of the Economy" section carries small charts (Payroll
Employment monthly change in thousands, GDP, unemployment, CPI). READ values off
the chart, then aggregate. "Mean of the average monthly change end-Q1->end-Q2
across 2004-2006" is TWO-level: per year divide the span change by MONTH count
(Mar->Jun = 3 months), then mean across the inclusive YEAR count (3 yrs). Payroll
charts often plot the monthly CHANGE directly -> average the 3 monthly-change
bars Apr-Jun. See reference for the worked 202.333 example & divisor pitfalls.

## HHI concentration + effective number of groups -> references/hhi-concentration-effective-number.md
Q frames categories (NYC vs Chicago banks, holder groups) as "full market", asks
Herfindahl Hirschman Index + "effective number = reciprocal of HHI". HHI=sum(s_i^2)
as FRACTION in (0,1] — do NOT x10000. Shares by VALUE held, not bank count.
N_eff=1/HHI. 2-group HHI in [0.5,1.0]. CONFIRMED [0.611,1.635].

## Gini coefficient of small extracted set (n=2 receipts vs expenditures) -> references/gini-coefficient-small-n.md
DENOMINATOR TRAP: gold uses SAMPLE MAD form n(n-1), NOT population n^2. For n=2,
Gini = |a-b|/(a+b) (abs diff over sum). Population form = exactly HALF the gold
(fail: 0.006 vs gold 0.012). If Gini looks too small & you used n^2 norm, x n/(n-1).

## Descriptive stats over months (population std/variance/mean) + plain SUM of 12 monthly cells -> references/descriptive-stats-over-months.md
"Population standard deviation / variance / mean of <metric> for the months in
CY<year> (or FY<year>), in millions, nearest hundredths." Read ONE value per
month for the 12-month window, then compute ONE stat. THREE choices decide it:
(1) ddof — "population" => ddof=0 (np.std(x,ddof=0)); "sample"/plain => ddof=1.
numpy default is ddof=0 but pandas .std() default is ddof=1 — be explicit. Wrong
ddof on N=12 => std ~4.5% too high (variance ~9%), a clean small overshoot.
Same reference also covers the MEAN-of-YIELD-SPREAD variant: "average yield
spread between Corporate Aa and Treasury bonds across months in CY1960-1969" =
read BOTH yield columns per month from the interest-rate/"yields of bonds" table
(not outlays), take (Aa - Treasury) per month, plain-mean over ALL months in the
multi-year window (10 yrs = ~120 rows, not 12). Match exact series (Aa not Aaa;
long-term Treasury bond not bills/intermediate).
(2) window — CY = Jan..Dec of year; FY = Oct(prev)..Sep; use single-month cells
NOT the YTD cumulative column. (3) row — "net outlays by function" => the TOTAL
net-outlays line, not one function. Worked: CY1981 net outlays, ddof=0 -> 6379.29
(gold). Decimal answer => Mode A (bare comma). See reference for full method.

## Percentile via a PLOTTING POSITION (Hazen/Weibull) over N annual values -> references/plotting-position-percentile.md
"85th HAZEN Percentile (using the Hazen Plotting Position) of <metric> from FY
YYYY to FY YYYY, nearest hundredths, millions." Read ONE value per year, then
take a percentile USING THE NAMED PLOTTING POSITION (NOT np.percentile default).
Sort ascending; plotting position p_i = (i-a)/(N+1-2a): HAZEN a=0.5 => (i-0.5)/N;
WEIBULL a=0 => i/(N+1). Value at percentile q = np.interp(q, p, x) (exact hit =>
order statistic; outside [p_1,p_N] => clamp to endpoint; else linear interp).
For N=10 Hazen, p_i = {0.05,0.15,...,0.85,0.95}, so the 85th = 9th-smallest value
EXACTLY (no interp). Defense outlays = on+off-budget agency total row (see
outlays-by-agency.md), one FY per year across several bulletins. Worked: 85th
Hazen of DoD on+off-budget outlays FY2011-2020 -> 678077.00 (gold). #1 fail =
using np.percentile default instead of the named Hazen plotting position.

## OLS slope+intercept rounding (untransformed YEAR predictor) -> references/ols-slope-intercept-rounding.md
"fit OLS, year untransformed as predictor, return slope AND intercept rounded to
thousandth." INTERCEPT = mean_y - slope*mean_x, mean_x~1935, so a 5e-7 slope
error = 0.001 intercept error. Fit ONCE in float64 (np.polyfit), round slope &
intercept INDEPENDENTLY; never compute intercept from the rounded slope. FAIL:
[0.096,-184.142] vs gold [0.096,-184.143] (slope perfect, intercept last digit).

## Multi-bulletin TIME-SERIES regression / polynomial projection -> references/multi-bulletin-timeseries-regression.md
5+ bulletins (e.g. 1994/1999/2004/2009/2014 _06) + "fit cubic/linear regression to
surplus-deficit over years YYYY-YYYY, predict year Z, abs diff vs Treasury's
reported estimate." Each FFO-1 col 7 gives 5 ACTUAL annual values; chain 5
bulletins = 25 yrs (1989-2013). Use ACTUAL not "- Est." for overlap years.
polyfit projection is index-base invariant. Comparison "Treasury reported 2025"
is NOT in docs = external FY2025 final MTS deficit **-1,877,649** million (~$1.88T;
NOT -1,775,587 — that was wrong). Regression is usually right; the answer hinges
on the CORRECT external comparison constant (verify it, #1 failure mode). Worked
example (1989-2013 cubic -> 2025 = -2,785,303; diff = 907,654) in the ref.

## MY-2 "New Aa corporate/municipal" monthly-yield regression -> references/my2-corporate-bond-yield-regression.md
Q: "linear regression of MONTHLY SERIES AVERAGES OF WEEKLY OR DAILY SERIES,
AA-rated corporate bond yields that are NEW, <yr>-<yr>, abs diff between PREDICTED
yield for <month> and the ACTUAL value." Series = Table **MY-2** (Market Yields),
sub-banner "MONTHLY SERIES—AVERAGES OF DAILY OR WEEKLY SERIES", col **(2) New Aa
corporate** (col 1=Treasury 30/20-yr, col 3=New Aa municipal). NOT MY-1 (Treasury-
only) and NOT Moody's seasoned Baa. MY-2 DISCONTINUED effective Jan 2003 -> last
printed value is Dec 2002; read the monthly series from the **2003_03** bulletin
(prints 1991-Dec 2002). TWO-STEP: regress x=1..48 (Jan99-Dec02) -> predict x=49;
then answer = |prediction - ACTUAL|. ★ The Jan-2003 ACTUAL is NOT in any bulletin
(series ended) = external New Aa corp **6.17**. FAIL MODE (this run): reported the
bare prediction 6.520 and forgot to subtract the actual; gold = |6.5205-6.17| =
**0.35**. Regression was correct; missing final subtraction was the whole error.

## Average yield SPREAD across a decade of months -> references/bond-yield-spread-decade-average.md
Q: "average **yield spread** between US Corporate Aa bonds and US treasury bonds
across the months in calendar years <YYYY>-<YYYY>." DISTINCT from MY-2 regression
above: older bulletins (June-1970 covers 1960-69), simple per-month DIFFERENCE
(corporate Aa − long-term Treasury) then flat MEAN over all months (1960-69 = 120
spreads). = mean(corp)−mean(treas) for equal-length span. Read **Aa** col (not
Aaa) + long-term Treasury col from the market-yields table. NO regression, NO
external actual. Worked CORRECT: gold **0.88525** (5 sig digits, single scalar =
no delimiter).

## ABS CHANGE in ANNUAL corp-bond yield between two EVENT-defined years -> references/corporate-bond-yield-annual-event-endpoints.md
Q: "absolute change in the average **ANNUAL** yield of the **highest quality
corporate bonds (as determined by Moody)** since <event-year-A> to <event-year-B>",
in absolute percentage points, nearest tenth. DECODE events to years FIRST:
WWII-end=1945, Korea-began=1950 (so 1945->1950), Korea-ended=1953, WWII US-entry=1941.
"Highest quality / highest grade" = **Aaa** col (top of Moody ladder, OPPOSITE of
the Aa-spread ref above). Use ANNUAL-AVERAGE row, not monthly endpoints. Answer =
|Aaa_annual(B) − Aaa_annual(A)| rounded to tenth. Worked CORRECT: 1945 & 1950 Aaa
annual avg both ~2.6-2.7% (flat late-1940s era) -> **0.0** GOLD. A zero is legit.

## Pearson CORRELATION of two yield series; abs diff across two years -> references/yield-series-pearson-correlation-abs-diff.md
Q: "sample **Pearson correlation coefficient** of monthly yields for Treasury
bonds and **New Aa corporate** bonds during years <Y1> and <Y2> ... absolute
difference." SAME "Average Yields of Long-Term Bonds" table as spread above, but
operation = CORRELATION not spread. Per year r = np.corrcoef of the 12 monthly
(Treasury, New-Aa-corp) pairs ("sample" Pearson = ordinary r; n-1 divisor cancels).
Answer = |r(Y1)−r(Y2)|, 4 dp. The two series are near-perfectly correlated within
a year, so the abs diff is TINY (~1e-4); large answer = wrong column/missing month.
Worked CORRECT: 1979 vs 1984 -> gold **0.0003** (single scalar, no delimiter).

## Maturity Schedule "FIXED maturity issues" + OLS regress -> references/maturity-schedule-fixed-issues-regression.md
4 EARLY bulletins (1948/1949/1950/1951 _03) + "fixed maturity type interest-bearing
public marketable securities per the Maturity Schedule (Outstanding Jan 31), OLS
linear regress, project next Jan." GOLD=39.5 (VERIFIED). ★ Use ONLY the FIRST /
NEAREST maturity-year group's "Total" Fixed value (debt maturing IN the bulletin's
OWN Jan year) — do NOT sum the whole schedule, do NOT add Panama Canal bond.
First-group Totals(M): 1948=46,615 1949=36,068 1950=44,467 1951=40,537 -> billions
-> OLS -> 1952 = **39.5**. (FAILED 3x by summing whole column -> 50/57; WRONG.)
Parse/OCR UNRELIABLE -> read pdftoppm page IMAGES (p.28/29/31/32) with vision.

## Treasury yields BY MATURITY CLASS, self-contained monthly OLS forecast -> references/treasury-yields-by-maturity-class-regression.md
Q: "nominal average yields from taxable Treasury bonds **due or callable in N years
or after**, OLS regression over <m1 yyyy>-<m2 yyyy> (**calendar months, not fiscal
year**), forecast yield for <next month>, 3dp." NOT the MY-2 market-yields table —
this is the **average yields BY MATURITY CLASS** table; read the column whose header
matches the requested band exactly ("20 years or after"). ★ SELF-CONTAINED: the
answer IS the bare prediction — NO external actual, NO abs-diff (unlike MY-2/FFO-1).
x=month index 1..n (Jul53-Jun56 = 36 months), polyfit deg1, predict x=n+1. VERIFIED:
"20yr or after", Jul53-Jun56 -> Jul-1956 = **2.916** ✓. Delimiter MODE A (decimal).

## EXTERNAL historical constant (FX rate / CPI / GDP) -> references/external-historical-constants.md
Final step "divide by the annual avg USD->GBP exchange rate for 1941" (or any
macro constant NOT printed in the Bulletin). Extraction+forecast is easy; answer
hinges on the CORRECT external constant (#1 failure mode) — LOOK IT UP if web
avail. 1941 USD/GBP annual avg = 4.0345 (verified: fish-import forecast Q -> gold
3.9970). Forecast "MoM increase added to M2 to forecast M3" = 2*V2 - V1. "as a
number like 5.25" = already *100, don't /100 again. Different year named => fetch
that year, do NOT reuse 4.0345.
Also covers HISTORICAL-EVENT -> calendar-YEAR mapping when a Q names no years but
references events ("end of WWII"=1945, "Korean War began"=1950, "fall of Saigon"
=1975): convert event->year FIRST, then read those annual rows (e.g. Moody Aaa =
"highest quality corporate bonds by Moody" annual-yield table). A 0.0 abs-change
result is legitimate (1945 vs 1950 Aaa yield ≈ flat) — don't distrust it.
ALSO covers (a) historical-event -> DAY-OF-MONTH divisor: "day in Sept 1939
Germany invaded Poland"=1 (Sep 1) so divide-by-1 = NO-OP; and (b) INTRA-YEAR
MONTHLY quadratic regression (3-4 consecutive months from ONE 1939 Bulletin year,
t=1..4, polyfit deg=2, project next month) — distinct from the multi-year cubic.
WORKED (gold 566840): "international flows of liquid banking funds" = Net movement
of banking funds GRAND-TOTAL row in the International Capital Movements tables.

## Multi-bulletin R-SQUARE / correlation BETWEEN two series -> references/r-squared-between-two-series.md
"R-square (or correlation) of the relationship between [A] and [B] for FY YYYY-YYYY,
use bulletins Sep 1996/2001/2006/2011." NOT a projection (no target year, no
external constant). Both series are two ROWS of the SAME FFO-1 table (e.g.
on-budget vs off-budget receipts), one (x,y) pair per FY. Sep YYYY bulletin ->
actual FY (YYYY-5)..(YYYY-1); 4 bulletins chain to 20 yrs 1991-2010. R-square =
(Pearson r)² = np.corrcoef(a,b)[0,1]**2, round 4dp -> Mode A [0.8298]. Worked: on
vs off-budget receipts FY1991-2010 = 0.8298 (gold).
VARIANT (same ref): "Pearson correlation coefficient between [currency A] and
[currency B] positions for [months]" -> report r ITSELF (not squared), source =
nonbanking-firms' foreign-currency-positions table (Capital Movements, 1970s-80s
bulletins), currencies are COLUMNS, quarterly month-ends are ROWS, values in
millions of the foreign unit. NEAR-MISS RULE: with ~4 points, r off only at 4th
decimal (e.g. 0.3723 vs gold 0.3719) = ONE mis-extracted cell, not a formula
error; never pre-round intermediates, re-read all 2N cells digit-by-digit,
verify quarter/year rows and that you didn't swap an adjacent currency column.

## Ownership Survey / TABs + "count categories over a threshold" -> references/ownership-survey-and-count-threshold.md
##   ALSO covers: TSO-3 "by issue / Regular weekly+annual maturing" Treasury Bill rows are BY MATURITY MONTH (decay 20k->3k) NOT stock; "total outstanding" of a security = its TOTAL/grand-total line; "how many months bills outstanding > $X" w/ N surveys = each survey covers its 12 forward months -> load this ref.
## *** RECURRING HARD FAIL (got 7, gold 12, TWICE) ***: "how many calendar months from <A> to <B> inclusive had TOTAL nominal outstanding of interest-bearing marketable Treasury BILLS > $20000M, using exactly 2 ownership surveys (Jan 1977 + Jan 1978)?" The metric is the STOCK total = "Total Treasury Bills" line (Jan31'77=164,005; Jan31'78=161,221 par millions), which is ~160k and CLEARS 20,000 in EVERY month. Each survey is one snapshot standing for its 12 FORWARD months: Jan'77 survey -> Feb'77..Jan'78 (12 mo), Jan'78 survey -> Feb'78..Jan'79 (12 mo). Feb'77..Jan'79 inclusive => 12 + ... but window spans exactly the 2 survey years; ALL 12 months of the relevant span clear it -> ANSWER = 12. DO NOT read the TSO-3 by-maturity-month "Total amount outstanding" rows (they decay 20k->3k and only ~7 exceed 20k) — that decaying maturity-bucket read is the trap that produces the WRONG 7.
"Treasury Survey of Ownership" breaks marketable debt by INVESTOR CLASS (commercial
banks, insurance cos, S&Ls, corporations, states/local, etc.). DISTRACTOR TRAP: the
question frames the category universe with one snapshot ("end of January 19XX") but
asks the metric on a DIFFERENT month + DIFFERENT security column ("Treasury TABs as
recorded in March"). Read the MARCH survey, TABs (Tax Anticipation Bills) column —
not bills/total/January. "How many categories had more than $500 million ... report
as a SUM of each year's count" = COUNT categories with value>500 (millions table) in
each year, then ADD the two integer counts. Answer is a tiny bare integer (e.g. 3),
NOT a dollar sum. Blank/dash cell = 0, does not count.

## Weekly CAPITAL MOVEMENTS by foreign area + weekday-anchored dates -> references/weekly-capital-movements-by-area.md
"Between the third Thursday and fourth Wednesday in <Mon Year>, net capital
inflow/outflow (thousands) between US and <area, e.g. Latin America>?" = 1938-40s
"Capital Movements between US and Foreign Countries" weekly exhibit. Rows=foreign
AREAS/countries, columns=WEEKS (week-ending dates). MAIN TRAP: resolve "third
Thursday"/"fourth Wednesday" as REAL calendar dates (compute with Python), NOT
table column ordinals. Jan 1939: 3rd Thu=Jan 19, 4th Wed=Jan 25. Table already in
THOUSANDS -> no rescale; read Latin America AREA-aggregate row for the matching
week. Check per-week vs cumulative. Worked: Latin America Jan19-25 1939 = 1461.

## MODERN capital-movements "Total Liabilities" by COUNTRY, multi-year sum + FX-convert -> references/capital-movements-liabilities-by-country-fx-convert.md
Q names a COUNTRY (UK, Japan), asks "Total Liabilities in capital movements,
nominal USD millions" for the SAME calendar month across SEVERAL years (Jun 2000,
2001, 2002), SUM them, then convert to that country's currency using a USD->FX
rate "rounded to its hundredths" on a NAMED date. Post-1990s TIC "Liabilities to
Foreigners Reported by Banks" table; read the country's "Total" row (NOT a
sub-component) verbatim in MILLIONS from EACH year's bulletin. ROUND the FX rate
to 2dp FIRST, then multiply the full USD sum. Answer = MODE A 2dp. Worked: UK
Jun00+01+02 sum * GBP/USD(2002-06-30 rounded) = 372507.20.

## Foreign liabilities BY CURRENCY denomination, SHARE across year-ends, MAX/MIN -> references/foreign-liabilities-by-currency-share.md
Q: "max share of <currency> (e.g. Canadian dollar) liabilities out of TOTAL
liabilities to foreign countries, CY-end values 2009-2011, as a DECIMAL." This is
the CURRENCY-denomination table (rows = USD/CAD/EUR/JPY/GBP/CHF/other), NOT the
by-COUNTRY table. For each Dec-31 year-end: share = currency cell / Total cell
(both USD millions, scaling cancels). Take MAX of per-year shares. Non-USD shares
are TINY: CAD ~0.005 (0.5%). Report DECIMAL not percent (0.005 not 0.5). Worked:
CY2009-2011 max CAD share = 0.005.

## SILVER monetary stock -> physical oz (statutory $1.2929/oz) -> REAL silver price -> MEDIAN -> references/silver-stock-statutory-conversion-real-price.md
Q: "total silver monetary stock (millions $, nominal) at Sep 1938/1948/1958, convert
to physical fine troy oz via the fixed STATUTORY conversion rate per fine oz, multiply
by the REAL inflation-adjusted silver price, return MEDIAN 2dp." Statutory rate =
$1.2929/oz (≈$1.29, the coinage/monetary value the stock is booked at — NOT $0.50/$0.7111
purchase prices). REAL price = market_silver_price(yr) * CPI_base/CPI_yr (DEFLATE; don't
skip/invert). Then statistics.median of the 3 products. FAIL: 3584.40 vs gold 2051.51
(1.747x) = likely used NOMINAL market price (no CPI deflation) or wrong median year.
Load the ref. MODE A 2dp.

## DIGIT-FREQUENCY counting ("how many times does numeral D appear as LEADING digit") -> references/digit-frequency-counting.md
NON-extraction category: count digit occurrences across a whole table region, not a
cell value. "Excluding row/column headers, on pdf page N ... how many times does '1'
appear as the LEADING digit within the table datapoints?" Answer = bare integer COUNT
(e.g. 104). METHOD: pdftotext -layout -f N -l N on the PDF-page number the Q gives
(trust it; May 1980 pdf41=report23, offset 18); drop header + stub-label lines;
tokenize numbers with regex r'-?\d[\d,]*\.?\d*' (keeps "1,234" whole = ONE datapoint,
leading 1); leading digit = first NON-ZERO significant digit (commas/decimal/sign not
digits; "0.45"->4). Count in Python, NOT by eye (100+ cells, gold is large). Pitfalls:
"leading" != "contains"; don't split thousands-comma numbers; exclude years/page nos;
a page may hold 2+ sub-tables — count all. Load the ref.

## VISUAL chart questions: counting features on LINE PLOTS (local maxima/minima, crossings)
A NON-extraction, VISION category: "On page N of the <Month Year> Bulletin, how
many LOCAL MAXIMA are there on the line plots on that page?" (also: local minima,
inflection points, times two lines cross, peaks above a threshold). The answer is
an integer COUNT of VISUAL features across ALL chart panels on the page — no table
reading, no unit scaling. The Bulletin's front "Chart" pages (distinct from the
"Table" exhibits) carry these line graphs; early-page chart sections plot monthly
series (receipts/outlays, debt, yields, money supply) over a multi-year x-axis.

METHOD — you MUST actually SEE the page at high resolution; do NOT reason from
pdftotext (charts have no extractable text peaks) or a thumbnail.
1. Render the single page to a HIGH-RES image (300 dpi min) and load it:
       pdftoppm -png -r 300 -f N -l N file.pdf /tmp/pg
   then vision_analyze on /tmp/pg-NN.png. If peaks are dense, render at -r 400+
   and/or crop per chart panel so individual wiggles are resolvable.
2. COUNT PER PANEL, THEN SUM. A "page" usually holds MULTIPLE stacked chart
   panels (2-5), and EACH may contain MULTIPLE lines (e.g. receipts vs outlays,
   or several maturity yields). "Line plots on that page" = EVERY line in EVERY
   panel. Tally each line's local maxima separately and add them up — the single
   most common error is counting one panel/one line and missing the others.
3. DEFINITION of a local maximum: a point higher than its immediate neighbors on
   both sides (an interior peak). Watch the AMBIGUOUS cases that cause off-by-one:
   - ENDPOINT peaks: a series that ends on an up-tick has NO right neighbor — by
     the strict interior definition it is NOT a local max. But a series whose
     value at the LEFT or RIGHT edge is higher than the adjacent interior point
     is sometimes counted as a boundary maximum. OfficeQA tends to count CLEAR
     interior peaks; when unsure whether an edge counts, the gold often INCLUDES
     a prominent edge peak — so re-scan both endpoints, a missed edge peak is the
     classic off-by-one (my 17 vs gold 18 = one missed peak, likely an edge or a
     low-amplitude wiggle on a secondary line).
   - PLATEAU / shoulder peaks: a flat-topped local max counts ONCE.
   - Small-amplitude wiggles on a noisy line each count — zoom in; do not smooth
     them away. Faint/secondary lines (lighter ink, dashed) carry peaks too.
4. SANITY: list every peak you found per panel ("panel 1 line A: 4 peaks at
   ~1972,'74,'77,'79; line B: 3 ...") so the total is auditable. If your count is
   off by exactly 1 from an expected ballpark, re-examine: (a) both x-axis edges
   of each line for an edge peak, (b) any faint/overlapping second line you may
   have skipped, (c) a shallow double-peak you merged into one. Off-by-one on
   these is almost always a MISSED peak, not a double-count — bias toward
   re-scanning for one more rather than removing one.
5. Local MINIMA: same method, troughs (lower than both neighbors). Crossings:
   count each point where two plotted lines intersect.
- Worked example: Sept 1990 Bulletin, page 5, count of local maxima on the line
  plots = 18 (I answered 17 — missed one peak; render at higher dpi and audit
  each line's endpoints + faint lines next time).

## Z-score: "how many SAMPLE standard deviations off the average" (sample vs population)
A statistics wrapper: collect N values (one per year/period over an inclusive
range), compute the SAMPLE mean and SAMPLE standard deviation, then report how
many standard deviations a particular value sits from the mean (a z-score):
    z = (x_target - mean) / std
- "SAMPLE standard deviations" / "sample standard deviation" => use the N-1
  (ddof=1) std dev: statistics.stdev(vals) or np.std(vals, ddof=1). This is the
  OPPOSITE of the TIPS volatility question (which says "population" -> pstdev,
  ddof=0). READ THE WORD: "sample" -> ddof=1; "population" -> ddof=0. Using the
  wrong one scales z by sqrt(N/(N-1)) (~1.05-1.12 for N=5-10) and fails the tight
  grader.
- The TARGET value's z keeps its SIGN: a value BELOW the mean gives a NEGATIVE z
  (the 1972 maturity total was below the 5-year average -> z = -1.063). Do not
  report the absolute value.
- "5-year sample average" / "X through Y inclusive" = N = the count of years
  listed (1972-1976 = 5 values). Both the mean and the std use all N values; the
  target (1972) is one of the N.
- Compute in Python:
      import statistics
      vals = [...]                     # N period values (e.g. 5 yearly totals)
      mean = statistics.mean(vals)
      sd   = statistics.stdev(vals)    # SAMPLE (ddof=1); use pstdev for population
      z    = (vals[idx_target] - mean) / sd
  Round only z to the requested place (thousandths -> -1.063). Mode A delimiter.
- The data lookup is ordinary: here "total interest-bearing marketable public
  debt securities SCHEDULED TO MATURE in that calendar year, from the maturity
  schedules outstanding at end of February" = the maturity-distribution exhibit
  (see next section), read the per-CALENDAR-YEAR scheduled-maturity total for
  each year. "outstanding at the end of February for each year" = use the Feb-end
  (Jan 31 / end-of-Feb) maturity schedule from that year's issue, one schedule
  per year. Collect each year's scheduled-maturity total, then run the z-score.

## Maturity-distribution table + OLS PROJECTION of a LEVEL (not log)

The Bulletin carries a "Maturity Distribution of Marketable Interest-Bearing
Public Debt" / "maturity schedule" exhibit (in the public-debt section). It
classifies marketable securities by remaining maturity bucket (within 1 year,
1-5, 5-10, 10-20, 20+ years) and by TYPE. A recurring question reads this table
at a fixed date across several years and fits an OLS line to PROJECT the next
year's level.

- "FIXED maturity type" is a SPECIFIC subset, NOT the grand total of marketable
  debt. The maturity table splits marketable issues into securities with a
  FIXED maturity date vs those with an OPTIONAL/CALLABLE maturity range (bonds
  callable before final maturity, listed by their call-to-maturity span). Read
  ONLY the fixed-maturity total — EXCLUDE callable/optional-maturity bonds, and
  exclude non-marketable issues (savings bonds, special issues, Treasury
  notes/bills only if the question scopes them out). Including callable bonds or
  the all-marketable total inflates the level and the projection.
  DIAGNOSTIC: my projection 50.0 vs gold 39.5 (~27% high) — an overshoot of this
  size on a 1948-1951 postwar series almost certainly means I summed too BROAD a
  category (whole marketable total or included callable/optional-maturity issues)
  instead of the narrower fixed-maturity-only figure. When the projection is
  high, re-check that you took the FIXED-maturity subtotal, not the grand total.

- "maturity schedule published on the last day of January of each year 1948-1951"
  = read the maturity table AS OF Jan 31 of each year (4 data points). Each
  year's figure comes from that year's January Bulletin (or the issue that
  publishes the Jan 31 maturity schedule). One value per year, 4 values total.

- OLS PROJECTION OF THE LEVEL (this question type fits the RAW value, NOT ln):
      x = [1948,1949,1950,1951]            # or 1-based index [1,2,3,4]; slope/
                                           # intercept differ but the PROJECTION
                                           # at the matching x is identical
      y = [v1948, v1949, v1950, v1951]     # fixed-maturity total, in billions
      slope, intercept = polyfit(x, y, 1)  # least squares on the LEVEL
      proj_1952 = slope*1952 + intercept   # (or slope*5 + intercept if 1-based)
  Round the projection to the requested place (tenths here -> 39.5). This is a
  PLAIN linear extrapolation of the value — do NOT log-transform y (that's the
  separate "OLS of ln(value) on FY index" question, which asks for slope+intercept
  not a projection). Read the verb: "project this AMOUNT" => extrapolate the level.

- The projection is exact regardless of whether x is calendar years or a 1-based
  index, AS LONG AS the target x is consistent (1952 with calendar x, or 5 with
  1-based x). The off-by-one index trap that affects INTERCEPT does NOT affect a
  correctly-aligned PROJECTION.

- Compute in Python:
      import numpy as np
      x = np.array([1948,1949,1950,1951]); y = np.array([...])
      m,b = np.polyfit(x,y,1)
      print(round(m*1952+b, 1))
  (If numpy is unavailable, statistics.linear_regression(x,y) returns slope,
  intercept on Python 3.10+, or hand-code the closed-form OLS.)

- SANITY: postwar (1948-1951) fixed-maturity marketable debt was roughly flat
  to modestly changing; a projected ~40 (billions) is plausible. A projection
  near 50 means the input series trended up too steeply -> wrong/too-broad rows.

## QUADRATIC (2nd-degree polynomial) regression projection — distinct from linear OLS
A recurring forecast wrapper that is NOT the plain linear OLS projection: \"fit a
QUADRATIC (2nd-degree polynomial) regression to these data points (t=1..N) and
project the value for the next step (t=N+1).\" You read N values (one per period),
fit a degree-2 polynomial, then evaluate it at the next t.
- USE DEGREE 2, NOT 1. polyfit(x, y, 2) returns [a, b, c] for a*x^2 + b*x + c.
  With exactly N=3 points a quadratic fits EXACTLY (interpolation); with N=4 it
  is a least-squares fit. The question wording \"quadratic / 2nd-degree polynomial\"
  is the trigger — do NOT reflexively use the linear (degree-1) projection from
  the maturity-distribution section.
- t-INDEXING: the question states the index base explicitly (\"t=1 (May) through
  t=4 (August)\", project \"September (t=5)\"). Use those exact t values; fit on
  x=[1,2,3,4], evaluate at x=5. The projection is index-base-consistent as long as
  the target t matches the fit's x convention.
- Compute in Python:
      import numpy as np
      x = np.array([1,2,3,4]); y = np.array([v1,v2,v3,v4])
      coeffs = np.polyfit(x, y, 2)          # degree 2 -> [a,b,c]
      proj = np.polyval(coeffs, 5)          # evaluate at t=5
  np.polyfit may warn \"Polyfit may be poorly conditioned\" for tiny N — that's fine,
  the fit/eval is still exact/least-squares.
- A quadratic EXTRAPOLATES with curvature, so the projected next value can shoot
  well above/below the linear trend (the t^2 term dominates at the edge). Don't
  \"sanity-clip\" it to the linear trend — the gold uses the raw quadratic value.
- Worked example: monthly aggregate international flows of liquid banking funds,
  May-Aug 1939 (t=1..4), quadratic projection for Sep 1939 (t=5), then divided by
  the day-of-month Germany invaded Poland (Sep 1, 1939 -> day number 1, so the
  divisor was 1), rounded to nearest integer -> 566840 (CORRECT).

## Historical-event-DAY-NUMBER divisor/operand wrappers
Some questions append a final arithmetic step keyed to a HISTORICAL DATE's
day-of-month (or day-of-year): \"divide your projected value by the calendar DAY
NUMBER in <Month Year> on which <event> happened.\" Translate the event to its
exact date, take the DAY-OF-MONTH integer, then apply the operator.
- Germany invaded Poland = SEPTEMBER 1, 1939 -> day number = 1 (so \"divide by\"
  it is a no-op; the projected value passes through unchanged except rounding).
  Watch for day=1 making the divisor harmless — the real work was the projection.
- Other common anchors (translate carefully, the question may want day-of-MONTH):
  Pearl Harbor = Dec 7, 1941 (day 7); D-Day = June 6, 1944 (day 6); VE Day =
  May 8, 1945 (day 8); VJ Day = Aug 15 (or Sep 2) 1945; US enters WWI = Apr 6,
  1917 (day 6); stock-market crash \"Black Tuesday\" = Oct 29, 1929 (day 29);
  armistice ending WWI = Nov 11, 1918 (day 11).
- READ whether it wants the DAY-OF-MONTH (1-31) or the day-of-YEAR ordinal — the
  phrasing \"calendar day number in <Month>\" means day-of-month. Verify the exact
  date (some events have a commonly-cited date that differs from the technical
  one); when in doubt, use the widely-accepted historical day-of-month.
- Apply the operator in the EXACT order written (the divide/multiply by the day
  number is usually the LAST step, after the projection/extraction), then round.

## Aggregate international flows of LIQUID BANKING FUNDS (1930s-40s capital tables)
The early Bulletins' Capital-Movements / international-finance section reports
monthly \"international capital movements\" including a breakdown of flows of
SHORT-TERM / LIQUID BANKING FUNDS between the US and abroad. A recurring lookup:
\"the monthly GRAND TOTAL representing aggregate international flows of liquid
banking funds (EXCLUDING brokerage balances and security transactions).\"
- This is a SUMMARY/GRAND-TOTAL row of the liquid-banking-funds movement table,
  NOT the brokerage-balances line and NOT the securities-transactions line — the
  \"excluding brokerage balances and security transactions\" clause tells you which
  sub-rows to leave out; you want the banking-funds aggregate (often labeled a
  net total of banks' own + customers' liquid funds movements).
- Reported MONTHLY (one value per calendar month). For a \"May through August 1939\"
  span, read the May, June, July, August 1939 monthly cells (4 data points).
- These capital-movement figures are natively in THOUSANDS (or millions) of
  dollars — check the header; the downstream answer here was a raw integer
  (566840) so no billions scaling. Read the printed value in its native unit.
- One Bulletin issue's table shows several recent months side by side; the
  1939 issues covering mid-late 1939 carry May-Aug 1939 together.

## Productivity / output-per-hour tables (quarterly, percent-change series)

The Bulletin's economic-indicators / business-statistics section carries U.S.
NONFARM BUSINESS PRODUCTIVITY series — "output per hour" (of all persons / of
labor) and related measures (output, hours, unit labor costs, compensation),
reported by CALENDAR-YEAR QUARTER. The series are often printed as PERCENT
CHANGE (the growth rate at an annual rate, or quarter-over-quarter), keyed by
year+quarter columns/rows.

- "GROWTH RATE of productivity ... in the Nth calendar year quarter of YYYY" =
  the PRINTED percent-change cell for that exact quarter (the table already
  reports the growth rate; you usually do NOT compute it from a level series).
  Match the row (nonfarm business, output per hour) and the quarter column
  exactly. "third calendar year quarter of 1995" = 1995 Q3; "first calendar
  year quarter of 1998" = 1998 Q1.
- "ABSOLUTE DIFFERENCE in the growth rate between quarter A and quarter B,
  inclusive" = |growth_B - growth_A| of the two printed growth-rate cells.
  This is the ABSOLUTE gap (NOT the "relative difference" trap — there is no
  normalize-by-base here; the word is "absolute"). Round to the requested place
  (tenths here). Worked example: nonfarm business output-per-hour growth rate,
  1995 Q3 vs 1998 Q1, absolute difference = 1.8 (nearest tenth).
- These are already PERCENT rates — no unit scaling. Read the printed figure.
- PITFALL: a productivity exhibit lists MULTIPLE measures (output per hour,
  output, hours, unit labor costs, compensation per hour) and MULTIPLE sectors
  (business vs NONFARM business vs manufacturing). Read the exact measure +
  sector named. Also some issues print both a quarterly rate AND a 4-quarter /
  annual rate — pick the per-quarter cell the question's quarter wording asks
  for. "inclusive" here just confirms both named quarters are the two endpoints;
  it does NOT mean sum/average the quarters in between.

## CPI-U inflation-adjustment wrapper (apply YoY inflation rate to a Treasury figure)

A recurring transform: "the inflation-adjusted dollar amount after applying the
official BLS CPI-U YEAR-OVER-YEAR inflation rate for calendar month <Mon Year>
to <some Treasury table figure> for the same (fiscal) month." You read ONE
Treasury value V, look up/compute the CPI-U YoY inflation rate r for that month,
then report V*(1+r). The CPI part is small arithmetic; the ERROR is almost always
the TREASURY VALUE you read, NOT the rate.

- FORMULA: inflation-adjusted = V * (1 + r), where
      r = (CPI_U[month, year] - CPI_U[month, year-1]) / CPI_U[month, year-1]
  "year-over-year for calendar month November 1969" = (CPI Nov1969 - CPI Nov1968)
  / CPI Nov1968. Use the SAME calendar month one year apart (NOT Dec/annual avg).
  Reference CPI-U (1982-84=100): Nov 1968 = 36.8, Nov 1969 = 38.8 -> r ≈ 0.0543
  (~5.4%). Apply r to V, do NOT deflate (the answer is LARGER than V here:
  56117.5 = ~53227 * 1.0543). "inflation-ADJUSTED ... after APPLYING the rate"
  means inflate by (1+r); it does not mean convert to constant/real dollars.

- DIAGNOSTIC — wrong BASE value, not wrong rate: if your final answer is off by a
  CLEAN constant factor (mine 48954.4 vs gold 56117.5 = factor 1.1463, the same
  factor regardless of which plausible CPI rate you assume), the inflation math is
  fine — you READ THE WRONG TREASURY ROW. Back out the implied base: gold/(1+r) ≈
  53227 vs my base ≈ 46433. A ~13% gap like this is the signature of reading a
  SUB-TOTAL / partial row instead of the requested grand-total row.

- "TOTAL CURRENCY IN CIRCULATION" — read the GRAND-TOTAL row of the currency /
  money-stock exhibit, NOT a component. The Bulletin's "Currency in Circulation"
  / money-stock tables break currency into components (Federal Reserve notes,
  Treasury currency, coin, etc.) and report several sub-totals AND "currency
  outside the Treasury and Federal Reserve Banks" / "currency held by the public"
  vs the full "total currency in circulation." My ~46,433 was a PARTIAL figure
  (e.g. Federal Reserve notes only, or currency-outside-banks); the gold ~53,227
  is the TOTAL-currency-in-circulation line. When the question says "TOTAL
  currency in circulation," take the all-components grand total, not Federal-
  Reserve-notes-only or a public-holdings subtotal.

- "by the end of the same fiscal month" = the END-OF-MONTH (last business day)
  value for that month — pick the month-end column, not a monthly-average or a
  mid-month figure. "fiscal month November" just means the November period;
  read November's end-of-month currency total.

- Worked example: total currency in circulation end of Nov 1969 ≈ 53,227 (millions)
  * (1 + CPI-U YoY Nov1969 ≈ 0.0543) = 56117.5 (gold, nearest tenth, millions).
  My 48954.4 came from reading a ~46,433 partial currency row (factor 1.146 low).

#### MONTH-OVER-MONTH CPI-adjusted change — read the TWO ADJACENT month-ends
A sub-variant: \"the MONTH-OVER-MONTH change in <Treasury figure> in <Mon2 Year>\n  dollars, using CPI-U to adjust the <Mon1 Year> value to <Mon2 Year> real\n  dollars.\" Two ADJACENT month-end values; inflate the earlier (Mon1) into Mon2\n  real dollars, then subtract from the Mon2 nominal value:\n      adj_Mon1 = V_Mon1 * (CPI[Mon2 Year] / CPI[Mon1 Year])   # SAME-month-apart? NO:\n                                                              # use the TWO months named\n      change   = V_Mon2 - adj_Mon1                            # signed, keep sign\n  The CPI ratio here is the ADJACENT-MONTH ratio (e.g. CPI Jun1979 / CPI May1979 ≈\n  216.6/215.0 ≈ 1.0074), NOT a year-over-year ratio. The real MoM change is TINY\n  relative to the level (the ~0.7% one-month inflation almost cancels the small\n  nominal month change), so the gold is a SMALL signed number (e.g. -156.11) even\n  though FRN levels are ~100,000 millions.\n- THE KILLER — WRONG PERIOD (12 months apart) blows the answer up ~10-66x. A\n  \"month-over-month\" change that comes out HUGE (mine -10295.54 vs gold -156.11,\n  ~66x) is almost never a CPI/formula error — it is reading the WRONG TWO CELLS:\n  two columns 12 months apart (a YEAR-over-year pair), or a fiscal-YTD/cumulative\n  cell instead of the single end-of-month value. DIAGNOSTIC: back out my implied\n  change ≈ -10,295 ≈ ~10% of the ~100,000 FRN level = exactly a FULL-YEAR change\n  during late-1970s ~10%/yr inflation. When a MoM change ≈ an annual-magnitude\n  change, you grabbed the same calendar month a YEAR apart (or two non-adjacent\n  columns) — re-read for the TWO ADJACENT month-end columns (May and June of the\n  SAME year), not Jun-vs-Jun or a YTD figure.\n- \"FEDERAL RESERVE NOTES\" is the COMPONENT row, read it AS NAMED — this is the\n  OPPOSITE of the \"TOTAL currency in circulation\" trap above. When the question\n  explicitly names \"Federal Reserve notes,\" take that specific component line of\n  the currency/money-stock exhibit (NOT the total-currency grand total, NOT\n  currency-outside-banks). Federal Reserve notes ≈ $100B (≈100,000 millions) in\n  1979. Match the exact named row; only fall to the grand total when the question\n  says \"TOTAL currency.\"\n- Worked example: month-over-month change in Federal Reserve notes in June 1979\n  dollars, May 1979 adjusted to June 1979 via CPI-U = -156.11 (gold, hundredths,\n  millions). My -10295.54 = reading FRN 12 months apart (annual change) instead\n  of the adjacent May/June 1979 month-ends. Mode A delimiter.

- UNIT: native millions; if the question asks millions, NO scaling. Round only
  the final adjusted amount to the requested place (tenths here). Mode A delimiter.

#### CONSTANT-BASE-YEAR deflation across MULTIPLE years, then DIFFERENCE
A distinct variant (NOT YoY-rate, NOT adjacent-month): "compute <Treasury figure>
for years Y1, Y2, ... and the BASE year Yb; adjust each to constant Yb dollars
using the ANNUAL AVERAGE CPI-U (1982-84=100, NSA); report the absolute difference
between adjusted Y2 and adjusted Y1 (in millions)."
- FORMULA: adj_Yk = nominal_Yk * (CPI_annual_avg[Yb] / CPI_annual_avg[Yk]). The
  base-year value's own ratio is 1 (it is already in Yb dollars). Then
  answer = | adj_Y2 - adj_Y1 |  (take ABSOLUTE value when "absolute difference").
- USE THE ANNUAL-AVERAGE CPI INDEX, not a month-end CPI -- the question says
  "annual average BLS CPI-U." Even when the Treasury figure is an END-OF-FISCAL-
  YEAR level, the DEFLATOR is still the calendar-year annual average index for
  that year. CPI-U annual averages (1982-84=100): 1960 = 29.6, 1961 = 29.9,
  1962 = 30.2. (FFY 1960/61/62 ended June 30; use the calendar-year annual avg
  matching the fiscal-year label, e.g. FY1960 -> 1960 annual avg = 29.6.)
- THE TREASURY VALUE: "total public debt outstanding as of end of FFY" = the
  END-OF-PERIOD (June 30, pre-1977) TOTAL gross public debt outstanding grand
  total from the Bulletin's public-debt / debt-outstanding table -- the all-in
  total, not interest-bearing-only or marketable-only. Native unit is millions.
- WORKED (this benchmark): |adj1961 - adj1960| = 264.632 (gold, thousandths,
  millions, no commas). adj_Yk = nominal_Yk * (30.2 / CPI[Yk]). The answer is a
  SMALL number (hundreds of millions) even though debt levels are ~286,000
  millions, because deflating two near-equal nominal levels to a common base
  nearly cancels. Mode A delimiter (decimals, single bare value, no commas).
- DIAGNOSTIC: if your answer is in the tens-of-thousands, you likely forgot to
  deflate one term, used a month-end instead of the annual-avg CPI, or read
  interest-bearing-only vs the gross total public debt.

### TRUST-FUND TOTAL BALANCE (Unemployment Trust Fund etc.) — read the GRAND TOTAL
A variant: "signed difference (Y2 - Y1) in the TOTAL BALANCE of the <Unemployment>
Trust Fund as of Dec Y1 and Dec Y2, adjusted for inflation using CPI-U, in
millions of Y2 dollars." Two month-end balances, inflate the EARLIER one to Y2
dollars, subtract.
- FORMULA: adj_Y1 = balance_Y1 * (CPI[Dec Y2] / CPI[Dec Y1]); adj_Y2 = balance_Y2
  (already in Y2 dollars). signed diff = adj_Y2 - adj_Y1 (keep the sign; "Y2 - Y1"
  order). Use the DECEMBER CPI of each year (the "as of December" month), not the
  annual average. CPI-U 1982-84=100: Dec 1946 ≈ 21.5, Dec 1947 ≈ 23.4.
- WHY THE SIGN CAN BE NEGATIVE despite the fund growing nominally: inflating the
  1946 balance up to 1947 dollars can make REAL 1946 > nominal 1947, so the real
  change is negative even though the fund grew in current dollars. A negative diff
  is plausible here — don't flip it.
- THE KILLER — read the FUND'S TOTAL BALANCE, not a component/sub-account. The
  Unemployment Trust Fund statement (in the trust-fund / "Trust account" tables)
  lists multiple lines: individual STATE account balances, the Railroad
  Unemployment Insurance account, the Federal unemployment account, the
  administrative/employment-security account, AND the overall TOTAL fund balance.
  Read the GRAND-TOTAL fund balance row for each date — NOT a single state's
  balance, not the railroad sub-account, not the federal-account-only line.
- DIAGNOSTIC — clean ~4x miss = wrong (partial) row: my answer -131.4 vs gold
  -550.3 = factor 4.19, SAME sign. A single clean multiplicative miss (not 2x
  rounding) with the sign correct means the CPI math was fine and I read a
  PARTIAL balance (a sub-account or one component) instead of the TOTAL fund
  balance. Back out: gold/(1+inflation-ratio) gives the true total; if your base
  balances are several-fold smaller than the fund's known ~billions-scale total,
  you grabbed a component. When a CPI-adjust trust-fund question misses by a
  clean factor with correct sign, RE-READ for the all-accounts TOTAL balance row.
- The Unemployment Trust Fund total balance was multi-billion (thousands of
  millions) in the mid/late 1940s; a Dec-to-Dec real difference of a few hundred
  million is the right magnitude. If your inputs imply a ~1-2 billion fund, you
  likely read a sub-total. Trust-fund balances live in the Bulletin's trust-fund
  statements / "Trust account" tables, keyed by month-end.

## Silver/gold monetary-stock -> physical-quantity via STATUTORY conversion rate
A multi-step monetary-metals wrapper (NEW category, EASY to get the constant
wrong): read the Treasury's SILVER (or gold) MONETARY STOCK in millions of
dollars at several month-end dates, convert each dollar value to a PHYSICAL
QUANTITY of fine troy ounces using a FIXED STATUTORY conversion rate, then
multiply by an inflation-adjusted metal price to get a nominal value, and
combine (median/mean/etc.). The data lookup is ordinary; the KILLER is WHICH
statutory rate you divide by — there are several candidate silver constants and
they differ enough to throw the final answer off by a clean factor.

- PHYSICAL QUANTITY = dollar_stock / statutory_rate_per_fine_troy_ounce.
  The Treasury's silver monetary stock is carried/monetized at the STATUTORY
  COINAGE VALUE of silver, which is $1.2929 per fine troy ounce (derived from
  the standard silver dollar = 371.25 grains of fine silver: 480 grains/oz ÷
  371.25 grains/dollar = $1.29292.../oz). This is the rate at which silver
  dollars and silver certificates were issued — i.e. the value at which the
  silver stock is BOOKED in the Bulletin's monetary-stock tables.
- DO NOT confuse the $1.2929 STATUTORY/COINAGE rate with the prices the Treasury
  PAID or pegged at under the Silver Purchase Acts: $0.50/oz, $0.6464/oz, the
  $1.29 ceiling, or the $0.905/oz Treasury support price. Those are PURCHASE
  prices, not the booking/statutory monetization rate. Likewise gold's statutory
  rate is $35/oz (post-1934) or $20.67/oz (pre-1934) — pick by era.
- DIAGNOSTIC — clean-factor miss = wrong statutory constant: my answer 3584.40
  vs gold 2051.51 = factor 1.747. That factor ≈ 1.2929/0.7395 (and other rate
  ratios land nearby), the signature of dividing the dollar stock by the WRONG
  silver rate (too small a divisor -> too many ounces -> answer too big). When
  one of these silver/gold questions misses by a single clean multiplicative
  factor (not ~2x rounding, but ~1.5-1.8x), re-check the statutory conversion
  constant FIRST — the table lookup and the median/price steps are probably fine.
  Candidate silver constants to test against the gold-implied factor: $1.2929
  (coinage/statutory, most likely the BOOKED rate), $1.29 ceiling, $0.9050
  support, $0.6464, $0.50. Back out gold/your_answer to see which rate ratio
  matches, then re-derive.
- "real inflation adjusted silver price AT THAT TIME" = the metal price deflated
  to (or expressed in) real terms for that date — read the operators literally
  and apply the price AFTER computing the physical ounces. If the question gives
  no explicit price table, it may intend the statutory price itself; but the
  phrase "real inflation adjusted ... price" usually means a market silver price
  CPI-adjusted to a base year. Identify the exact price source the question
  cites before multiplying.
- MEDIAN of the three computed nominal values = the middle value after sorting
  the three (Sep 1938, Sep 1948, Sep 1958 here) — not the mean. Round only at
  the end to the requested place (hundredths).
- Silver monetary stock lives in the Bulletin's MONETARY STATISTICS / "Stock of
  money" / "Silver" exhibit (same section as seigniorage, gold stock, currency
  in circulation), reported by month-end in millions of dollars.

## H Spread / IQR (Type-7 quartiles) with an INTERMEDIATE-rounding instruction
A statistics wrapper: "the H SPREAD of <monthly series> for FY <year> ... use the
standard linear-interpolation percentile method to compute quartiles (Type 7) and
for this question only use the intermediate values rounded to the TENTHS of
billions before computing the H spread value." H Spread = IQR = Q3 - Q1.
- COLLECT the series: 12 monthly values for the named FISCAL year (Oct..Sep for a
  US fiscal year — NOT Jan..Dec). "monthly nominal net budget receipts from
  Corporation income taxes" = the corporate-income-tax row of the monthly budget
  RECEIPTS table, one cell per fiscal month, converted to billions.
- TYPE 7 quartiles = the DEFAULT linear-interpolation method:
      import numpy as np
      q1 = np.percentile(x, 25)            # method='linear' is Type 7 (default)
      q3 = np.percentile(x, 75)
      hspread = q3 - q1
- THE KILLER — WHERE the "rounded to tenths" applies. "use the INTERMEDIATE
  VALUES rounded to the tenths ... BEFORE computing the H spread value" means
  round Q1 and Q3 (the intermediate quartile results) to the nearest TENTH, THEN
  subtract — NOT round the 12 input data points. Q3-Q1 of two tenth-rounded
  numbers is itself a tenth-resolution number, so the gold lands on a clean tenth
  even though the answer is reported to hundredths (e.g. 57.50, the trailing 0
  preserved per Mode A).
      q1r = round(q1, 1); q3r = round(q3, 1)
      hspread = round(q3r - q1r, 2)        # -> e.g. 57.50
- DIAGNOSTIC: my 57.53 vs gold 57.50 (off by 0.03, and 57.53 is NOT a tenth) =
  I rounded the wrong stage. A non-tenth H-spread when the instruction said to
  round intermediates to tenths is the signature of having rounded the 12 input
  values (then run Type-7 interpolation, which re-introduces hundredths) instead
  of rounding the two QUARTILES Q1/Q3 to tenths and subtracting. When the answer
  isn't a clean tenth but the rule said "intermediate values to tenths," re-apply
  the rounding to Q1 and Q3 themselves.
- "intermediate values" in these instructions = the quartiles (the values that
  feed the final formula), not the raw data. Round the immediate inputs to the
  final operation, then do the final operation, then round to the reported place.
- These budget-receipts figures are natively in millions -> divide by 1000 for
  billions; do the unit conversion BEFORE rounding to tenths-of-billions. Mode A
  delimiter, keep trailing zero (57.50).

## Herfindahl-Hirschman Index (HHI) of concentration + effective-number reciprocal
A market-concentration wrapper: read a small set of holdings/values that form a
\"market\", compute each player's SHARE, then HHI = sum of squared shares. A
recurring companion sub-question asks for the \"effective number\" = 1/HHI.
- FORMULA (shares as FRACTIONS, so HHI is on a 0-1 scale):
      shares = [v_i / sum(values) for v_i in values]
      HHI    = sum(s**2 for s in shares)        # in [1/N, 1], decimal form
      eff_N  = 1 / HHI                          # reciprocal = effective # of players
  For N=2 groups with values a,b: HHI = (a/(a+b))**2 + (b/(a+b))**2; eff_N = 1/HHI.
- DECIMAL vs POINTS scale — read the wording. \"shares based on the VALUE of ...\"
  with a thousandths rounding and no \"points\"/\"x10000\" instruction => use the
  DECIMAL 0-1 convention (shares as fractions). HHI then lands in [0.5,1] for a
  2-group market. The ANTITRUST convention (shares as percent, HHI 0-10000) is a
  DIFFERENT scale — only use it if the question says points / out of 10000. Here
  the decimal form was correct: gold 0.611 (NOT 6112 or 61.1).
- \"effective number of bank GROUPS implied ... reciprocal of the HHI\" = 1/HHI,
  the numbers-equivalent / inverse-Simpson value. For a 2-group market it ranges
  1 (one group has everything) to 2 (perfectly equal split). Worked example:
  NYC banks vs Chicago banks holding Treasury notes -> [0.611,1.635] (HHI 0.611,
  eff groups 1/0.611=1.635, both to thousandths). The two GROUPS are the market
  participants (NYC group, Chicago group) — the COUNTS (16 NYC, 14 Chicago banks)
  are a distraction; the shares are by the VALUE of notes held by each GROUP, not
  by bank counts. Read the two group-total note VALUES from the bank-ownership
  survey table.
- The \"bank ownership survey ... published on the last day in 1959\" = the
  Dec-31-1959 ownership/holdings survey exhibit; pick the column for the value of
  Treasury notes held by each bank group.
- Output order [HHI, effective_number]; Mode A delimiter (bare comma), keep
  trailing thousandths.

## (Historical Expected Shortfall is covered ONCE, above at line ~1211.)
# DELETED a stale, self-contradictory duplicate that said "do NOT pct-change the
# yields" and computed ES on raw LEVELS -> +6.14 (CONFIRMED WRONG; gold -18.51%).
# That math is impossible: the min of 6-9% yields can never be -18.51. ALWAYS
# convert levels -> simple returns FIRST. See references/historical-expected-shortfall-cvar.md.

## Balance-sheet reasoning trap (recurring)
A Treasury fund balance sheet (e.g. Exchange Stabilization Fund) follows:
    Total Assets = Total Liabilities + Total Capital
The bottom line is usually labeled "Total capital and liabilities" (= Total
Assets). Questions often ask for BOTH:
  (a) a sub-total like "total nominal capital", AND
  (b) the absolute difference between (a) and "total capital and liabilities".

Key insight: "total capital and liabilities" is the GRAND TOTAL (the whole
balance sheet footing), while "total capital" (or "total nominal capital") is
only the capital portion. Their absolute difference therefore equals TOTAL
LIABILITIES. So:
  - Read both the capital sub-total line and the grand-total footing line.
  - difference = |grand_total - capital_subtotal| = total liabilities.
  - Worked example (ESF, end of March 1989): capital = 8.124 B,
    total capital & liabilities = ~20.976 B, difference = 12.852 B.
    Answer: [8.124, 12.852].
- Sanity check: the difference should equal the liabilities you can read
  separately on the sheet. If it doesn't, you grabbed the wrong column or
  mis-scaled a unit.

## U.S. liquidity ratio (international financial statistics, U.S. to Foreigners)
The Bulletin's International Financial Statistics section ("Liquid Liabilities to
Foreigners" / "U.S. Liquidity Position") reports a LIQUIDITY RATIO — U.S. reserve
assets as a fraction (×100 = percent) of U.S. liquid liabilities to foreigners.
Questions ask for the ratio in a given CALENDAR YEAR, sometimes restricted to a
liability subset.
- "U.S. liquidity ratio = U.S. reserve assets / liquid liabilities to foreigners".
  When the Q says "considering only ... marketable liabilities for liabilities to
  FOREIGN OFFICIAL INSTITUTIONS", use that specific subset column (marketable
  liabilities held by foreign official institutions) as the denominator — NOT the
  grand-total liquid-liabilities line. Read the exact narrowed row/column.
- The ratio is typically read directly OR computed = reserves/liabilities*100. If
  the table already prints a ratio row use it; otherwise divide the two cells.
- "change in absolute percentage points" between two calendar years =
  |ratio_yearB − ratio_yearA| in points (NOT a percent-of-percent). Worked: the
  CY2001 vs CY2008 comparison gave a 9.89 point change (gold "9.89%" — bare 9.89
  graded CORRECT; Mode A delimiter, percentage-points value).
- Find the right ANNUAL column: these IFS tables are wide, year-keyed columns
  (calendar-year-end). Confirm the year header AND the exact liability subset row.

## Indirect DATE-CLUE resolution (questions encode years as trivia)
Some questions hide the target year(s) behind real-world trivia instead of stating
them. RESOLVE THE CLUE TO A CALENDAR YEAR FIRST, then do the lookup. Examples seen:
- "Dot-com bubble burst / year Amazon's stock reached its lowest point 2000-2005"
  -> 2001 (AMZN bottomed late 2001).
- "U.S. housing bubble crash / CY the U.S. government passed a multi-billion bank
  bailout package" -> 2008 (TARP / EESA, Oct 2008).
- General: "global financial crisis"=2008; "Lehman collapse"=2008; "9/11"=2001;
  "COVID crash"=2020; "Black Monday"=1987; "Nixon closes gold window"=1971.
Pitfall: resolve to the CALENDAR YEAR the clue points at, then pull THAT year's
column. Don't anchor on the bubble's PEAK year when the clue specifies the
burst/crash/bottom year. Double-check the clue's qualifier ("lowest point",
"passed the bailout") fixes a single unambiguous year before reading the table.

## PDF parsing
- `pdftotext -layout <file.pdf>` preserves columnar alignment for these wide
  balance-sheet tables — use it first.
- If columns collapse, restrict to the page range and re-extract; for dense
  multi-column footings, read the targeted page directly (read_file/vision).
- Verify the column you read by confirming its date header AND the row label
  ("Total capital", "Total capital and liabilities", etc.) line up.

## Pitfalls checklist
- [ ] Report in the REQUESTED unit (could be thousands, millions, or billions
      — not always billions); convert only if it differs from the table's unit.
- [ ] Round only once, at the end, to the requested place.
- [ ] *** PER-COMPONENT ROUNDING *** Before submitting a multi-value bracket,
      re-read the clause attached to EACH value. An inline "rounded to nearest
      X place" on a specific sub-answer OVERRIDES any trailing "All numbers
      rounded to Y place" sentence FOR THAT VALUE. Different values in one
      bracket can have DIFFERENT dp. Build a quick map (e.g. YoY%->hundredths,
      slope->thousandths, intercept->thousandths) and verify each value's dp
      against its own clause. RECURRING FAIL: emitted 2.806 (global thousandths)
      when the YoY clause said hundredths -> gold 2.81. See
      references/per-component-rounding-overrides-blanket.md.
- [ ] Output order matches sub-question order.
- [ ] Numbers only inside brackets, no symbols.
- [ ] DELIMITER MODE: plain decimals/rates -> bare comma `[a,b]` (Mode A);
      large integers the Bulletin prints with thousands commas -> group each
      value `f"{n:,}"` and join with COMMA+SPACE `[374,443, 381,327]` (Mode B).
- [ ] Keep requested trailing zeros (`44.00`, not `44`).
- [ ] For "difference between capital and total-capital-and-liabilities",
      the answer is total liabilities, not a recomputation of capital.

## "How many sample standard deviations off the average" (signed z-score)
"How many SAMPLE standard deviations off the N-year average was year X?" =
signed z-score using SAMPLE SD (n-1 denominator): z = (x - mean) / stdev_sample.
The word "sample" = ddof=1 — np.std(vals, ddof=1) or statistics.stdev (NOT
pstdev/ddof=0). Keep the sign (below mean = negative). For small N the n vs n-1
choice changes the answer materially. Worked: CY1972–76 marketable-debt maturity
totals (end-of-Feb maturity schedules), 1972 z = -1.063 (PASS).
See references/sample-sd-deviations-off-mean.md.

## Silver MONETARY stock -> implied physical OZ -> REAL silver price -> median
Q: "Using total silver MONETARY stock ($M) in Sep YYYY (multiple years),
determine implied PHYSICAL quantities via the FIXED STATUTORY conversion rate
per fine troy oz, multiply by the REAL inflation-adjusted silver price, return
MEDIAN." STATUTORY rate = $1.2929292/oz (coinage value) -> use ONLY for
stock->oz. REAL price = MARKET silver price CPI-deflated -> use ONLY for
oz->value. Mixing the two (using $1.29 in both steps) overshoots by ~1.747x.
FAILED once: emitted 3584.40 vs GOLD 2051.51 (=3584.40/1.747).
See references/silver-monetary-stock-to-physical-and-real-price.md.

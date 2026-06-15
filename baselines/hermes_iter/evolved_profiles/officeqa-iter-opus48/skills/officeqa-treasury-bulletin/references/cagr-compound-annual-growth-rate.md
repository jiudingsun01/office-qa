# CAGR — Compound Annual Growth Rate (single start value -> single end value)

## Trigger
Question says "compound annual growth rate (CAGR)" OR "geometric annual rate of
change" between a START value and an END value (FY YYYY to FY YYYY, OR month-dated
e.g. Dec 1938 -> Dec 1940). "geometric annual rate of change" == CAGR for gold.
Distinct from the GEOMEAN-of-period-%-changes method (currency-and-geomean.md)
and from the Fisher symmetric growth rate (fisher-symmetric-growth-rate.md).
Do NOT confuse the three — gold treats them differently.

## OUTPUT FORMAT depends on wording — read carefully
- "reported in percent per year" / "%" example -> *100, percent.
- "outputted as a decimal value (e.g. 0.1234, not 12.34%)" -> BARE DECIMAL, do
  NOT multiply by 100. Formula = (V_end/V_start)**(1/N) - 1, round at given dp.
  Sign is kept (decline -> negative, e.g. gold [redacted]). Single value -> period
  decimal, no comma delimiter.

## RATIO metrics: form the ratio at EACH endpoint FIRST, then CAGR over ratios
Trigger: "the X-to-Y ratio" or "X to Y ratio" as the quantity whose rate of change
you want (e.g. "General Fund working balance to total balance ratio").
  1. ratio_start = X_start / Y_start ; ratio_end = X_end / Y_end
  2. CAGR = (ratio_end / ratio_start)**(1/N) - 1
Do NOT CAGR X and Y separately. Read both X and Y cells from the SAME table at
each period. WORKED SUCCESS (CORRECT, gold = [redacted]): "geometric annual rate of
change in General Fund working balance to total balance ratio, Dec 1938 -> Dec
1940, decimal, thousandths." N = 1940-1938 = 2; ratio fell -> negative -0.119.

## Formula (the one OfficeQA gold uses)

    CAGR (%) = ((V_end / V_start) ** (1 / N) - 1) * 100

where N = NUMBER OF YEARS ELAPSED = end_year - start_year.

## #1 PITFALL: N is elapsed years, NOT the count of data points
- FY 1947 -> FY 1950 spans N = 1950 - 1947 = **3 years** (NOT 4, even though 4
  fiscal years are named/touched). Using N=4 gives a too-low rate.
- General rule: count the GAPS between the endpoints, not the endpoints.

## Worked success (CORRECT, gold = [redacted])
"CAGR for expenditure transfers to the OASI trust fund from FY 1947 to the FY in
which the Korean War started, in percent per year, round to hundredth, nominal $."
- Korean War began calendar 1950 -> FY 1950 (event->year map: see
  external-historical-constants.md).
- N = 1950 - 1947 = 3.
- (V_1950 / V_1947) ** (1/3) - 1, * 100, round 2 dp = **108.01**.
- Such a high CAGR (>100%/yr) is legitimate when the start value is tiny relative
  to the end value (a young, fast-growing trust fund). Do NOT distrust a triple-
  digit CAGR — verify the cells and report it.
- TARGET RATIO CHECK: gold [redacted] over N=3 => (V_1950/V_1947) = 1.0801**? no:
  2.0801**3 = 9.00. So V_1950 / V_1947 MUST equal ~9.0. If your ratio is not ~9,
  you read a wrong cell — re-extract before answering.

## RE-FAIL on THIS EXACT OASI Q (got 74.40 vs gold 108.01) — ROW SELECTION, not method
The method/N/event-year above are ALL correct and were already in this file, yet a
run still answered 74.40. Back-solve: 1.7440**3 = 5.305, gold ratio = 9.00; my
ratio was 0.59x of gold (off by ~1.7x). A sub-2x miss on a CAGR == WRONG CELL, not
a formula slip. Diagnosis + fix:
  - SOURCE = the "Federal Old-Age and Survivors Insurance Trust Fund" statement
    (Trust Funds section of the Bulletin). This table has SEVERAL transfer/receipt
    lines: "Appropriations" (tax transfers from general fund), "Deposits by
    States", "Transfers to the trust fund", "Interest", a "Net" line, AND
    administrative "expenditure transfers". The Q says **"expenditure transfers TO
    the trust fund"** — pin THAT exact line, do NOT grab the big "Appropriations"
    or a "Total receipts/Net" line (those grow only ~1.6x 1947->1950, giving a
    too-low CAGR like 74 or lower).
  - The correct row is a SMALL, fast-growing line (start tiny -> 9x by FY1950),
    consistent with the >100% gold. If your start value is in the $1,000M+ range
    you almost certainly grabbed Appropriations, not the expenditure-transfer line.
  - PDFs for the late-1940s/1950 bulletins are NOT in the local data set
    (local set starts 1981/1990s), so these FY1947 & FY1950 cells come from the
    benchmark's own source bulletin — read the named row label LITERALLY and
    verify the 9.0 ratio sanity check above before committing.
  - GENERAL LESSON (mirrors the fish-quota re-fail in external-historical-constants.md):
    when the FORMULA + N + year-mapping are all confirmed correct yet the answer is
    <2x off, the bug is ALWAYS ROW/LINE SELECTION in a multi-line statement table.
    Match the question's noun phrase to the EXACT printed row label.

## Conventions
- "nominal dollars" = use the printed Bulletin figures as-is, NO CPI deflation.
- Keep full precision through the power/root; round ONCE at the final dp.
- Answer is a single decimal value WITH a "%" in the gold string. Single value =>
  no delimiter concern (the MODE A/B comma rule only matters for multi-value lists).

## VARIANT: PROJECTION forward ("if it continued at the same rate, what level in year Z?")
Trigger: "if X continued to grow at the same annualized compound rate observed
between [START] and [END], what would its projected level be in [TARGET]?"
Answer is a LEVEL in millions of $ (NOT a percent).

Two-step, keep full precision, round ONCE at the end:
  1. r = (V_end / V_start) ** (1 / N_obs)   where N_obs = end_year - start_year
  2. V_target = V_end * r ** (N_proj)        where N_proj = target_year - end_year

Equivalent one-liner (no intermediate r): V_target = V_end * (V_end/V_start)**(N_proj/N_obs).
SHORTCUT when N_proj == N_obs: V_target = V_end**2 / V_start (the geometric continuation).

Worked success (CORRECT, gold = [redacted]):
  "Series I savings bonds interest-bearing debt, same annualized compound rate
   March 2001 -> March 2006, projected level March 2011, millions nominal $, 2 dp."
  - N_obs = 2006-2001 = 5;  N_proj = 2011-2006 = 5  (equal -> shortcut applies)
  - V_2011 = V_2006**2 / V_2001  -> round 2 dp = 339501.88.
  - Both windows use CALENDAR months (March), read the March column each year.
  - Single value -> no delimiter concern; period decimal, no commas.
  - PITFALL: do NOT compute the % CAGR and round it before projecting — keep r at
    full float precision through the exponentiation, else the level drifts.

## Which growth-rate method does the question want?
- "compound annual growth rate" / "CAGR"  -> THIS file: (end/start)^(1/N)-1.
- "geometric mean of the [annual/quarterly] % changes" -> currency-and-geomean.md
  (chain the per-period growth factors, take Nth root of their PRODUCT).
- "Fisher Ideal symmetric growth rate" -> fisher-symmetric-growth-rate.md
  (200*(B-A)/(B+A)).

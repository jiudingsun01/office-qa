---
name: tb-budget-monthly-expenditures
description: Use for Treasury Bulletin questions about monthly (or fiscal-year) budget receipts or expenditures by category or by agency/department — e.g. "national defense and related activities", interest on the public debt, veterans, or "the highest spending Federal Department in fiscal year X" — including 12-month calendar sums, percent-contribution-of-a-source shares (e.g. individual income taxes / total receipts), and max/min-department lookups.
---

# Treasury Bulletin: monthly budget receipts & expenditures by category

## Where the data lives
- Recurring tables near the FRONT of each issue, in the fiscal/budget section: "Summary of Fiscal Operations" and "Budget Receipts and Expenditures" (titles vary slightly by era). Expenditure categories such as **"National defense and related activities"** appear as a column (or row) in the expenditures breakdown.
- Figures are **in millions of dollars** (1950s-era issues). Report nominal millions as printed.
- Rows are periods: several recent **fiscal years**, then the **individual months** of the current and prior fiscal year. The Bulletin's fiscal year runs **July–June**.

## Calendar-year questions span two fiscal years
- The 12 calendar months of year Y are split across FY Y (Jan–Jun) and FY Y+1 (Jul–Dec). No single fiscal-year total equals the calendar-year total — you MUST sum 12 monthly cells.
- Prefer ONE late issue whose monthly rows cover all 12 months (an issue from ~Feb–Apr of year Y+1 typically lists every month of calendar year Y), so all values come from a single vintage. If one issue doesn't reach back far enough, combine two issues and watch for revisions between vintages — when the question says "reported values", the printed monthly figures in the issue you use are what count.

## Procedure
1. Identify the category line/column exactly as printed (e.g. "National defense and related activities" — match loosely on "national defense" since OCR mangles the rest).
2. Extract each of the 12 monthly values into a list labeled by month; verify none is a fiscal-year or cumulative ("July to date") row — cumulative rows are much larger than monthly ones and usually sit adjacent.
3. **Mandatory reconciliation against the printed FY totals** (this is the #1 way a calendar-year sum goes wrong by a small amount). The 12 calendar months split into two fiscal years, and each half has an independent printed constraint:
   - Jan–Jun(Y) sum MUST equal `FY Y total − Jul–Dec(Y-1) sum` (both printed in the same/adjacent issue).
   - Jul–Dec(Y) sum is part of FY(Y+1); reconcile it via `FY(Y+1) total − Jan–Jun(Y+1) sum` when those months are available, or against the issue's running "July-to-date" cumulative column (Dec cumulative − Jun cumulative).
   If a half-year reconciliation is off by a SMALL amount (single digits / tens of millions), that is not rounding — it is one mis-OCR'd monthly cell in that half. Do NOT sum-and-ship; re-read each cell in the failing half digit-by-digit (a units digit like ...9 vs ...0, or a transposed digit, is the usual culprit) until the half reconciles exactly. An off-by-9-type error on a ~44,000 sum is a classic single-digit misread, fully catchable here.
4. Sum the 12 values and report in millions of nominal dollars (bare number unless a format is requested).

## Expenditures BY AGENCY / DEPARTMENT (e.g. "highest spending Federal Department")
- Besides the functional-category breakdown, the Bulletin carries an **"Expenditures by Agencies"** (a.k.a. by departments and agencies) table in the same front fiscal/budget section, with one column/row per cabinet department and major agency, in **millions of dollars**, with fiscal-year rows alongside monthly rows.
- For "highest/lowest spending Department in FY X": find the FY X row of that table and take the argmax across **Departments** only (exclude non-department lines like independent agencies, interest on the public debt, and the Total column).
- "Department" means a cabinet department (e.g. **Department of Defense**), NOT the functional category "National defense and related activities" — the two figures differ slightly. In the 1950s the Defense Department is invariably the largest (FY1955 ≈ 36,080), but verify against the printed row rather than assuming.
- Report nominal millions as printed (e.g. answer "36080" / "[redacted]"), no unit conversion.

## Modern era (2000s+) agency outlays "including budgetary and trust-fund flows"
- Wording like "figures that include both budgetary and trust fund flows" means the department's **TOTAL outlays (on-budget + off-budget/trust)** — the grand-total line for the agency, not a budget-accounts-only column or a sub-bureau line. For the **Department of Labor** this matters enormously: the Unemployment Trust Fund dominates DOL outlays (FY2011 total ≈ $133B, collapsing to ≈ $35B by FY2019 as UI spending wound down).
- Fiscal-year agency totals are revised between vintages. For each fiscal year endpoint, take the figure from the **final/year-end statement for that FY** (e.g. the September Monthly Treasury Statement Table 5 / the FY-end Treasury Bulletin issue), and pull BOTH endpoints the same way. Mixing a preliminary figure for one year with a revised figure for the other produces answers wrong in the third decimal of any derived rate.
- A derived-rate answer (CAGR, elasticity) that is close but off by a few thousandths almost always means one endpoint cell is from the wrong column (budget-only vs total) or wrong vintage — re-retrieve both cells from a second source before trusting the computation. Formulas for the CAGR/decay-factor/arc-elasticity triple live in tb-math-transform-wrappers.

## "Sum all agencies EXCEPT a few" — compute by SUBTRACTION from the printed Total, don't add up rows
- Questions like "total outlays for <month> across all listed agencies except Commerce, FEMA, and Interior, excluding undistributed offsetting receipts" should NOT be answered by manually adding 30+ agency rows — that is how you silently drop or mis-OCR one row (a single missed/misread agency shows up as an off-by-a-few-hundred error, e.g. 180222 vs correct [redacted]).
- The robust identity: the table's printed **Total outlays** = (sum of ALL agency rows) + (undistributed offsetting receipts, a NEGATIVE line). So:
  `sum(all agencies) = Total outlays − (undistributed offsetting receipts)`  ← subtracting a negative ADDS its magnitude back.
  Then `answer = sum(all agencies) − (the few excluded agencies' outlays)`.
- Procedure: read the printed **Total** cell for that month, read the **undistributed offsetting receipts** cell (carry its sign), and read ONLY the handful of excluded agency cells. Two-to-four lookups instead of thirty — far fewer chances to err.
- ALWAYS cross-check both ways: also sum the individual rows directly and confirm it equals the subtraction result. If they disagree, the difference pinpoints the dropped/misread agency row — find and fix it before answering. The two methods agreeing is your proof the row set is complete.
- "agency-specific entries only / exclude undistributed offsetting receipts or other non-agency items": these non-agency lines (undistributed offsetting receipts, and sometimes interest blocks) are exactly what the Total includes but the question wants removed — that's why the subtraction approach handles them cleanly: subtract each non-agency line out of the Total.

## Fiscal-year month windows differ by era
- 1950s-and-earlier issues: fiscal year runs **July–June** (FY1953 = Jul 1952–Jun 1953).
- Post-1976 (modern) issues: fiscal year runs **October–September** (FY1981 = Oct 1980–Sep 1981). Pulling Jul–Jun months for a modern FY silently grabs 3 wrong months and shifts every derived statistic.

## Dispersion stats over a year's 12 monthly values (e.g. "population standard deviation of monthly net outlays")
- "Use the latest table to include all of these monthly values in one place" is a sourcing instruction: pick ONE bulletin issue late enough that its monthly outlays/receipts table lists ALL 12 months of the target FY (an issue from a few months after the FY ends works) — don't stitch two vintages.
- In modern (1980s+) issues the monthly **"outlays by function"** table (FFO-series numbering) has monthly rows and a **total net outlays** column. "Std dev of monthly net outlays by function" means the dispersion across the **12 monthly TOTAL net outlays**, not across functions.
- Population std dev ⇒ divide by N=12: `python3 -c "import statistics; print(statistics.pstdev([...]))"` — NOT `statistics.stdev`. (See tb-security-price-volatility for the full pstdev/stdev pitfall.)
- Values stay in nominal millions as printed; round only the final statistic. Verified example: FY[redacted] monthly total net outlays, population std dev → **[redacted]** (accepted).
- **Calendar-year variant**: CY Y months span TWO modern fiscal years (Jan–Sep of Y are in FY Y, Oct–Dec of Y are in FY Y+1), so the FFO outlays table in one issue may show them in two separate fiscal-year panels/columns — pick an issue late enough (~spring of Y+1) that both panels are present, and pull Jan(Y)–Dec(Y) explicitly by month label, not by panel. Read FY vs CY in the question carefully: the SD differs hugely (FY1981 → 2760.44 vs CY1981 → **[redacted]**, both accepted) because a CY window straddles the year-over-year level jump.

## "Receipts from the public" / "payments to the public" (cash basis)
- These are **cash-basis** rows from the Bulletin's summary of cash transactions with the public (in/near the "Summary of Fiscal Operations" tables at the front), and are NOT the same as "net budget receipts" / "budget expenditures" (budget basis). Match the exact phrase the question uses; don't substitute one basis for the other.
- Monthly rows exist alongside fiscal-year rows, in millions of dollars, same layout conventions as above.

## WWII era (1941–1945) specifics
- The defense category is renamed mid-war: early-1941 issues print **"National defense"**; from ~1942 it becomes **"War activities"**. Treat them as one series — a question about "national defense expenditures" in 1942–43 means the "War activities" line. Pre-war (1940) issues likewise print plain **"National defense"**; by the 1950s it is "National defense and related activities". All are the same series for question-matching purposes.
- Cross-era comparisons (e.g. CY1940 vs CY1953): pull each calendar year's 12 months from an issue of ITS OWN era — a ~early-1941 issue for CY1940, a ~early-1954 issue for CY1953. No single issue spans both; do two independent 12-month extractions and sums.
- Receipts side: "total net budget receipts" = total receipts **minus the net appropriation to the Federal old-age insurance trust fund** — take the line labeled "Net receipts", not gross "Total receipts".
- Spending grew ~5–15% **per month** in 1941–43, so one misplaced cell (a cumulative "July 1 to date" value grabbed instead of a monthly one, or a month from the wrong year) shifts a calendar-year total by 2x. The 1940s monthly tables print monthly and fiscal-year-cumulative columns SIDE BY SIDE — extract the monthly column only, list all 12 values, and check they rise roughly monotonically through 1941–43 before summing.
- Sanity anchors (calendar year, millions): CY1941 net receipts ≈ 9,000 vs defense ≈ 7,000–8,000 → ratio **above 1**; CY1943 receipts ≈ 22,000–25,000 vs war expenditures ≈ 75,000–85,000 → ratio ≈ 0.3. If a computed CY1941 receipts/defense ratio comes out below 1, the defense figure is almost certainly inflated — re-extract it.

## Historical cross-decade category comparisons (e.g. "public works in 1934 vs 1946")
- When a question compares one expenditure category across far-apart fiscal years (1930s vs 1940s), do NOT sum months or combine two contemporaneous issues. Postwar Bulletins carry a **historical fiscal-year table** of expenditures by major classification (rows like Public works, National defense/War activities, Veterans, Interest...) covering many years back into the 1930s. Pull BOTH years from that one table in one late issue so the figures share a vintage.
- The phrase **"revised figures"** is itself a vintage instruction: use the later (e.g. 1946–47) issue's restated series, not the numbers printed contemporaneously in the earlier year's own bulletin — classifications were redefined after the war and the two vintages disagree.
- When the question describes what the series should **include/exclude** ("should account for PWA spending and housing", "exclude certain wartime spending"), that is a row-selection key: the table prints multiple variants of the same-named category (e.g. "Public works" with and without war facilities), distinguished by **footnotes**. Match the question's include/exclude clause against the footnote text, not just the row label.
- "Absolute difference ... in millions of nominal dollars" = |value(yearA) − value(yearB)| of the printed millions, reported as a positive bare number.

## Receipts by source & "percent contribution" share-change questions
- Modern (1980s+) bulletins carry a **"Budget Receipts by Source"** table (FFO-2 era numbering) alongside the outlays tables: columns/rows for **individual income taxes, corporation income taxes, social insurance taxes, excise, estate & gift, customs, miscellaneous**, plus **total receipts** — with fiscal-year rows and monthly rows, in millions. When the question says "net" individual income taxes, that is the standard receipts figure (gross minus refunds) — match the printed label rather than re-deriving.
- "Percent contribution of X to total receipts in CY Y" = (12-month CY sum of X) / (12-month CY sum of TOTAL receipts) × 100. Sum BOTH numerator and denominator over the same 12 calendar months from the same vintage — don't pair a CY sum of X with a fiscal-year total.
- "Change in percent contribution from CY Y1 to CY Y2" = share(Y2) − share(Y1), a **signed difference in percentage points** (e.g. "4.61"). It is NOT a percent change of the share — do not divide by share(Y1).
- Keep full precision in each share; round ONLY the final difference to the requested decimals — rounding the monthly sums or the individual shares first can flip the hundredths digit.

## Multi-year ratio/mean questions
- "Mean of the ratios of A to B for each of years Y1–Yn" = compute A/B **separately per year, then average the ratios**. Do NOT compute sum(A)/sum(B) — with a fast-growing denominator (WWII defense) the two differ enormously (≈0.68 vs ≈0.36 for 1941–43).
- Write out each year's numerator, denominator, and ratio before averaging; one bad year is the usual failure mode and is only visible that way.
- **MANDATORY before averaging: check every per-year ratio against the era anchors below.** A mean that lands well between the per-year and sum-of-ratios values (e.g. ~0.48 for 1941–43, vs the correct ~0.68) is the signature of ONE collapsed year's ratio dragging the average down — almost always the earliest year, whose defense denominator got inflated (a cumulative "July-to-date" cell grabbed instead of monthly, or the wrong column). Do not average until each ratio matches its anchor; fix the offending year first. The mean is NOT robust here — a single wrong year shifts it ~0.2.

## Pitfalls
- Do NOT use the fiscal-year total row as a shortcut for a calendar year.
- Don't mix "net" vs "gross" expenditure variants or pick the "Total expenditures" column when a specific category is asked.
- Monthly tables sometimes show a "Total —— fiscal year 19XX" subtotal between June and July rows; exclude it from the 12-month sum.
- "Absolute percent change" between two years' sums = |later − earlier| / **earlier** × 100, reported as a positive percent (e.g. "[redacted]"). The base is always the earlier year; sum the raw monthly cells first and round ONLY the final percent (intermediate rounding of the sums can shift the hundredths digit).
- **When the percent change is huge (hundreds/thousands of %), the EARLIER year is a small denominator and dominates the result's precision.** A 1-in-1000 error in the base year moves the answer by ~1 percentage point at the hundredths place. So spend MOST of your reconciliation effort on the earlier/smaller year's 12 cells: re-read each digit-by-digit and reconcile both half-years against their printed FY totals BEFORE trusting the final percent. (CY1940 vs CY1953 national defense → **[redacted]**; an answer like 1608.26 that is right to the integer but off in the first decimal is the signature of ONE mis-OCR'd cell in the 1940 base — not a rounding choice.)

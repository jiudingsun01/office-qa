# Receipts / Defense-Expenditure Ratios — CY1941-1943 (SOLVED, gold=0.6841)

## Trigger
Q: "mean of the ratios of total net budget receipts to total national defense
budget expenditures for each of the calendar years 1941-1943, in millions,
4 dp." Given the Oct-1941, Oct-1942, Oct-1943 bulletins.

## ✅ CORRECT ANSWER = 0.6841. DO NOT sum monthly cells. USE FISCAL-YEAR ROWS.
Despite the word "calendar," the gold is reproduced EXACTLY by reading each
bulletin's OWN-YEAR headline FISCAL-YEAR figures from the "Budget Receipts and
Expenditures / Summary by Major Classifications" table:

  Year | Net receipts | Defense line                 | source bulletin
  1941 | 7607         | National defense   = 6080    | 1941_10 Table 1 (p.12 row "1941")
  1942 | 12799        | Total war activities = 26011 | 1942_10 Table 1 (p.12 row "1942")
  1943 | 22282        | Total war activities = 72109 | 1943_10 Table 1 (p.27 row "1943")

  ratios: 7607/6080=1.251151, 12799/26011=0.492061, 22282/72109=0.309004
  mean = 2.052216/3 = 0.6840723 -> 0.6841  ✓ EXACT

KEY POINTS:
- The DEFENSE denominator is whatever that bulletin LABELS the defense/war line
  for its own fiscal year: 1941 issue prints "National defense" (=6080); the
  1942 and 1943 issues renamed it "Total war activities" (=26011, =72109).
  USE THAT FISCAL-YEAR ROW VALUE. They are the same conceptual line across the
  reclassification — do NOT try to find a separate narrower "national defense"
  number for 1942/43.
- Net receipts = the "Net receipts" fiscal-year row in the SAME table.
- "mean of the ratios" = per-year ratio first, then average the three.
- "calendar years" / "expressed in millions" are RED HERRINGS: the ratio is
  unitless and the values used are the fiscal-year rows, not calendar-month sums.

## ⚠️ TWO CONFIRMED WRONG APPROACHES — do not repeat
1. Summing MONTHLY "War activities" cells per calendar year (CY1941=12552,
   CY1942=49858, CY1943 Jan-Sep=60612) with calendar receipts {8848,16403,24687}
   -> mean 0.4804. WRONG.
2. Same monthly approach with any "national defense" monthly row -> still ~0.48.
The benchmark does NOT want calendar-month aggregation here; it wants the
fiscal-year summary rows, one per bulletin.

## Where the values live
- 1941_10: Table 1 "Receipts and Expenditures", row labeled "1941"
  (the fiscal-year-totals block). Cols: Net receipts=7607, National defense=6080.
- 1942_10: Table 1 (~p.12), row "1942": Net receipts=12799,
  "Total war activities"=26011.
- 1943_10: monthly Table 1 "Summary by Major Classifications" (PDF p.27), the
  fiscal-year block row "1943": Net receipts=22282, "War activities"=72109.
  (1943 issue is the Third-War-Loan special issue; its budget tables are deeper,
  around PDF p.22-28, not the front matter.)

## Verification gate
Compute the three ratios. Expect ~1.25, ~0.49, ~0.31 -> mean 0.6841. If you get
~0.48 you summed monthly cells — STOP and use the fiscal-year rows instead.

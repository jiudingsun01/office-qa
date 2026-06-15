---
name: tb-irs-collections
description: Use for Treasury Bulletin questions about Internal Revenue collections by source — total collections reported by the IRS, corporation/individual income taxes, employment taxes (old-age, railroad retirement, unemployment insurance), estate/gift, excise — for any fiscal year or month. Also contains the cross-bulletin OCR cross-check tactic that applies to ANY single-cell lookup feeding a sensitive computation (elasticity, ratio, % change).
---

# IRS Internal Revenue Collections table

## Where the data lives
- Every bulletin has a section "INTERNAL REVENUE COLLECTIONS", "Table 1.- Summary by Principal Sources", in **thousands of dollars**. In the parsed txt files, find it with `grep -n "Total collections reported by Internal Revenue"`.
- Columns: Budget receipts from internal revenue | Adjustment of collections to budget receipts | **Total collections reported by IRS** | Corporation income & profits taxes | Total (indiv. income + employment) | Indiv. not withheld | Indiv. withheld | Old-age and disability insurance | Railroad retirement | **Unemployment insurance** | then (often a second sub-table) Estate & gift | Excise...
- For monthly rows from ~1955 on, the Adjustment is blank and "Budget receipts" == "Total collections reported by IRS" (same number in both columns). For full fiscal years they differ — use the column the question names.

## Column-shift pitfall (monthly rows)
In the printed table, **"Old-age and disability insurance" has NO monthly figure** (footnote: it's included in withheld/not-withheld for months). Parsers handle this blank inconsistently across bulletin issues:
- Some issues: `... withheld | nan | <railroad> | <unemployment>` (values in labeled columns).
- Other issues: `... withheld | <railroad> | <unemployment> | nan` (values shifted left into the old-age/railroad headers, last column nan).
So identify the unemployment-insurance value as the **last non-nan numeric in the employment-tax block**, not by header position. Sanity check: monthly railroad retirement is ~15k–90k with peaks in Feb/May/Aug/Nov; monthly unemployment insurance is tiny (<3k) most months but spikes in Jan–Feb and the month after each calendar quarter (FUTA/SUTA filing).

## Cross-bulletin OCR cross-check (general tactic)
Parsed bulletin txt files contain single-digit OCR errors (e.g. the same monthly cell may appear as "20174" in one parse and "20974" in another but correctly elsewhere).
- Any given month appears in ~12+ consecutive bulletin issues (and fiscal years in many more). Before using a value in a sensitive computation, **grep the SAME cell in 2–4 other issues and take the majority value**:
  `for f in 1960_06 1960_07 1960_09 1960_12; do grep -A30 "Total collections reported by Internal Revenue" .../treasury_bulletin_$f.txt | grep "Mar"; done`
- This matters most when the value is a small denominator or enters a difference of similar-sized numbers — a one-digit error can swing an arc elasticity substantially.
- If issues disagree with no clear majority, open the source PDF page for the tie-break.

## Arc elasticity reminder
Arc (midpoint) elasticity of Y w.r.t. X between two periods:
`[(Y2−Y1)/((Y1+Y2)/2)] / [(X2−X1)/((X1+X2)/2)]` — keep full precision until the final 3-decimal rounding.

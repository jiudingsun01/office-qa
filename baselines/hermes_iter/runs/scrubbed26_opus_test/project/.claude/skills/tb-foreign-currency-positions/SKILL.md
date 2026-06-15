---
name: tb-foreign-currency-positions
description: Use for Treasury Bulletin questions about foreign-currency positions reported by banks or NONBANKING firms/business concerns — positions in Belgian francs, Canadian dollars, German marks, Swiss francs, etc., in millions of foreign-currency units, usually at quarter-end dates — including any statistic computed across several quarters (correlation, mean, change).
---

# Treasury Bulletin: Foreign Currency Positions (banks & nonbanking firms)

## Where the data lives
- Section "Foreign Currency Positions" near the back of mid/late-1970s+ Treasury Bulletins, table series **FCP** (e.g. FCP-II for nonbanking firms). Each currency (Belgian franc, Canadian dollar, French franc, German mark, Italian lira, Japanese yen, Swiss franc, pound sterling) has its **own sub-table**, with one row per reporting date.
- Reporting dates are **quarter-ends**: when a question says "calendar months December 1975, March 1976, June 1976, September 1976" it means the rows dated 12/31/75, 3/31/76, 6/30/76, 9/30/76.
- Values are in **millions of the foreign currency itself** ("millions of current foreign-currency units"), NOT dollars. The dollar exchange rate is a separate column — do not use it unless asked.
- Pick the column the question names ("positions" without qualifier usually = the net/overall position column; assets and liabilities are separate columns).

## Critical pitfall: revisions across issues
Quarterly FCP figures are **revised in later bulletins**. A bulletin shows the latest few quarters; an early issue carries a preliminary figure that a later issue revises slightly. With only 4 data points, a one-unit difference in a single cell moves a Pearson correlation in the 4th decimal place.
1. Find ONE bulletin issue whose FCP table spans **all** requested dates in a single table, and take every value from that one issue (consistent vintage).
2. Prefer the issue where the requested dates are the OLDEST rows shown (i.e., fully revised), not the newest (preliminary, often footnoted "p" or "r").
3. Cross-check each cell against a second issue (the cross-bulletin OCR cross-check in `tb-irs-collections`). If two issues disagree, use the later issue's value.

## Diagnosing a far-off correlation
If your r comes out far from a plausible value, you likely read the WRONG cells rather than missing a revision subtlety. Diagnose in this order:
1. **Wrong column.** The nonbanking FCP sub-table has multiple columns (assets, liabilities, net position). "Positions" with no qualifier = the **net/overall position** column. Picking assets-only or liabilities-only flips the correlation by tenths.
2. **Wrong currency sub-table or wrong rows.** Confirm you are in the correct currency sub-tables, reading the quarter-end rows (e.g. 12/31/75, 3/31/76, 6/30/76, 9/30/76) — not adjacent months/quarters.
3. Only AFTER r is in the plausible ballpark do the ±1-unit revision check for the 4th decimal.

## Computing Pearson r on n=4 quarters
- Keep ALL digits as printed; never round intermediates.
- r = [n·Σxy − Σx·Σy] / sqrt{[n·Σx² − (Σx)²]·[n·Σy² − (Σy)²]} — do it in Python, not by hand.
- Sanity check: recompute after perturbing each cell by ±1 in the last printed digit; if the 4th decimal of r changes, your cell reads MUST be verified against a second source before answering.
- Round only the final r to the requested decimals.

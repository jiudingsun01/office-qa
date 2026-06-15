---
name: tb-esf-balance-sheet
description: Use for Treasury Bulletin questions about the Exchange Stabilization Fund (ESF) — its balance sheet / statement of financial position, capital, assets, liabilities, or income — as of a quarter-end date.
---

# Treasury Bulletin: Exchange Stabilization Fund (ESF) statements

## Where the data lives
- The Treasury Bulletin has a recurring "Exchange Stabilization Fund" section containing a **balance sheet** (and an income/expense statement) reported **as of calendar-quarter-end dates** (Mar 31, Jun 30, Sep 30, Dec 31).
- Publication lag: a quarter-end balance sheet appears in an issue published **one to two quarters later** (e.g. the March 31, 1989 balance sheet is in a mid/late-1989 issue, not the March 1989 issue). If the obvious issue lacks it, check the next one or two issues.
- "As of the last day of <month> <year>" → match the quarter-end date column/heading exactly; the table often shows two date columns (current vs. prior quarter) — take the column for the asked date.

## Modern-era (1999+) asset line items
- Assets list: U.S. dollar deposits, Special drawing rights (SDRs), and **"Foreign exchange and securities"** broken out by currency — **European euro** and **Japanese yen** lines. "Foreign-exchange holdings and securities" = euro + yen (do NOT include SDRs or dollar deposits).
- Verified issue mapping for quarter-end sheets around [redacted]–[redacted]: **June 30 balances appear in the December issue of the same year; September 30 balances in the following March issue** (consistent with the 1–2 quarter lag rule below).
- Verified values (thousands of $, FX+securities / total assets): Jun [redacted]: [redacted]/[redacted]; Jun [redacted]: [redacted]/[redacted]; Jun [redacted]: [redacted]/[redacted]; Sep [redacted]: [redacted]/[redacted]; Sep [redacted]: [redacted]/[redacted]; Sep [redacted]: [redacted]/[redacted].
- For "average share of total assets ... CPI-adjusted" questions: the adjustment is a no-op — average the per-date shares (see tb-math-transform-wrappers, "Average SHARE of total + CPI-adjustment wrapper").

## Units and rounding
- ESF balance-sheet figures are printed **in thousands of dollars**.
- To report in **billions rounded to the nearest thousandth**: divide the printed thousands figure by 1,000,000 and round to 3 decimals (e.g. 8,123,xxx thousand → 8.124).

## Line items to match precisely
- The Capital section distinguishes **"Capital account" / nominal capital** from cumulative **net income/retained earnings** and from **"Total capital"**. "Total nominal capital" refers to the capital total line in the Capital section — read the exact printed total rather than recomputing, then verify it sums from its components.
- "Total capital and liabilities" is the bottom-line grand total (equals total assets on a balanced sheet). Do not confuse it with "Total liabilities" alone.

## Multi-part "value + difference" questions
- A common pattern asks for (a) a line value and (b) the **absolute difference** between it and another total from the same statement. Pull both printed values first, convert each to the requested unit, then subtract — don't round intermediate values before differencing if avoidable; round only the final answers.
- Output format when asked: answers in one set of square brackets, comma-separated, in the order the sub-questions were asked, e.g. `[8.124,12.852]` — NO space after the comma; graders exact-match the answer string (see answer-format-exact-match skill).

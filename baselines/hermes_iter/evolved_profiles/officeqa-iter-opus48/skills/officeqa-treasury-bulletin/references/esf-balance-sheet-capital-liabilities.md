# ESF balance sheet: Capital subtotal vs "Total capital and liabilities"

## Question shape
"What is the **total nominal capital** held per the Exchange Stabilization Fund
(ESF) Balance Sheet as of the last day of <Month YYYY>, and what is the
**absolute difference** of this value with the **total capital and liabilities**
recorded as of this date? Report both in billions, rounded to nearest thousandth."

Example: as of March 31, 1989 -> gold [8.124, 12.852]. CORRECT first try.

## Balance-sheet structure (the whole trick)
The ESF balance sheet (Treasury Bulletin "Exchange Stabilization Fund" section,
under International / Capital Movements statistics) is laid out as:

  ASSETS                          LIABILITIES AND CAPITAL
   ... asset lines ...             Liabilities
   Total assets ........ X          ... liability lines ...
                                    Total liabilities ..... L
                                   Capital
                                    ... capital lines ...
                                    Total capital ......... C
                                   Total capital and
                                     liabilities ......... X   (= Total assets)

Three distinct grand/subtotal lines that are EASY to confuse:
- **Total capital** (C)  — capital section subtotal ONLY (e.g. 8.124 B).
- **Total liabilities** (L) — liability section subtotal.
- **Total capital and liabilities** (X) — the grand total of the right-hand
  side; by balance-sheet identity X = Total assets, and X = C + L.

KEY IDENTITY: abs(Total capital - Total capital&liabilities) = abs(C - X) = L
  i.e. the requested absolute difference IS just total liabilities.
  Here 12.852 = X - C = total liabilities (X = 8.124 + 12.852 = 20.976 B assets).

## Procedure
1. Open the bulletin issue that reports the requested quarter-end (Mar 31 ->
   the issue carrying the March 31 column; ESF is reported quarterly). Find the
   "Exchange Stabilization Fund" balance-sheet statement.
2. Read the EXACT named line items off the right-hand (Liabilities & Capital)
   side for the requested period-end column:
   - sub-Q1 = "Total capital" line (the CAPITAL subtotal — NOT "Total capital
     and liabilities", NOT "Total liabilities").
   - sub-Q2 = abs(Total capital - "Total capital and liabilities").
3. Units: ESF balance sheet is in **thousands of dollars** (or millions — CHECK
   the column header). To billions: thousands ÷ 1,000,000 ; millions ÷ 1,000.
4. Round each to nearest thousandth, ROUND_HALF_UP.

## Pitfalls
- Do NOT grab "Total capital and liabilities" when only "Total capital" is asked.
  They differ by total liabilities (often the larger number).
- The right-hand grand total equals Total assets — sanity check: C + L should
  match Total assets on the left side. If it doesn't, you mis-read a line.
- Watch the unit header (thousands vs millions). Getting the answer off by 1000x
  means wrong scaling, not wrong cells.
- "last day of March" = the March 31 column, not a prior-period column shown in
  the same issue.

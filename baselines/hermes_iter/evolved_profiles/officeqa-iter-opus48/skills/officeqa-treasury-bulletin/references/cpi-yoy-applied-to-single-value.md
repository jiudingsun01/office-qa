# Inflation-adjust a Treasury Bulletin dollar value by CPI-U (single value OR MoM)

## Pattern A — single value, YoY rate
"Apply the official BLS CPI-U year-over-year inflation rate for calendar month
MMM YYYY to the [Treasury Bulletin dollar value] at the end of the same fiscal
month, rounded to ... in millions of dollars."

NOT the share/ratio case (where CPI cancels). A single nominal value is scaled:

    answer = value_MMMYYYY * (1 + r_yoy)
    r_yoy  = CPI_U(MMM YYYY) / CPI_U(MMM YYYY-1) - 1   (same calendar month, prior year)

Use BLS CPI-U, U.S. city average, ALL items, NSA, MONTHLY index (1982-84=100).
Carry full precision; round only the final millions value.

### EXACT CPI-U index anchors (NSA, 1982-84=100) — use these literally
Getting the CPI pair off by even 0.1 index point produces a near-miss that
GRADES WRONG (digits ~99.97% right). Pin the official monthly values:
- Nov 1969 = 38.8 ; Nov 1968 = 36.8  ->  r_yoy = 38.8/36.8 - 1 = 0.054348 (5.4348%)
- (Do NOT interpolate, do NOT use SA series, do NOT use annual averages.)
WORKED FAILURE (Nov 1969 total currency in circulation): base value =
53224.845M, gold = 53224.845 * 38.8/36.8 = 56117.5. I got 56134.5 by using a
slightly off rate (5.467% vs 5.4348%) — same row, same base, WRONG CPI index.
Ratio to gold was 1.0003x (NOT a clean ratio) => the tell for a CPI-index slip,
as opposed to a wrong-row error (which gives a clean ~1.1x / 2.3x ratio).
NOTE: the base currency figure is NOT round — it was 53224.845 (carries
decimals). Read the full-precision table cell, don't truncate to 53225.

## Pattern B — month-over-month change in REAL dollars (ASYMMETRIC!)
"month-over-month change in [LINE] in millions of June 1979 dollars when using
CPI-U to adjust the May 1979 [LINE] value to June 1979 real dollars."

ONLY the PRIOR month is rescaled to the current month's price level. Current
month stays nominal. The formula is asymmetric:

    answer = value_JUN_nominal - ( value_MAY_nominal * CPI_U(Jun)/CPI_U(May) )

- Use the SAME-MONTH consecutive CPI ratio (Jun/May), NOT a YoY ratio.
- Do NOT scale BOTH months by the ratio (that would just give ratio*(nominal MoM)).
- Do NOT adjust June (it is already the target/real base month).
- DANGER: when the nominal MoM is small, the adjustment term
  value_MAY*(ratio-1) DOMINATES the answer. CPI(Jun1979)/CPI(May1979) ≈
  216.6/214.1 ≈ 1.01168, so the term ≈ 116.8 per 10,000 of the May value. A
  WRONG base row therefore swings the answer wildly — base-row selection is the
  #1 error, not the CPI math.
- WORKED FAILURE->NOW-PASS (Jun 1979 Federal Reserve notes, MoM real-$):
  gold = -156.11. EARLIER got -362.45 (sign right, ~2.32x too large) by a
  wrong-base/ratio-to-both-months slip. LATER re-run got -156.11 CORRECT using
  Pattern B exactly: answer = FRN_Jun_nominal - FRN_May_nominal*CPI(Jun)/CPI(May),
  reading the FEDERAL RESERVE NOTES component row, rescaling ONLY May. This
  validates the asymmetric formula + literal-row rule. If you reproduce
  -156.11 you are done; a ~2.3x blow-up means base-row/both-months error.

## #1 FAILURE MODE: wrong ROW — match the row to the EXACT line the Q names (BIDIRECTIONAL)
The CPI math is easy and usually RIGHT. The graded-wrong error is reading the
wrong cell of the currency table. The rule cuts BOTH ways:
- Q says "TOTAL currency in circulation" -> read the GRAND-TOTAL/footer row.
  Do NOT read "Federal Reserve notes" or any single component. (Nov 1969:
  total ~$53.3B, NOT FRN ~$46.7B.)
- Q says "Federal Reserve notes" -> read the FEDERAL RESERVE NOTES component
  row literally. Do NOT read the total currency / total-in-circulation row, and
  do NOT sum components.
Always read the row whose label is the EXACT noun phrase in the question.

## DIAGNOSTIC
If a CPI-adjusted answer is a clean fixed ratio off the gold (e.g. ~1.14x, or
~2.3x), the rate/method is fine and you grabbed the WRONG ROW (or, for Pattern
B, applied the ratio to the wrong/both months). Re-open the table and read the
row literally labeled by the question's exact line item, for the exact month
column(s). For Pattern B confirm only the PRIOR month was rescaled.

## Where the figure lives
Treasury Bulletin "Currency and Coin" / "Currency in Circulation" section. The
table breaks circulation into Federal Reserve notes, U.S. notes, coin, etc.,
with a TOTAL row. Read the month-end column(s) for the stated fiscal month and
the row matching the question's exact wording. Values in millions of dollars.

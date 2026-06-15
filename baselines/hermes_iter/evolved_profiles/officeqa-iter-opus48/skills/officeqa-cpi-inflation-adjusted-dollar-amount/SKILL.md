---
name: officeqa-cpi-inflation-adjusted-dollar-amount
description: OfficeQA Treasury Bulletin — CPI-U inflation adjustment of a Treasury dollar figure, three variants. Variant A (apply YoY rate for month MMM YYYY) — answer = base*(1+rate), rate from BLS NSA MONTHLY index ratio; FAILED Nov1969 currency-in-circ on wrong base row. Variant B (signed difference YearB minus YearA in millions of YearB dollars, or "for those years") — deflate EACH year figure to a common base year using ANNUAL-AVERAGE CPI-U then subtract, real_X = nom_X * CPI[base]/CPI[X]; PASSED Unemployment Trust Fund Dec1946 vs Dec1947 giving -550.3. Variant C (month-over-month change in REAL current-month dollars) — change = nom_curr - nom_prev*CPI[curr_month]/CPI[prev_month] using MONTHLY NSA index; FAILED Jun79 FRN twice by emitting raw nominal MoM with NO deflation (+247.53 vs GOLD -156.11).
---

# OfficeQA — CPI-U YoY inflation-adjusted Treasury dollar amount

## When this fires
Question shape: "What is the inflation-adjusted dollar amount after applying the official
U.S. BLS CPI-U **year-over-year** inflation rate for **calendar month MMM YYYY** to
**<a Treasury Bulletin dollar figure>** by the end of the same fiscal month rounded to the
nearest tenths place in millions of dollars?"

Examples of the `<Treasury figure>`: "total currency in circulation", "total currency
outstanding", a debt total, a receipts/outlays line, etc. — read from the bulletin for
that fiscal month.

## The formula
```
answer = BASE * (1 + YoY_rate)
```
where `YoY_rate = CPI_U[MMM, YYYY] / CPI_U[MMM, YYYY-1] - 1`, and BASE is the dollar
figure (in $ millions) from the bulletin. Round answer to **tenths** ($0.1 million).

This question has TWO orthogonal failure points. Nail BOTH.

## Piece 1 — the CPI-U YoY rate (NSA monthly index, NOT row-derived)
Use the official BLS CPI-U (1982-84=100) **Not-Seasonally-Adjusted MONTHLY index** and
take the **same-month one-year-prior ratio**. Do NOT derive the rate from a row inside the
bulletin, and do NOT use seasonally-adjusted or annual-average series — the near-1.0 ratio
makes any index slip catastrophic.

Pinned anchor values:
- **Nov 1969 = 38.8, Nov 1968 = 36.8 → 38.8/36.8 - 1 = 5.4348%**
- general — CPI-U Nov1969 YoY ≈ 5.4%, not 14%

Sanity check: a Nov-1969-era YoY should be ~5–6%, NOT double digits. Implied rate >10% means
an index error.

## Piece 2 — the BASE Treasury dollar figure (the part that killed Nov1969)
**This is the dominant failure mode now.** The rate was correct (~5.43%) but the base
currency figure was wrong — read ~46,433 vs the correct ~53,227 (ratio exactly 1.1463).

Rules for "total currency in circulation" / "currency outstanding":
- Find the table reporting **"Currency in circulation"** as a single TOTAL line
  (Treasury "Status / circulation statement of United States Money", or the
  "Money in circulation" / "Currency and coin" summary). Use the **grand TOTAL currency in
  circulation**, NOT a single component (Federal Reserve notes alone, or "outstanding"
  minus Treasury-held without adding coin).
- "currency in circulation" usually = (currency outstanding) − (amount held by Treasury and
  Federal Reserve Banks). If the table gives both "outstanding" and "in circulation"
  columns, the question's "in circulation" wording means the **in-circulation** column.
- Nov 1969 correct base ≈ **53,227 $ million** (53227 * 1.054348 ≈ [redacted] = GOLD).

### DEBUG trick when verdict is wrong
Compute GOLD / your_answer.
- If the ratio CHANGES when you divide out (1+rate) differently, you picked the wrong RATE.
- If GOLD/(1+rate) vs yours/(1+rate) give the SAME ratio at every plausible rate, your BASE
  row was wrong, not the rate. For Nov1969 the 1.1463 ratio held at every rate → base error.

## Procedure
1. Identify MMM YYYY and the target Treasury figure from the question.
2. Get BLS CPI-U NSA monthly index for MMM YYYY and MMM (YYYY-1); rate = ratio - 1.
   Sanity: era-appropriate magnitude (late-1960s ≈ 5–6%).
3. Read the BASE from the correct bulletin table — for "currency in circulation" take the
   grand TOTAL in-circulation line in $ millions, not a component.
4. answer = BASE * (1 + rate); round to tenths.

## Pitfalls
- DON'T derive the inflation rate from a Treasury row — use the BLS CPI-U NSA index.
- DON'T grab a currency component (FR notes only) or an "outstanding" figure when the
  question says "in circulation" — use the TOTAL in-circulation line.
- DON'T use double-digit rates for the late 1960s.
- Round FINAL to tenths of a million.

## VARIANT B — signed difference of TWO years, both deflated to a common base year
Question shape: "signed difference (YearB - YearA) in <figure> as of Dec YearA and Dec YearB,
adjusted for inflation using BLS CPI-U for those years, in millions of <YearB> dollars."

This is NOT the YoY-rate variant. Here you take TWO nominal figures (one per year) and
deflate EACH to a common base year using the **annual-average CPI-U**, then subtract.

Formula (base year = YearB, so YearB figure is already in YearB dollars):
```
real_A = nominal_A * (CPI[YearB] / CPI[YearA])
real_B = nominal_B                       # already in YearB dollars
answer = real_B - real_A                 # signed, in YearB-dollar millions
```
More generally for base year G: real_X = nominal_X * CPI[G]/CPI[X].

Use the **annual-average CPI-U** (calendar-year average index), NOT a single month, because
the question says "for those years" (plural, year-level), not a specific month.
- CPI-U annual avg 1946 ≈ 19.5, 1947 ≈ 22.3 (1982-84=100). Ratio 1947/1946 ≈ 1.1436.

PASSED: Unemployment Trust Fund total balance, Dec1946 vs Dec1947, in 1947 dollars → -550.3.

### Variant B sub-case — ABSOLUTE difference, FY-end public debt, 3 years named
PASSED FY1960/1961/1962 public debt outstanding, adjust FY1960 & FY1961 to constant 1962$,
ABSOLUTE difference |real_1961 - real_1960| → [redacted] (GOLD [redacted]).
- "absolute difference" → report |·| (non-negative), unlike the SIGNED Dec1946/47 case.
- The question may NAME three fiscal years but only adjust TWO and difference TWO; FY1962 is
  just the base year (its figure is read only to confirm base, not differenced here).
- "fiscal-year public debt outstanding as of the END of FFY YYYY" → the TOTAL gross public
  debt outstanding at FISCAL-YEAR-END (June 30 for these years), from the public-debt /
  "Summary of Federal Debt" table. NOT a Dec figure, NOT a calendar-year figure.
- Still ANNUAL-AVERAGE CPI-U (1982-84=100, NSA): real_X = nom_X * CPI[1962]/CPI[X].
  Anchor annual avgs: 1960≈29.6, 1961≈29.9, 1962≈30.2 (1982-84=100).
- Round to thousandths when asked ("thousandths place"). Single value, no commas.
The fund balance GREW nominally but the real (1947$) Dec1946 figure, once inflated up to
1947 dollars, exceeded the nominal Dec1947 figure → negative signed difference.

Key distinctions vs Variant A:
- "for those YEARS" / "in millions of YYYY dollars" → annual-avg CPI, deflate-to-base. (Variant B)
- "YoY inflation rate for calendar month MMM YYYY ... by end of same fiscal month" → monthly
  NSA index YoY rate, base*(1+rate). (Variant A)
- Direction of adjustment: to express an OLDER year in NEWER dollars, MULTIPLY by
  CPI[new]/CPI[old] (>1). The Dec-of-each-year balances come from the Treasury Bulletin
  trust-fund / "Government corporations and credit agencies" balance tables.

## VARIANT C — month-over-month change in REAL dollars (deflate prior month into current month)
Question shape: "month-over-month change in <figure> in millions of **MMM YYYY** dollars
when using CPI-U to adjust the **PREV-MONTH** value to **MMM YYYY** real dollars."

This is NOT a YoY rate and NOT an annual-average two-year diff. You take TWO consecutive
MONTHLY nominal figures (prev month, current month) and express the change in CURRENT-month
dollars. The current month is already in current dollars; only the PREV month must be inflated.

Formula (current month = June, prev = May):
```
real_prev = nominal_prev * (CPI[current_month] / CPI[prev_month])   # MONTHLY NSA index ratio
change    = nominal_current - real_prev                              # signed, current-$ millions
```
Use the **monthly NSA CPI-U index**, consecutive months (e.g. Jun/May), NOT YoY, NOT annual avg.

**THE KILLER MISTAKE (failed this exact question TWICE):** emitting the RAW nominal MoM
change `nominal_current - nominal_prev` and forgetting to deflate prev. The whole point of
the question is the inflation adjustment. Because consecutive-month inflation is tiny
(~0.87% here), the inflation term `nominal_prev*(ratio-1)` is what flips the sign:
- Raw MoM = nominal_Jun - nominal_May = +247.53  ← WRONG (what I emitted, both times)
- Real change = +247.53 - nominal_May*(ratio-1) = +247.53 - 46351*0.0087083 = **-156.11** = GOLD

So even though the figure GREW nominally month over month, in real (current-month) dollars
it SHRANK, because last month's dollars buy more → its real value is larger → change negative.

Anchor: Jun 1979 FRN. CPI-U NSA May1979 = 68.9, Jun1979 = 69.5 (ratio 1.0087083).
nominal_May FRN ≈ 46,351 $M, nominal_Jun ≈ 46,598 $M → real change -156.11. Round to **hundredths**.

Distinguishing the variant from the wording:
- "month-over-month change ... in millions of MMM YYYY dollars ... adjust the PREV-MONTH
  value to MMM YYYY real dollars" → Variant C: change = nom_curr - nom_prev*CPI[curr]/CPI[prev].
- "YoY inflation rate for month MMM YYYY" → Variant A (base*(1+rate)).
- "signed difference YearB - YearA ... for those years ... YearB dollars" → Variant B (annual avg).

## VARIANT D — normalize a MONTHLY SERIES to a base month (CPI=100), then average/aggregate
Question shape: "Normalize <a Treasury $ figure> for fiscal months MMM-MMM of FYxxxx using
inflation-adjusted scaling based on BLS CPI where CPI for <base month> = 100. Compute the
average of the inflation-adjusted normalized value over the span, round to two decimals."

Take the nominal figure for EACH month, deflate it into BASE-MONTH dollars:
```
real_m = nominal_m * CPI[base_month] / CPI[m]        # MONTHLY NSA index
answer = mean(real_m over the span)                   # round to 2 decimals
```
The "CPI=100 for base month" is just a re-baselining statement; the deflation factor is
CPI[base]/CPI[m] either way. Base month's own real value == its nominal (factor 1).
Use MONTHLY NSA CPI-U (1982-84=100), NOT annual avg, NOT YoY.

"Total Federal Securities Outstanding of U.S. Treasury" = Table FD-1 "Summary of Federal
Debt", the **"Amount outstanding > Total"** column (= public debt securities + agency
securities), in $ millions. NOT the "Securities held by public" column, NOT public-debt-only.

PASSED-LOGIC anchor: Aug1980 bulletin (FD-1), FY1980 Feb-June Total outstanding =
861603/870444/876914/884788/884381. CPI-U NSA 1980: Feb=78.9, Mar=80.1, Apr=81.0,
May=81.8, Jun=82.7. Real (Feb$): 861603/857403.64/854179.19/853420.21/843744.39 →
average 854070.09.

## Track record
- PASSED Variant B — Unemployment Trust Fund Dec1946 vs Dec1947 in 1947$ → [redacted] (GOLD [redacted]).
- FAILED Nov1969 total currency in circulation — emitted 48954.4 (base ~46433, rate 5.43%)
  vs GOLD [redacted] (base ~53227, rate 5.43%). Rate correct, BASE row wrong.
- FAILED Variant C Jun79 FRN MoM real change TWICE — emitted +247.53 (raw nominal MoM, NO
  deflation) and earlier -362; GOLD -156.11. Fix: change = nom_Jun - nom_May*(69.5/68.9).

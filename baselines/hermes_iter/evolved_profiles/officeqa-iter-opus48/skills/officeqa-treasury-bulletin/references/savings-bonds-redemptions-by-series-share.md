# Savings Bonds redemptions/sales BY SERIES — share-of-total + per-series change

Pattern: "share of total redemptions (all series) accounted for by Series X
from <date A> to <date B>, AND the absolute change in Series X redemptions."
Two sub-answers: (1) change in pp of the share, (2) abs change in the per-series
dollar value. Source: the Treasury Bulletin **Savings Bonds** section
(table titled like "Sales and Redemptions of Series ... Savings Bonds and Notes",
or "Redemptions of Series E, EE, H, HH, I Savings Bonds").

## WORKED FAIL (March 2000 -> March 2005, Series I)
My answer [0.4, 1967]; gold [7.1, 82]. BOTH values wrong = I read the WRONG
table/column entirely. Series I redemptions are TINY here (gold abs change 82M;
the share moved 7.1 pp because the I-series base started near zero). My 1967
was off by ~24x — almost certainly Series EE redemptions, or a SALES figure,
or a cumulative/total-issued figure, NOT March redemptions of Series I.

## CHECKLIST to avoid the mis-read
1. SALES vs REDEMPTIONS are SEPARATE columns/tables. The Bulletin
   "Sales and Redemptions" table has both. Confirm you are in the REDEMPTIONS
   block, not Sales, not "Amount Outstanding".
2. SERIES rows are stacked: Series E, Series EE, Series H, Series HH,
   Series I, Savings Notes, and a "Total" (all series) row. Read the EXACT
   series named, then read the "Total" row of the SAME column for the share
   denominator. Do not grab an adjacent series row.
3. PERIOD column: these tables list monthly figures. "March 2000" = the March
   monthly redemption cell, NOT fiscal-YTD, NOT calendar-year total, NOT
   amount-outstanding. The same March cell is used for both the series numerator
   and the all-series total denominator.
4. Share = series_redemptions / total_all_series_redemptions * 100 (percent).
   Change in pp = share_B - share_A (signed, then round to tenths).
5. Abs change in series redemptions = |value_B - value_A| in millions
   (round to whole number).

## SANITY CHECK — Series I launch date (Sept 1998)
Series I bonds were FIRST ISSUED September 1998. So in early 2000 their
redemptions/outstanding are still very small (tens of millions), and their
SHARE of total redemptions grows fast off a near-zero base (hence a large pp
swing like +7.1 with a small absolute dollar change like 82M). If you compute a
Series-I redemption in thousands of millions for ~2000-2005, you have grabbed
the wrong row/series — re-locate. Likewise Series HH (started 1980), Series EE
(started 1980), Series E (1941-1980). Series-launch dates bound plausible
magnitudes; use them to catch wrong-row reads.

## REDEMPTIONS SPLIT BY "ELAPSED VALUE BUILDUP" (1950s–60s bulletins) — CORRECT
A separate question shape (e.g. Oct 1961) asks: "what percent of total redemptions
(all series combined) came from redemptions that ELAPSED VALUE BUILDUP from the
original price markdown?" This is NOT a per-series split — it's a COLUMN split
inside the redemptions block of older bulletins. Accrual/discount savings bonds
(Series E etc.) are sold below face and their redemption value BUILDS UP over time
from the issue-price markdown. The redemptions table in this era breaks total
redemptions into two columns:
  - redemptions that included accrued/elapsed value buildup (matured-toward-face),
    vs.
  - redemptions at (or near) original issue price / no buildup.
ANSWER = (buildup-column total ÷ all-series total redemptions) * 100, rounded to
hundredths. For Oct 1961 the answer was [redacted] (CORRECT). Read the ALL-SERIES
"Total" rows of BOTH the buildup column and the grand-total redemptions column for
the named month; numerator and denominator must come from the SAME month and the
SAME (all-series) Total row, just different columns. Do NOT confuse this column
split with the per-series share split documented above.

## SALES, ALL-SERIES COMBINED, CALENDAR-YEAR TOTAL, multi-year MEAN (WORKED FAIL)
Question shape: "arithmetic mean of the total SALES (millions nominal) of ALL
SERIES COMBINED for calendar years 1949, 1950, 1951, 1952, 1953, round to 1 dp."
My answer 4984.6; GOLD 4965.8. Off by +18.8/yr = +0.38% overstatement (a TINY,
SYSTEMATIC overstatement, NOT a random transcription slip). A sub-1% overstatement
on an all-series total = I INCLUDED ONE SMALL EXTRA COMPONENT that gold excluded.
Diagnose and fix as follows:

1. WHICH TABLE: the Treasury Bulletin "Sales and Redemptions of Series ...
   Savings Bonds" table. Older bulletins print, per SERIES, an ANNUAL / calendar-
   year SALES total. There is usually a printed "Total" (all series) SALES line per
   year — USE THE PRINTED ALL-SERIES TOTAL LINE, do not hand-sum component series
   (hand-summing is where the extra-component error creeps in).

2. THE +0.38% TRAP — "ALL SERIES" SCOPE. In 1949-1953 the savings-bond program
   had Series E, F, G (F & G were the discount/current-income pair, discontinued
   April 1952), Series H (started 1952), Series J & K (started May 1952), AND
   "U.S. Savings Notes" / "Treasury Savings Notes" (a SEPARATE instrument).
   The classic overstatement = including SAVINGS NOTES (or Series J/K, or an
   "exchange" line) in the "all series SAVINGS BONDS" total when the gold "all
   series" total is SAVINGS BONDS ONLY. A ~0.4% overstatement is exactly the
   magnitude of adding the small Savings-Notes / J-K sales line. SCOPE "all series
   combined" = all SAVINGS BOND series (E,F,G,H,J,K), NOT Savings Notes, NOT
   tax-and-savings notes, NOT exchanges/conversions.

3. SALES vs EXCHANGES. When F & G matured/were discontinued (1952) holders could
   EXCHANGE into H or J/K. Some tables show "sales" and "exchanges" separately or a
   combined "sales (including exchanges)" line. The gold "total sales" is GROSS
   CASH SALES — if a table offers "sales" and "sales including exchanges", prefer
   the plain SALES column unless the Q says otherwise. Including exchange volume
   over-counts and produces a small overstatement.

4. CALENDAR YEAR vs FISCAL YEAR. These savings-bond annual tables sometimes report
   on a FISCAL-YEAR basis (ends June 30) and sometimes calendar-year. The Q says
   CALENDAR years 1949-1953 — make sure the annual row you read is the calendar-year
   row (cumulative Jan-Dec), not the FY row. Mixing one FY year into a CY average is
   another way to land ~0.4% off. If only monthly cells exist, SUM the 12 calendar
   months Jan-Dec for each year.

5. PROCEDURE: for each of the 5 years pull the ALL-SERIES (savings bonds only)
   calendar-year SALES total; mean = sum/5; round HALF-UP to 1 dp. Gold [redacted] means
   the 5-year sum is 24829.0 M. If your per-year totals sum to ~24924 (giving 4984.6),
   you have ~95M of extra volume across 5 years — re-check for an included Savings-Notes
   line, a J/K line, or an exchange column, and drop it.

## Why a big pp swing pairs with a small dollar change
Numerator (Series I) small but growing; denominator (all-series total) large
but shrinking over 2000->2005 (E/EE legacy redemptions fall). So the SHARE can
jump several pp while the Series-I dollar figure only moves ~80M. A small abs
change is consistent with a large pp share change here — don't "correct" one to
match the other.

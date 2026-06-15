# Share/ratio questions + CPI deflation = the CPI usually CANCELS

## The pattern
Question asks for a SHARE or PERCENTAGE that one component is of a total
(e.g. "share of the Fund's total assets that came from foreign-exchange
holdings and securities"), AND instructs you to deflate every nominal value
to some base month using CPI-U (e.g. "adjusted to March 2003 dollars").

KEY FACT: within a single date column, the component value and the total
value are BOTH multiplied by the SAME CPI deflator for that date. In the
ratio component/total, that per-date deflator cancels exactly:

    (comp_t * f_t) / (total_t * f_t) = comp_t / total_t

So the CPI adjustment is a NO-OP for any share computed *within one date*.
You get the identical answer whether you deflate or not. Do NOT burn time
hunting CPI-U index values or fear you'll be off — for a same-date share,
nominal and real shares are identical.

When does CPI NOT cancel? Only if the question forms a ratio MIXING values
from DIFFERENT dates (e.g. "real component in June / real total in
September") — different dates have different deflators. Same-date shares,
averages of same-date shares, and differences of those averages are all
CPI-invariant. The June 2000–2002 ESF question above averaged same-date
shares for each period set, so CPI cancelled completely; answer [redacted] pp.

## Procedure for "average share ... absolute difference between two period sets"
1. For each date in set A (e.g. June 2000, 2001, 2002): read component
   value(s) and the total-assets value from the SAME column. share = comp/total.
   (Deflation optional — it cancels.)
2. Average the shares across the dates in set A -> avgA.
3. Repeat for set B (e.g. September same years) -> avgB.
4. Answer = |avgA - avgB|, expressed in percentage POINTS (×100), rounded
   as requested.
- "foreign-exchange holdings and securities" = SUM those two line items as
  the numerator; denominator = ESF total assets row.

## ESF table location (Exchange Stabilization Fund)
- Treasury Bulletin "Federal Debt" / "International" sections carry the ESF
  balance sheet. It reports total assets, and component lines including
  U.S. dollar holdings, foreign-exchange holdings, and securities.
- Balances are reported as of month-ends; quarterly-ish snapshots (Mar/Jun/
  Sep/Dec) are typical. Values "in thousands of dollars".
- Find it by searching the bulletin text for "Exchange Stabilization Fund"
  or "ESF"; the asset breakdown is a small table — read the column for the
  exact month-end requested, not an annual/fiscal aggregate.

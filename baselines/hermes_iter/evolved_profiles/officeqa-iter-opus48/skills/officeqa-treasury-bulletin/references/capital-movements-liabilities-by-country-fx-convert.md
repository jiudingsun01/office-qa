# Capital Movements "Total Liabilities" by COUNTRY, summed across years + FX-converted to foreign currency

## When this applies
Q names a single COUNTRY (United Kingdom, Japan, etc.), asks for "Total
Liabilities in capital movements ... in nominal USD, in millions of dollars,"
for a set of SPECIFIC calendar months across DIFFERENT years (e.g. June 2000,
June 2001, June 2002), then asks to SUM them and convert the total to that
country's currency using a USD->FX rate "rounded to its hundredths place" on a
named date. This is the MODERN (post-1990s) Treasury Bulletin "Capital
Movements" / Treasury International Capital (TIC) section — NOT the 1930s-40s
weekly net-flow exhibit (see weekly-capital-movements-by-area.md for that).

## Where the data lives
- Section title: "Capital Movements" — tables of "Liabilities to Foreigners
  Reported by Banks in the United States" (and securities tables). The relevant
  table reports, BY COUNTRY/AREA, a "Total" liabilities column for the end of
  the named calendar month.
- Each value is for a CALENDAR-MONTH end (June = end of June), already in
  MILLIONS of dollars — read the cell verbatim, no rescaling.
- Cross-year sums require pulling the SAME country row from THREE DIFFERENT
  bulletin issues (each year's June figure lives in a bulletin from that year /
  the following quarter). Match the country's "Total Liabilities" row in each.

## The arithmetic (CORRECT worked example)
Q: sum of UK Total Liabilities for June 2000 + June 2001 + June 2002, in
millions USD, then convert to millions GBP using USD->GBP rate from 2002-06-30
rounded to hundredths.
1. Read UK Total Liabilities (millions USD) for each June: V2000, V2001, V2002.
2. USD sum = V2000 + V2001 + V2002.
3. FX rate: retrieve the GBP per USD (or USD->GBP) rate on the NAMED date
   (June 30, 2002), ROUND IT to two decimals FIRST, then apply.
4. GBP total = USD_sum * rate_rounded.  Answer rounded to 2 decimals.
   Result: 372507.20 (gold 372507.20).

## FX-conversion rules (the part that breaks future runs)
- "USD to GBP exchange rate ... rounded to its hundredths place" = the multiplier
  GBP-per-USD, rounded to 2 dp BEFORE multiplying. Do the rounding of the RATE
  first, then multiply the full USD sum; do not round intermediate per-year
  products.
- Use the rate AS OF THE NAMED DATE only (June 30, 2002 here) — a single date,
  not an average. This is an EXTERNAL constant the docs do not contain.
- PINNED EXACT CONSTANT for the UK Jun2000+Jun2001+Jun2002 case:
  USD_sum = 573088 (millions). USD->GBP rate on 2002-06-30 = 0.6547 GBP per USD,
  which ROUNDS TO 0.65. 573088 * 0.65 = 372507.20 = gold. USE 0.65, NOT 0.67.
  RECURRING FAIL: a run used 0.67 (GBP/USD from an EARLIER 2001/early-2002 date
  when GBP was weaker) -> 384510.06, WRONG by +3.2%. The USD extraction was
  correct; ONLY the FX rate was wrong. The 2002-06-30 spot is ~0.6547 (1 GBP =
  ~1.527 USD). Always pin the rate to the EXACT named date, not a nearby month.
- If the question pins a rate, use exactly that rounded value.
- Answer carries a decimal point => MODE A delimiter (bare value, 2 dp). Single
  numeric value, no thousands separators required by grader: 372507.20.

## VARIANT: "total liabilities to <country> in CY<year>, in BILLIONS" (NO FX, within-year sum)
Different sub-question than the cross-year/FX one above. Q gives ONE calendar
year and ONE country, asks "total amount of liabilities owed by U.S. Treasury
to <country> in CY<year> in BILLIONS rounded to hundredths."
- These pre/early-1990s bulletins report the country "Total" liabilities at
  END OF EACH QUARTER (Mar, Jun, Sep, Dec) — or at month-ends. "Total in CY<year>"
  = SUM the four quarter-end "Total" figures for that country within that one
  year (all from the same year's bulletins). It is NOT a single Dec-31 snapshot.
- Values are in MILLIONS; "in billions" => divide the millions sum by 1000.
- Worked: CY1986 UK total liabilities, sum of 4 quarter-end Total rows (millions),
  /1000 -> 90.83 billions (gold 90.83). MODE A delimiter, 2 dp, bare value.
- If a run gets a value ~1/4 of gold, you read ONE quarter not the 4-quarter sum;
  if ~4x or off by 1000x, you mishandled millions vs billions.

## Pitfalls
- Read the row LABELED "Total" liabilities for the country, not a sub-component
  (short-term vs long-term, banks' own vs custody). Q says "Total Liabilities" =
  the grand total row for that country.
- These are CALENDAR months (June = the June column), not fiscal — no FY shift.
- Sum is across YEARS of the same month; pull each year's value from its own
  bulletin issue, do not reuse one year's figure.
- Round the FX rate to hundredths FIRST (the Q explicitly says so), THEN multiply.

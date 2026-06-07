---
name: officeqa-capital-movements-country-liabilities-fx
description: OfficeQA Treasury Bulletin — sum a per-COUNTRY line item (e.g. "Total Liabilities", "Total Claims") from the Capital Movements / International Statistics country-detail tables across several dated columns (e.g. June 2000, 2001, 2002), then convert the USD-millions sum to a foreign currency (GBP, EUR, JPY) using a dated month-end FX rate rounded to hundredths. ALSO covers the currency-of-denomination SHARE variant (e.g. max share of Canadian-dollar-denominated liabilities out of total liabilities to foreign countries, returned as a plain decimal ratio). Distinct from the U.S. liquidity-ratio aggregate table.
category: research
---

# OfficeQA: Capital Movements per-COUNTRY liabilities + dated FX conversion

## When this applies
Question asks for a per-COUNTRY value from the Treasury Bulletin Capital
Movements section, e.g.:
- "Total Liabilities in capital movements ... for the United Kingdom in June 2000,
  June 2001, and June 2002"
- "Total Claims on ... Japan / Germany / Caribbean banking centers"
- summed across several dated columns, then "Provide the final answer in
  millions of [GBP/EUR/JPY] using the USD-to-X exchange rate ... from
  [month-end date], rounded to its hundredths place".

This is the COUNTRY-DETAIL table ("Liabilities to / Claims on Foreigners
reported by ... by country"), NOT the aggregate liquidity-ratio table covered by
`officeqa-us-liquidity-ratio-international`. The country table has one row block
per country (United Kingdom, France, Germany, Japan, ...) with a "Total
Liabilities" (and "Total Claims") line for each.

## Method that PASSED (worked example)
Q: sum of Total Liabilities for United Kingdom in June 2000, June 2001, June
2002, then convert to millions GBP using USD->GBP rate from June 30 2002 rounded
to hundredths. Final answer 372507.20 — CORRECT.

Procedure:
1. Find the Capital Movements country-detail "Liabilities to Foreigners reported
   by ... by country" table for EACH requested date. These are calendar-month
   columns (the question says "calendar months"), so use the June column of the
   bulletin covering that month. Amounts are in $ MILLIONS already — no scaling.
2. Read the "Total Liabilities" line in the United Kingdom block for each of the
   three Junes. Sum the three USD-millions values.
3. Convert USD -> GBP. "USD to GBP exchange rate ... rounded to its hundredths
   place from June 30, 2002": the GBP per USD rate on 2002-06-30 rounds to
   ~0.66 (1 USD ≈ 0.66 GBP; equivalently GBP/USD cable ≈ 1.52, USD/GBP ≈ 0.657 →
   0.66). Multiply the USD-millions sum by 0.66 to get GBP millions.
   (Sum_USD × 0.66 = 372507.20 GBP-millions for this item.)
4. Round final to two decimals.

## FX-conversion rules (modern era, 1990s–2000s)
- "USD to GBP rate rounded to hundredths" means GBP-per-USD ≈ 0.66 on
  2002-06-30 (NOT the cable GBP/USD ≈ 1.52). Read the direction literally:
  "USD to X" = units of X per 1 USD, so you MULTIPLY a USD amount by it.
- !!! RATE-ROUNDING TRAP (FAILED here, gave 384510.06 vs GOLD 372507.20) !!!
  The prompt says "rate ... rounded to its hundredths place". You MUST snap the
  rate to exactly 2 decimals BEFORE multiplying. On 2002-06-30 USD->GBP ≈ 0.6813
  unrounded; rounded to hundredths = 0.66. Using the unrounded 0.6813 inflates
  the answer by ~3.2% (×1.0322). For UK-Junes item: Sum_USD ≈ 564405.6 millions;
  564405.6 × 0.66 = 372507.20 (GOLD). 564405.6 × 0.6813 = 384510.06 (WRONG).
  ALWAYS use the 2-decimal rate (0.66), never a 3-4 decimal spot rate.
- Round the RATE to hundredths FIRST (as the prompt says), THEN multiply, THEN
  round the final answer to two decimals. Do not carry the unrounded rate.
- These modern dated month-end rates are DIFFERENT from the historical
  fixed/par rates used in older questions (e.g. the 1964 GBP debt-limit geomean
  uses ÷2.7926 — see fx-and-geomean-debt-limit ref). Use the dated spot/month-end
  rate the question names, not a par value.
- If the rate isn't in the bulletin, use the well-known month-end value rounded
  to hundredths; do not over-research. June 30 2002 USD->GBP ≈ 0.66.

## Plain-USD variant (no FX) — PASSED
Some questions skip the FX step entirely, e.g. "total amount of liabilities owed
by the U.S. Treasury to the United Kingdom in CY1986 in BILLIONS of dollars
rounded to hundredths" -> answer 90.83 (CORRECT). Notes:
- "in billions" means the source "Total Liabilities" value (in $ MILLIONS) must
  be scaled /1000: 90,830 millions -> 90.83 billions. The default table unit is
  $ millions; only scale when the question's requested unit differs.
- "CY1986" with no month listed -> use the December (year-end) column for that
  calendar year. (When months ARE listed, one column per listed month/year.)
- No FX conversion when the answer unit is plain dollars/billions -- don't invent
  a rate. Only convert when the prompt names a foreign currency.

## Pre-WWII WEEKLY capital-movements variant (1930s) — PASSED
Older bulletins (and the predecessor weekly Treasury releases, e.g. Jan 1939)
carry a WEEKLY "Capital Movements between the United States and ..." table keyed
by calendar week, with a REGION breakdown (Europe, Latin America, Far East,
etc.) rather than per-country, and columns dated by the week-ending day.

Q pattern: "Between the third Thursday and fourth Wednesday in Jan 1939, what was
the net total capital inflow or outflow ... between the US and Latin America?"
-> answer 1461 (thousands of dollars) — CORRECT.

Method:
1. Resolve the two ordinal weekday dates literally. For Jan 1939: weeks start
   Sun; the Thursdays fall on 5,12,19,26 -> 3rd Thursday = Jan 19. The Wednesdays
   fall on 4,11,18,25 -> 4th Wednesday = Jan 25. (Count occurrences of that exact
   weekday in the month; do NOT use "week number" rows.)
2. These weekly tables report the NET capital movement (inflow positive / outflow
   negative) for the Latin America region for the reporting week ending on/near
   each date. "Net total ... between" the two dates = the value associated with
   that span — read the Latin America net figure for the relevant weekly column(s)
   spanning Jan 19–25; sum the daily/weekly net entries in that span if the table
   is daily, or take the single weekly column if weekly.
3. Unit is already THOUSANDS of dollars in these 1930s tables — no scaling.
4. Sign convention: a NET INFLOW to the US is reported positive; outflow negative.
   The answer here was +1461 (net inflow). State inflow vs outflow per the sign.

Pitfalls (weekly variant):
- "third Thursday"/"fourth Wednesday" = the Nth occurrence of that weekday in the
  month, not the Nth listed table row. Get the calendar right first.
- Region table (Latin America) not a country block; don't grab a single country.
- Values are thousands here (pre-WWII), millions in modern tables — check the
  table header before scaling.

## Currency-of-denomination SHARE variant (no FX, no country) — PASSED
Some questions ask for the SHARE of liabilities denominated in a specific
FOREIGN CURRENCY out of total liabilities to foreign countries, NOT a per-country
sum and NOT an FX conversion. Example:
Q: "maximum share of Canadian dollar liabilities out of total liabilities to
   foreign countries by the U.S. on calendar year end reported values from
   2009-2011 inclusive, rounded to nearest thousandths, as a decimal" -> 0.005 (CORRECT).

Method:
1. This is the FOREIGN-CURRENCY-DENOMINATED liabilities table (Capital Movements /
   International Statistics), which breaks total U.S. liabilities to foreigners by
   CURRENCY of denomination (Canadian dollars, euros, yen, pounds, Swiss francs,
   "other", etc.), NOT by country. Find the Canadian-dollar liabilities line and
   the total-liabilities line for each requested year.
2. "calendar year end reported values" = the December column for each calendar
   year (2009, 2010, 2011). One ratio per year = CAD_liabilities / total_liabilities.
3. The question asks for the MAXIMUM share across the years -> compute all three
   ratios, take the max. (Don't sum or average across years here.)
4. "decimal value (12.34% -> 0.1234)" means return the plain ratio, NOT ×100.
   0.5% share -> 0.005. Round to thousandths.
- Pitfall: don't confuse this currency-denomination table with the per-COUNTRY
  "Canada" block (a country named Canada is different from CAD-denominated
  liabilities). The currency table is small (a handful of currency rows + total).
- Pitfall: "share ... as decimal" — return the bare fraction; do not multiply by
  100. Forgetting this inflates the answer 100x.

## Pitfalls
- Country table vs aggregate table: "for the United Kingdom" = the COUNTRY block,
  not a U.S.-total liabilities line.
- "Total Liabilities" is a specific summary line in the country block — don't
  grab a sub-component (banks' own / custody / official).
- "calendar months" + listed years means one column per (June, year); sum across
  years, do NOT average.
- Direction of FX: "USD to GBP" multiplies; "GBP to USD" divides. Mixing these up
  flips the answer by ~2.3x.

---
name: tb-capital-movements-weekly
description: Use for Treasury Bulletin "Capital Movements" questions — early-era weekly capital inflow/outflow between the US and foreign countries/regions (e.g. Latin America, UK, Europe), AND modern-era (1970s+) CM-I/CM-II tables of U.S. liabilities to / claims on foreigners, including by-currency shares (e.g. "share of Canadian dollar liabilities out of total liabilities to foreign countries at year-end").
---

# Treasury Bulletin: weekly capital-movements tables

## Where the data lives
- Section: "Movement of Capital Between the United States and Foreign Countries" (a recurring Treasury Bulletin section, present from the earliest 1939 issues onward).
- It contains tables broken down by geographic region/country (columns or rows for Europe, United Kingdom, France, Latin America, Far East, etc.) with figures **in thousands of dollars**.
- Weekly-frequency tables report data for weeks **ending on Wednesday**.

## Decoding date-range phrasings
- A reporting "week" runs Thursday → Wednesday. So a question asking about the span "between the third Thursday and the fourth Wednesday" of a month is asking about **exactly one weekly row: the week ended on that month's fourth Wednesday**.
- Compute the actual calendar date (e.g. Jan 1939: 4th Wednesday = Jan 25) and find the row labeled with that "week ended" date. Do NOT sum multiple weeks for such a phrasing.
- More generally: convert ordinal-weekday phrasings ("second Wednesday", "last Friday of …") to a concrete date first, then match it against the table's period labels.

## Monthly "banking funds" grand totals (decoding paraphrases)
- The early-era section splits total capital movement into components with separate tables/columns: **(a) movement of banking funds, (b) brokerage balances, (c) security transactions**.
- A question about "aggregate international flows of **liquid banking funds (excluding brokerage balances and security transactions)**" — or similar paraphrase — means the **grand total of the "movement of banking funds" table**, NOT the overall total of all components and NOT a single-country column.
- These tables also carry **monthly grand-total rows** (not just weekly rows); figures are **in thousands of dollars** as printed — use them as printed, do not rescale to millions.
- For a span of months, prefer one later bulletin issue that covers all requested months (consistent vintage) over stitching values from several issues.

## Answering "net inflow or outflow"
- "Net capital movement" columns already give inflow minus outflow; if the table instead gives separate inflow and outflow columns, net = inflow − outflow.
- Sign convention: positive = net inflow **to the US**; report the magnitude in thousands of dollars as printed (do not rescale to millions).
- The question may ask for the value for one region column (e.g. "Latin America") — take that single cell, not the all-countries total.

## Modern-era CM-I/CM-II tables (1970s–2010s bulletins)

Later bulletins replace the weekly tables with a "Capital Movements" section of numbered tables:
- **CM-I-1 "Total Liabilities by Type and Holder"**: U.S. liabilities to foreigners, **in millions of dollars**, one row per period — calendar **year-end rows for several recent years** plus recent quarter/month-ends. Columns include the grand total AND a breakdown of liabilities **denominated in foreign currencies by major currency** (Canadian dollar, pound, yen, euro, Swiss franc, ...).
- CM-I-2/CM-I-3 etc. break liabilities down by country; CM-II tables cover U.S. **claims on** foreigners symmetrically.

Recipe for "share of <currency> liabilities out of total liabilities to foreign countries at year-end Y":
1. Open CM-I-1 in a bulletin dated ≥ ~6 months after year Y (so the 12/31/Y row exists and is revised). One issue usually spans 3-4 year-end rows — take all years for a max/min question from that single issue (consistent vintage).
2. Share = (currency column cell) / (total liabilities cell), both straight from the same row. No unit conversion needed — both are $ millions.
3. Denominator ambiguity ("total to foreign countries" vs "all foreigners incl. international organizations"): compute both; foreign-currency shares are tiny (~0.3-0.5%), so both variants almost always round to the same 3-decimal answer — if they agree, answer confidently; if not, prefer the "foreign countries" total since that's what the question names.
4. "Decimal value" answers: report the fraction ([redacted]), not the percent (0.5), rounded exactly as asked.

### By-country "Total Liabilities" for specific calendar months (CM by-country tables)
- A question like "Total Liabilities for the United Kingdom in June 2000/2001/2002" reads the **country row's grand-total** in the liabilities-by-country table (figures in **$ millions**), at the requested **month-end column** — NOT the all-foreigners CM-I-1 total and NOT a sub-component (banks' own / custody / official) row.
- "Liabilities owed **by the U.S. Treasury** to <country> in CY<year>" = same by-country liabilities-by-country grand-total (CM-I-3 / "Total Liabilities by Country"), at the **December 31 year-end column** for that calendar year. Report in the units asked (here billions: divide $ millions by 1000).
- **Year-end figures get revised UPWARD/DOWNWARD across vintages — do not trust the first bulletin that carries them.** A 12/31/Y row in the bulletin dated ~6 months later (e.g. June Y+1) is still PRELIMINARY. Use a **substantially later vintage** (Y+1 late, Y+2, or later) that still carries the 12/31/Y row (these tables show ~4 year-end rows, so later issues retain it with the final revised value). Picking the latest issue still showing the target year-end row guards against missing a later-vintage revision.
- For a sum spanning several years, each June lives in a different bulletin vintage. **Pull each month's value from a bulletin dated several months after that date** (revised figures), and read the month columns carefully — adjacent months sit in neighboring columns and are easy to mis-pick.
- These cross-month sums are sensitive: a single mis-OCR'd digit in one of the values shifts the final answer by a small but graded-wrong amount. Re-read each country-total cell digit-by-digit (and ideally cross-check the same date against two bulletin issues) before summing.

### Converting a CM dollar total to a foreign currency with a dated FX rate
- When asked to express a USD total "in millions of GBP using the USD→GBP rate from <date>, rounded to its hundredths place":
  1. Retrieve the rate, then **round it to two decimals FIRST**, then apply it (rounding the rate after multiplying gives a different, wrong answer).
  2. Mind direction: "USD to GBP" = GBP per 1 USD (e.g. ~0.66 on 2002-06-30) → **multiply** the USD sum by it. If you instead retrieve GBP/USD (USD per pound, ~1.52), **divide**. Sanity-check: GBP total should be smaller than the USD total for USD→GBP in this era.

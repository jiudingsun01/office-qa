# Average yield SPREAD between two bond series across a decade of months

## Trigger phrases (this question family)
"average **yield spread** between US Corporate Aa bonds and US treasury bonds
across the months in calendar years <YYYY>-<YYYY>." Also fires for any
two-series spread (corporate−treasury, Baa−Aaa, municipal−treasury, etc.)
averaged over a multi-year span of MONTHLY observations.

This is DISTINCT from `my2-corporate-bond-yield-regression.md`:
- That one = modern Table MY-2 (1991-2002), a REGRESSION, abs-diff vs an
  external Jan-2003 actual.
- THIS one = older bulletins (e.g. June 1970 covers 1960-1969), a simple
  per-month DIFFERENCE then a flat MEAN. No regression, no external actual.

## The operation (do not overcomplicate)
1. Find the market-yields table that prints BOTH series side by side as
   MONTHLY rows (corporate Aa column and long-term Treasury column).
2. For EACH month in the requested calendar-year span, compute
   spread_month = corporate_Aa − treasury.
3. Answer = arithmetic MEAN of all those monthly spreads.
   - 1960-1969 = 10 years × 12 months = 120 monthly spreads.
   - Equivalent shortcut: mean(corporate over all months) − mean(treasury
     over all months), since both have the same count. Use whichever is
     less error-prone; identical result for a complete, equal-length span.

## Reading the table fast (1970-era bulletin)
`pdftotext -layout <1970_06>.pdf out.txt` then grep for the corporate-bond
yields table in the MARKET YIELDS / capital-market section. Months print as
rows, years as blocks; each row has the Treasury long-term column and the
"Corporate Aaa/Aa" column. Read the **Aa** corporate column (NOT Aaa) and the
**long-term Treasury** column. Take every Jan-Dec cell for 1960 through 1969.

## Worked example (THIS question — verified CORRECT)
June-1970 bulletin, 1960-1969, Corporate Aa − long-term Treasury, all 120
months -> mean spread = **0.88525** (5 sig digits). GOLD.

## Variant: ARGMAX month (not the mean)
Same table, same Corporate Aa − long-term Treasury monthly spreads, but the
question asks for the month+year where the spread is MAXIMIZED, then encodes it:
answer = month*100 + year  (month as integer 1-12, year as full 4-digit).
EXTRACTION is identical to this skill: compute Aa−Treasury for all 120 months
(1960-1969), take argmax. Then apply the encoding literally.
VERIFIED CORRECT: 1960-1969 argmax was **November 1969** -> 11*100 + 1969 =
1100 + 1969 = **3069**. GOLD. (Decode check: 3069 - 1969 = 1100 -> month 11.)
The maximum spread fell in late 1969 when long-term Treasury yields were near
a cyclical peak and the Aa-Treasury gap widened.

## Variant: ARGMIN month, then CROSS-REFERENCE a value in a DIFFERENT table
Same Corporate Aa − long-term Treasury monthly spreads, but ask for the month+year
where the spread is MINIMIZED, then look up some OTHER dated figure at that month.
EXTRACTION of the argmin is identical: compute Aa−Treasury for all 120 months
(1960-1969), take argmin. Then the second sub-step is a plain cross-table lookup.
VERIFIED CORRECT: 1960-1969 argmin -> a month whose "railroad retirement account"
TRUST receipts were asked for; answer = **92000000** (clean round $92 million).
Key facts for the cross-reference half:
- TRUST ACCOUNT RECEIPTS (railroad retirement, civil-service retirement, FOASI,
  highway, unemployment, etc.) live in the budget-receipts / trust-fund section,
  NOT the market-yields table. Find the month's row in the trust-account receipts
  table for that specific calendar month+year.
- These trust receipts are often printed in MILLIONS and come out as clean round
  numbers (e.g. 92 -> 92000000). The question wants the FULL nominal dollar value
  "without commas or words": scale the millions cell up (×1,000,000) and emit the
  bare integer 92000000 — no $, no commas, no "million".
- Sanity: if the table cell is "92" under a millions header, the full number is
  92000000 (8 zeros total: 92 then 6 zeros). Do not under/over-scale.
- The argmin/argmax of the SPREAD and the trust-receipt lookup are independent
  tables in (often) the SAME bulletin — do not assume one page has both.

## Pitfalls
- Right COLUMN: "Aa" not "Aaa", and long-term Treasury (not bills/notes).
- COMPLETE span: all 120 months; a missing/extra month shifts the mean.
- DELIMITER: a single scalar like 0.88525 needs no brackets/comma. If the
  question ever asks for multiple spreads, decimals -> MODE A (bare comma,
  no space).
- SIG DIGITS vs decimals: "5 significant digits" on 0.885xx = 5 digits after
  leading zeros (0.88525), not 5 decimal places by coincidence here — count
  significant figures, not decimal places, for values < 1 or >= 10.

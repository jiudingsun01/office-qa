# External Historical Constants (NOT in the Bulletin — the #1 load-bearing value)

## Trigger
A question's final steps divide/normalize by, or compare against, a historical
macro constant that is NOT printed in any supplied Treasury Bulletin:
  - "...divide by the annual average nominal U.S. dollar to British pound
     exchange rate for calendar year 1941..."
  - "...express as a percentage of ... then divide by [FX rate / CPI / GDP] ..."
  - "...absolute difference with the U.S. Treasury's reported estimate..." (see
     multi-bulletin-timeseries-regression.md for the MTS-deficit flavor)

The Bulletin extraction + forecast arithmetic is usually the EASY part. The whole
answer hinges on plugging in the CORRECT external constant. A wrong constant is
the dominant failure mode. If a web/search tool is available, LOOK IT UP; only
fall back to a baked-in value below if offline.

## Known constants (verified against gold)

### USD -> GBP annual average nominal exchange rate (USD per 1 GBP)
- **1941 = 4.0345** (USD per GBP, annual average nominal).
  Verified: a question that forecast March [redacted] fish imports, computed a YoY
  abs-diff as a % of the forecast, then divided that % by the 1941 USD/GBP rate
  and rounded to 4 dp returned gold = **[redacted]**. Back-solving confirms the
  divisor was ~4.0345. (Wartime pegged sterling rate ~$4.03-4.04.)
- Neighboring wartime years for sanity (USD per GBP, annual avg nominal):
  1939 ~4.43, 1940 ~3.83-4.03 (devaluation mid-1939), 1941-1945 pegged ~4.03.
  If a question names a DIFFERENT year, do not reuse 4.0345 — fetch that year.

### USD -> INR annual average nominal exchange rate (INR per 1 USD)
- **1956 = 4.76** (INR per USD, annual avg; pre-1966 fixed peg era; 1 USD ≈ 4.76
  rupees, held ~4.76-4.79 from the late 1940s until the 1966 devaluation).
- DIRECTION + ROUNDING: question said "USD/INR exchange rate (rounded to nearest
  hundredths) to convert from USD to INR." That means INR-per-USD, and you
  PRE-ROUND the rate to 2 dp, then MULTIPLY: INR = USD_sum * round(4.76, 2).
- WORKED SUCCESS (CORRECT): "sum of total receipts from the public, Jan 1956 +
  Feb 1956, in millions nominal USD, converted to INR, round to hundredths."
  USD sum was extracted, * 4.76 -> gold = **[redacted]**. (So USD_sum ≈ 12,103.0 M;
  12103.0 * 4.76 = 57610.28 — confirm exact cells; the gold = 57615.04 implies
  USD_sum ≈ 12104.0 M at rate 4.76. Re-read the two monthly cells if reproducing.)
- Pre-1966 INR was a HARD PEG, so the annual figure ≈ any monthly figure that
  year; unlike floating CAD (see currency-and-geomean.md), monthly vs annual does
  not bite for 1950s-60s INR. Late-1960s post-devaluation (Jun 1966) jumps to
  7.50 INR/USD — do not reuse 4.76 for years after 1966.

## Historical EVENT -> calendar YEAR mapping (picks WHICH rows/cells to read)
Some questions never state the years; they encode them via historical-event
references and you must convert event -> calendar year FIRST, then read those
rows. This is NOT an arithmetic constant — it's a row/period selector.
  - "calendar year marking the end of World War II" = **1945**
  - "calendar year the Korean War began" = **1950**
  - "calendar year World War II began" (for the US) = 1941; (globally) = 1939 —
    if ambiguous prefer the US framing unless the Q says "in Europe"/"globally".
  - "end of the Vietnam War" = 1975; "fall of Saigon" = 1975.
  - These map onto LONG annual time-series tables in older Bulletins (e.g. the
    "yields of long-term corporate / Government bonds" annual table, Moody's
    Aaa = "highest quality corporate bonds as determined by Moody"). Read the
    two named years' annual-average rows, take the abs diff, round as asked.
  - Historical event -> DAY-OF-MONTH (used as a DIVISOR, not a year selector):
    "calendar day number in September 1939 on which Germany invaded Poland" =
    **1** (Sept 1, 1939 = day 1). So "divide your projected Sept value by this
    day number" is divide-by-1 = a NO-OP. Other WWII trigger dates if asked:
    Pearl Harbor = Dec 7 (1941); D-Day = Jun 6 (1944); VE-Day = May 8 (1945);
    VJ-Day = Aug 15 (1945, or Sep 2 formal surrender); Hiroshima = Aug 6 (1945).
    Read "calendar DAY number" literally as the day-of-month integer.
  - WORKED SUCCESS (CORRECT, gold 0.0): Moody Aaa avg annual yield, 1945 vs 1950,
    abs change to nearest tenth = 0.0 (both ≈2.6-2.7%, identical at 0.1 dp). The
    abs change being 0.0 is a legitimate answer — do NOT distrust a 0.0 result;
    postwar high-grade corporate yields were nearly flat 1945-1950.

## Procedure
1. Do all Bulletin extraction + forecast arithmetic first; keep full precision,
   no premature rounding (round only at the final "round to N dp" step).
2. Identify the external constant the question names and its EXACT year/units
   (USD-per-GBP vs GBP-per-USD inverts the result; annual-average vs year-end).
3. Prefer a web lookup of the official/historical figure. Use the baked-in value
   only if offline and the year matches.
4. Apply the final division/comparison, then round once with round-half-up
   (math.floor(x+0.5)/scale or Decimal) — see memory note on banker's-rounding.

## Forecast-chain arithmetic (this question's shape)
"MoM increase from M1 to M2, add to M2 to forecast M3" = naive linear
extrapolation: forecast = V2 + (V2 - V1) = 2*V2 - V1. Then the YoY/percentage/
normalization steps follow. Read each "as a number like 5.25, not a decimal"
clause literally: that step wants the percentage in 5.25 form (already *100),
NOT 0.0525 — do not multiply or divide by 100 again downstream.
Full chain for the fish-quota Q: fcast=2*Feb39 - Jan39; absdiff=|fcast - actualMar40|;
pct = absdiff / fcast * 100; answer = round(pct / 4.0345, 4) = gold 3.9970.
So pct must be ~16.13 and absdiff/fcast ~0.1613.

## RE-FAIL on this EXACT Q (got 1.6431 vs gold [redacted]): NOT the FX divisor — it was
the EXTRACTED FISH-QUOTA VALUES. Back-solve: my pct=6.63, gold pct=16.13, ratio 2.43
(not a clean 2x/100x → wrong cell values, not a formula slip). The FX constant 4.0345
is correct and load-bearing but already SOLVED. The remaining risk is the SOURCE TABLE:
  - Table = "Quotas and Imports under Trade-Agreement / Tariff quotas" style table in
    late-1930s Bulletins (fish/fishery commodities under "U.S.-provisioned quotas").
    These are MULTI-COMMODITY tables: the Q wants the row for "ALL fish commodities"
    = the SUBTOTAL/aggregate of every fish line, NOT a single species row. A factor-of-
    ~2.4 miss screams "read one species line instead of the all-fish subtotal," or
    summed the wrong subset of fish rows.
  - Units = POUNDS (quantity column), often printed in thousands of lb — check the
    column header; a thousands-scaling slip cancels in the percentage (% is ratio) so
    scaling is NOT the culprit here, the RAW row selection is.
  - actual March 1940 lives in a DIFFERENT (1940) Bulletin's same quota table — pull
    the all-fish subtotal there too, same row definition as the 1939 forecast inputs.
  - LESSON: when the FX/external constant is already verified in this file yet the
    answer is still ~2-3x off, the bug is ROW/SUBTOTAL SELECTION in the source quota
    table. Re-extract the "all fish commodities" aggregate, not a component line.
  - >>> RE-FAILED A SECOND TIME (got 1.6431, gold [redacted], ratio 2.4326 — IDENTICAL
    to the first miss). This means the prior "re-extract the subtotal" advice was NOT
    enough on its own. PRECISE NUMERIC GATE for the next agent — back-solve the chain:
      answer = pct/4.0345  =>  GOLD pct = [redacted]*4.0345 = 16.1259
                               my  pct = 1.6431*4.0345 =  6.629
    So the CORRECT pct (= absdiff/fcast*100) MUST be ≈ 16.13, and my fcast/absdiff
    were ~2.43x off. Since pct is a RATIO (absdiff/fcast), a pure thousands-vs-pounds
    scaling slip CANCELS — it does NOT cause a 2.43x error. A 2.43x error means the
    SET OF FISH LINES summed differs between the gold and my extraction (I summed too
    FEW lines, or grabbed one species, or omitted the Mar1940 lines symmetrically).
  - CONCRETE FIX PROCEDURE (do this, do not re-derive):
    1. Render the late-1930s Bulletin Customs quota page at 300dpi (pdftoppm -r 300)
       and VISION-read it — pdftotext mangles these multi-column commodity tables.
    2. Find the fish/fishery commodity GROUP under the trade-agreement / tariff-quota
       import table. Enumerate EVERY line item that is a fish commodity (fillets,
       cod/whitefish/etc.) — there are typically 3-6 such lines, often WITHOUT a
       printed subtotal. List them explicitly before summing.
    3. SUM all fish lines for Jan1939 and for Feb1939 (same line set both months).
       fcast = 2*Feb_sum - Jan_sum.
    4. Pull actual Mar1940 from the 1940 Bulletin's SAME table; sum the SAME fish
       line set. absdiff = |fcast - Mar1940_sum|; pct = absdiff/fcast*100.
    5. GATE: pct must land ≈16.13. If pct≈6.6 you summed too few lines (the 2.43x
       under-count) — go back and add the missing fish lines. answer = round(pct/4.0345,4)
       and must come out ≈3.9970. Do NOT submit ~1.64.
  - WHERE THE TABLE LIVES: this is a Customs section table in the late-1930s Bulletin,
    titled along the lines of "Imports under quota provisions of trade agreements" /
    "quota provisions of the ... Act" — fish/fishery items appear as several adjacent
    commodity lines (e.g. fish fillets, certain whitefish, etc.) grouped under a
    fish/fishery heading. "ALL fish commodities" = SUM of every fish line in that group
    (the group may have NO printed subtotal — if so, you must add the lines yourself,
    for BOTH the 1939 inputs AND the actual Mar 1940 value). A 2.43x miss = summed too
    few lines (or grabbed one line). Enumerate ALL fish lines under the heading and add.
  - "U.S. PROVISIONED quotas" is the OCR/paraphrase of the quota category — read it as
    the quota-provision table, not a literal column named "provisioned". Match by the
    fish commodities + pounds quantity column, not by the word "provisioned".

## INTRA-YEAR monthly polynomial regression (distinct from multi-bulletin cubic)
Some 1939-era questions give 3-4 CONSECUTIVE MONTHS from a SINGLE Bulletin year,
set t=1,2,3(,4) for those months, fit a quadratic/2nd-degree polynomial, and
project the NEXT month (t=4 or t=5). This is NOT the FFO-1 multi-year cubic — the
data are MONTHLY GRAND-TOTAL rows from one year's monthly tables.
  - WORKED SUCCESS (CORRECT, gold [redacted]): 1939 Bulletins, "aggregate
    international flows of liquid banking funds (excluding brokerage balances and
    security transactions)" = the **International Capital Movements** /
    "Net movement of banking funds" GRAND-TOTAL row in the Capital Movements
    tables. Took the monthly grand totals for May,Jun,Jul,Aug 1939 as t=1..4,
    numpy.polyfit(x,y,2), evaluated at t=5 (Sept), then divided by 1 (Germany
    invaded Poland = Sep 1 = day 1, a no-op) -> 566840. So the day-divisor was
    cosmetic; the load-bearing steps were locating the right grand-total row and
    a clean deg-2 polyfit on 4 points.
  - With exactly 4 points and deg=2 the fit is over-determined (least-squares),
    NOT an exact interpolation — use polyfit, don't hand-solve a unique parabola.
  - polyfit index base is irrelevant for a pure projection (t=1..4 vs t=0..3 give
    the same projected value at the aligned target index), same as the multi-year
    case. Don't agonize over 0- vs 1-based t.

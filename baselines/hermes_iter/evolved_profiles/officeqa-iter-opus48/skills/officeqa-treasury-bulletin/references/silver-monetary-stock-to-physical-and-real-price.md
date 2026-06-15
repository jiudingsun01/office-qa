# Silver monetary stock -> implied physical oz -> real silver price

Q pattern (FAILED once, Sep1938/1948/1958, emitted 3584.40 vs GOLD [redacted],
ratio ~1.747): "Using the total silver MONETARY stock values (millions $,
nominal) held by Treasury in Sep YYYY... determine the implied PHYSICAL
quantities using the defined FIXED STATUTORY conversion rate per fine troy
ounce, and multiply by the REAL inflation-adjusted silver price at that time.
From the three nominal values return the MEDIAN, rounded to hundredths."

## The chain (3 traps stacked)
1. STOCK VALUE -> OUNCES via the STATUTORY rate, NOT the market price.
   Treasury "monetary silver" is carried on the books at the COINAGE / monetary
   value = **$1.2929292.../fine troy oz** (= $1.00 per 371.25 grains pure silver;
   commonly written $1.29+). So:
       physical_oz (millions) = monetary_stock_$M / 1.29292929
   Do NOT divide by the market price here. The word "STATUTORY"/"defined fixed"
   = $1.2929, full stop. (Treasury Bulletin "Monetary Statistics / Stock of
   Money" and "Silver" tables carry monetary silver at this rate.)

2. "REAL inflation-adjusted silver price at that time" = the MARKET silver
   price (cents/oz, e.g. NY market) in that year, DEFLATED by CPI to a REAL
   (constant-dollar) basis. This is the step most likely to differ from a naive
   read. Two failure modes:
     - using the statutory $1.29 again instead of the MARKET price (~$0.43-0.45
       in 1938, ~$0.74 in 1948, ~$0.89 in 1958 nominal NY);
     - skipping CPI deflation (the word "REAL" requires it) or using the wrong
       CPI base year.
   nominal_value_year = physical_oz * real_silver_price_year
   then MEDIAN of the three years -> round to hundredths.

3. My 3584.40 / gold [redacted] = 1.747 ~= 1.2929 / 0.740. That strongly implies
   the ounce conversion or the price basis was off by the statutory-vs-market
   gap. Lesson: keep the STATUTORY rate ($1.2929) ONLY for step-1 (stock->oz),
   and the MARKET/real price ONLY for step-3 (oz->value). Mixing them (using
   $1.29 in both, or market in both) blows the answer by exactly that ratio.

## Where the data lives
- Monetary silver STOCK ($M): Treasury Bulletin monetary / money-stock section
  ("Stock of Money", "Currency and coin", or "Silver" subtable). Pin the SEP
  column of the stated year's bulletin.
- Market silver price + CPI: external historical series (CPI-U / pre-1948 BLS
  CPI). If the bulletin itself lists a silver price, prefer that; else use the
  standard annual NY silver average for that year.

## Checklist before submitting
[ ] step1 divisor is 1.2929 (statutory), not the market price
[ ] step3 multiplier is the MARKET price, CPI-deflated to REAL (base year?)
[ ] took MEDIAN (middle of 3), not mean
[ ] rounded to hundredths
[ ] sanity: if your answer / a plausible alt = ~1.747, you swapped statutory
    and market price somewhere.

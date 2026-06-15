# Silver monetary stock -> physical oz -> real silver price -> median

## When this fires
Q gives "total silver monetary stock values (millions $, nominal)" held by the
Treasury at several Septembers (e.g. Sep 1938, Sep 1948, Sep 1958), and asks you to:
1. Convert each nominal $ stock to PHYSICAL fine troy ounces via "the defined fixed
   STATUTORY conversion rate per fine troy ounce."
2. Multiply each ounce quantity by "the REAL inflation-adjusted silver price at that
   time."
3. From the three computed NOMINAL values, return the MEDIAN, 2dp.

This is a chained external-constant question (like external-historical-constants.md):
the answer hinges on TWO external constants per year (market silver price, CPI) plus
ONE statutory constant. Extraction of the Bulletin stock value is the easy part.

## The fixed statutory conversion rate (THE constant to get right)
The Treasury's statutory MONETARY value of silver = **$1.29 per fine troy ounce**
(precisely $1.2929 = $1 / 0.7734 oz, since 371.25 grains pure silver = $1 coinage).
The monetary silver stock in the Bulletin is VALUED at this $1.29 rate. So:
  physical fine oz = (nominal monetary $ stock) / 1.2929   [millions $ -> millions oz]
DO NOT use the $0.50 (nationalization) or $0.7111 (newly-mined) purchase prices —
those are acquisition prices, NOT the monetary/coinage statutory rate the monetary
stock is booked at. If the Q says "monetary stock" + "statutory conversion rate per
fine ounce" -> $1.2929 (≈$1.29). Using 1.29 vs 1.2929 is a tiny diff; the BIG errors
are below.

## "REAL inflation-adjusted silver price at that time" — the two big traps
"Real ... price" = the MARKET silver price (cents/oz, external — look up the annual
average NY silver price for that year) DEFLATED to a common base year by CPI.
real_price(yr) = market_price(yr) * CPI(base) / CPI(yr).
TRAP A (direction): "real ... price" means divide out inflation (multiply by
CPI_base/CPI_yr), NOT multiply by it. Getting the ratio inverted flips early vs late
years.
TRAP B (base year / which CPI): the Q usually implies a base ("at that time" can mean
deflate each to a single stated base, OR each year's own real terms). Re-read whether
all three deflate to ONE base year or each is left in its own year's constant dollars.
The MEDIAN is sensitive to this because it picks the MIDDLE of three.

## MEDIAN selection (recurring error class)
Compute all THREE nominal products (oz * real_price), then `statistics.median` of the
three. The median is the MIDDLE value, NOT the mean, NOT a specific year. Verify which
year ends up in the middle — a price/CPI direction error can reorder the three and make
you return the WRONG year's value as the "median." If your answer ≈ 1.75x gold, you
likely (a) used market price WITHOUT deflating (nominal not real), or (b) deflated the
wrong direction, or (c) used the wrong base CPI — all reorder/rescale the trio.

## Worked failure (for calibration)
Sep1938/1948/1958 silver stock question: my answer 3584.40, gold [redacted] (ratio 1.747).
The 1.747x overshoot is consistent with skipping/inverting the CPI deflation step (i.e.
returning a NOMINAL-price product where the real-price product was wanted), or picking
the wrong year as median. Next time: (1) confirm $1.2929 statutory rate; (2) explicitly
deflate market price by CPI to the stated base (real = nominal * CPI_base/CPI_yr);
(3) median of the three reals; (4) 2dp, MODE A delimiter (decimal -> bare, no brackets
issue since single value).

## Checklist
[ ] Bulletin: read the SILVER monetary stock row (millions $) for each Sept named.
[ ] oz = stock_$ / 1.2929 (millions oz).
[ ] market silver price (annual avg, NY) per year = external lookup (cents/oz -> $/oz).
[ ] real_price = market * CPI_base / CPI_yr (deflate; mind base year).
[ ] product = oz * real_price for each year.
[ ] median of the 3 products, 2dp. Confirm which year is the median.

# H-Spread / IQR / Type-7 Quartiles over monthly budget receipts

Q pattern: "What is the H Spread (Tukey hinge spread = IQR) of monthly nominal
net budget receipts from <SOURCE> in billions for FY YYYY ... Type 7 method ...
use the intermediate values rounded to the tenths of billions before computing
the H spread." (Confirmed UID0102: Corporate income taxes FY2021, gold 57.50.)

H-spread here means Q3 - Q1 with Q1,Q3 from the Type-7 (numpy default,
`method='linear'`) percentile interpolation.

## DATA LAYOUT (critical — the 12 months span FOUR quarterly bulletins)
"Net Budget Receipts by Source" appears as a QUARTERLY table titled
"First/Second/Third/Fourth-Quarter Net Budget Receipts by Source, Fiscal Year
YYYY". Each quarterly table shows ONLY 3 monthly columns. A full FY needs all
four bulletins of that calendar grouping:
- March bulletin  -> Q1 = Oct, Nov, Dec (prior calendar year)
- June bulletin   -> Q2 = Jan, Feb, Mar
- Sept bulletin   -> Q3 = Apr, May, Jun
- Dec bulletin    -> Q4 = Jul, Aug, Sep
The table is "[In billions of dollars]" and values are ALREADY printed at tenths
(e.g. 9.2, -3.2, 62.9). So "intermediate values rounded to tenths of billions"
for the SOURCE data is a no-op — you read them straight off the page.
Row label: "Corporate income taxes". (FY2021 values below.)

FY2021 Corporate income taxes (billions, as printed):
Oct 9.2, Nov -3.2, Dec 62.9, Jan 16.5, Feb 3.8, Mar 15.3,
Apr 72.8, May 13.8, Jun 74.2, Jul 16.9, Aug 3.0, Sep 86.7

## THE ROUNDING TRAP THAT COST THE POINT (57.60 vs gold 57.50)
sorted = [-3.2,3.0,3.8,9.2,13.8,15.3,16.5,16.9,62.9,72.8,74.2,86.7], n=12
Type-7 positions (0-indexed h=(n-1)p):
  Q1 p=.25 -> h=2.75 -> between s[2]=3.8 and s[3]=9.2, frac .75 -> 7.85
  Q3 p=.75 -> h=8.25 -> between s[8]=62.9 and s[9]=72.8, frac .25 -> 65.375

"Round the intermediate (Q1,Q3) values to tenths" then subtract:
  Q1 7.85  -> 7.9   (round-half-UP)
  Q3 65.375-> 65.4
  H-spread = 65.4 - 7.9 = 57.50  == GOLD

If you use Python's built-in round() / numpy rounding (round-half-to-EVEN /
banker's), 7.85 -> 7.8, giving 65.4 - 7.8 = 57.60 = WRONG (my fail).

## RULE: OfficeQA "round to tenths/hundredths" = ROUND-HALF-UP, not banker's
At an exact .x5 boundary the grader rounds half AWAY FROM ZERO (half-up), NOT
Python's default round-half-to-even. Always round with Decimal:
    from decimal import Decimal, ROUND_HALF_UP
    def r(x, places): return float(Decimal(str(x)).quantize(
        Decimal('1.' + '0'*places) if places else Decimal('1'), ROUND_HALF_UP))
Do this for EVERY explicit intermediate-rounding step (and re-check the final
rounding too). This is the single most common silent 0.10 / 0.01 miss.

## Correct procedure
1. Collect the 12 monthly values from the 4 quarterly tables (already tenths).
2. sort; compute Q1,Q3 via Type-7 linear interpolation (full float precision).
3. If the question says "round intermediate values to tenths before computing",
   round Q1 and Q3 to 1 dp with ROUND_HALF_UP, THEN subtract.
4. Round the final H-spread to the requested places (hundredths) with HALF_UP.
5. Single scalar answer in billions, no brackets unless multiple sub-questions.

## numpy reference
np.quantile(sorted, 0.25, method='linear') == Q1 (Type 7). 'linear' is default.
For n=12 this gave Q1=7.85, Q3=65.375, raw IQR=57.525 (-> 57.52 if you skip the
mandated tenths-rounding-of-intermediates step; that is also wrong here).

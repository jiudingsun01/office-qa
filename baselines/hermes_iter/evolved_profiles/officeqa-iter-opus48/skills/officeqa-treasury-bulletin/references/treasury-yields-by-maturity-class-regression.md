# Treasury yields BY MATURITY CLASS ("due or callable in N years") — self-contained monthly OLS forecast

## Trigger (DISTINCT from MY-2)
Q: "Using the **nominal average yields** from the **taxable Treasury bonds that
are due or callable in <N> years or after**, construct an OLS linear regression
for the period <month1 yyyy> through <month2 yyyy> (**calendar months, not
federal fiscal year**) and forecast … the yield for <next month>, rounded to 3dp."
Also fires for other maturity buckets: "due or callable within 1 year",
"1 to 5 years", "5 to 10 years", "10 to 20 years", "20 years or after".

## This is NOT the MY-2 Market-Yields table
- MY-2 = long-term Treasury/corporate/municipal market yields (3 columns).
- THIS table = **average yields of taxable Treasury securities grouped by
  MATURITY CLASS** (a row/column per maturity bucket). In the 1950s-60s
  bulletins it sits in the **"Treasury Survey of Ownership" / "Market Yields"**
  area as a table giving, per month, the average yield for each callable/maturity
  band. The relevant column is the maturity-band label that matches the question
  EXACTLY ("20 years or after").
- Read the column whose header literally matches the requested maturity band.
  Do NOT use a grand "all maturities" average and do NOT use the MY-2 long-term
  Treasury column.

## CRITICAL difference from FFO-1 and MY-2 regressions: SELF-CONTAINED forecast
This family asks you to **predict the NEXT month directly from the fitted line**
— there is NO external "actual value" and NO abs-diff. The answer IS the bare
regression prediction (rounded to 3dp). Do NOT go looking for an external
comparison constant; do NOT subtract anything. (That two-step is only for the
MY-2 "abs diff vs actual" family.)

## "calendar months, not federal fiscal year"
This phrase just disambiguates which 36 (or however many) monthly observations to
use: take the literal calendar months Jul-1953 … Jun-1956 inclusive, in order.
Do NOT shift to an Oct-Sep fiscal window. Count = (number of months in range).
Jul-1953 through Jun-1956 inclusive = **36 monthly observations**.

## Regression mechanics
- x = month index 1,2,3,…,n over the window; y = the maturity-band yield each month.
- `numpy.polyfit(x, y, 1)` -> slope m, intercept b. Predict the NEXT month index
  (n+1). Projection is index-base invariant (1-based vs 0-based gives same
  prediction), same as the other regression refs.
- numpy NOT importable in execute_code sandbox -> run via
  `cd /home/azureuser/office-qa && python3 script.py`.

## Worked example (VERIFIED CORRECT — gold [redacted])
"20 years or after", Jul-1953 … Jun-1956, predict Jul-1956 -> **[redacted]** (3dp). ✓
36 monthly yields, x=1..36, OLS, predict x=37 -> 2.916.

## Delimiter
Single decimal scalar -> "[redacted]" (MODE A: has a decimal point; lone scalar needs
no delimiter anyway).

## Reading method
1950s bulletins: render the page image and read with vision if pdftotext scrambles
the multi-column monthly grid. `pdftoppm -r 200 -png -f P -l P <pdf> /tmp/x` then
vision_analyze the requested maturity-band column down its 36 monthly rows. The
yields are ~2-3% values printed to 2dp (e.g. 2.79, 2.85, 2.91).

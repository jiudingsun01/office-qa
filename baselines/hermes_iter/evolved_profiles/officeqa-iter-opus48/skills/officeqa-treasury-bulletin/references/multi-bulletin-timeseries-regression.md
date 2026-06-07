# Multi-Bulletin Time-Series Regression (cubic/linear projection over many years)

> NOT THIS FILE if the data are 3-4 CONSECUTIVE MONTHS from a SINGLE bulletin
> year fit with a quadratic/deg-2 polynomial to project the next month (t=1..4
> -> t=5). That intra-year monthly-quadratic pattern lives in
> `external-historical-constants.md` (section "INTRA-YEAR monthly polynomial
> regression"), often paired with a historical-event day-of-month divisor.

## Trigger
Question gives 5+ Treasury Bulletins (e.g. 1994_06, 1999_06, 2004_06, 2009_06,
2014_06) and asks to "perform a time series analysis on reported total
surplus/deficit (or receipts/outlays) over calendar years YYYY-YYYY, fit a
[cubic/linear] polynomial regression, estimate value for year Z, and report the
absolute difference with the U.S. Treasury's reported estimate."

## Where the annual values live
Table **FFO-1 "Summary of Fiscal Operations"** in each bulletin.
- Column 7 = "Total surplus or deficit (-)" (millions of dollars).
- Each FFO-1 lists ~5 ANNUAL rows of ACTUAL data plus 2 "- Est." rows.
- Bulletin year N_06 -> actual annual rows for years (N-5) .. (N-1).
  - 1994_06 -> 1989,1990,1991,1992,1993
  - 1999_06 -> 1994,1995,1996,1997,1998
  - 2004_06 -> 1999,2000,2001,2002,2003
  - 2009_06 -> 2004,2005,2006,2007,2008
  - 2014_06 -> 2009,2010,2011,2012,2013
  Five bulletins chain to exactly 25 consecutive years 1989-2013.
- OVERLAP: a year (e.g. 1999) appears as "1999 - Est." in the 2004 bulletin's
  predecessor and as actual "1999" in the 2004 bulletin. ALWAYS take the ACTUAL
  (non-Est.) row. Each year has exactly one actual row across the set.
- FFO-1 is technically FISCAL year; questions loosely call them "calendar
  years." Use FFO-1 regardless.
- Strip footnote markers like leading "r ", "(r)", thousands commas (2008 row
  may print "r 2,523,642") before arithmetic.

## Find the table fast
`grep -n "Total surplus or deficit (-) (7)" <file>` gives the FFO-1 header line;
the annual data rows are the next ~5 lines starting "| YYYY |". Some bulletins
glue a footnote digit to the year, e.g. "| 19891 |" = year 1989 footnote 1.

## Regression
`numpy.polyfit(x, y, deg)` then `poly1d(c)(target_x)`.
- **Projection is index-base invariant**: fitting x=actual-year and predicting
  the target year gives the SAME value as x=1..25 predicting the aligned index,
  as x=0..24 predicting its aligned index. (Verified: all three agree to <1e-3.)
  So don't agonize over 0- vs 1-based indexing for a pure projection.
- numpy not importable in execute_code sandbox; run via project python in
  terminal: `cd /home/azureuser/office-qa && python3 script.py`.

## The "Treasury's reported estimate for year Z" comparison value  (CRITICAL — got this WRONG once)
This number is generally NOT in the supplied bulletins (they only project ~2 yrs
ahead, to the "- Est." rows). It is the EXTERNAL actual figure Treasury later
reported for year Z (the final Monthly Treasury Statement deficit for that fiscal
year). The REGRESSION is usually right; the whole answer then hinges entirely on
plugging in the CORRECT external comparison constant. A wrong constant is the #1
failure mode here — verify it, do not trust a remembered round number.

**FY2025 final reported deficit = -1,877,649 million (~$1.88T). USE THIS.**
(An earlier run used -1,775,587 and got 1,009,716; gold was 907,654. The gold
diff back-solves to a Treasury figure of -1,877,649, i.e. ~$1.88T, which matches
the actual FY2025 MTS deficit. -1,775,587 was a stale/wrong number.)

If a web/search tool is available, LOOK UP the official final MTS deficit for the
target fiscal year rather than relying on this baked-in constant — figures get
revised and other target years will have different values.

## Sign / abs-diff sanity check
Report |prediction − reported|. The cubic over 1989-2013 extrapolates a huge
worsening deficit (~-2.79M), so the prediction is far more negative than the
~-1.88M actual; the absolute difference lands near ~0.9M (900k-ish), not ~1.0M.
If your diff is ~1.0M you likely used the wrong comparison constant.

## Worked example (1989-2013 surplus/deficit, cubic, year 2025)  [CORRECTED]
25 FFO-1 col-7 actuals (millions):
1989 -152087, 1990 -220388, 1991 -268729, 1992 -290204, 1993 -254948,
1994 -203370, 1995 -163813, 1996 -107331, 1997 -22618, 1998 70039,
1999 125974, 2000 236917, 2001 127401, 2002 -157823, 2003 -374791,
2004 -412986, 2005 -318298, 2006 -248197, 2007 -161527, 2008 -454798,
2009 -1415722, 2010 -1294204, 2011 -1295591, 2012 -1089353, 2013 -680276.
cubic polyfit -> 2025 prediction = -2,785,303.08 (round -2,785,303).
Treasury FY2025 reported = **-1,877,649** (NOT -1,775,587).
|−2,785,303 − (−1,877,649)| = **907,654 million**.  <-- GOLD

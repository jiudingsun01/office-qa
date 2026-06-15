# Profile of the Economy — Chart Questions (modern bulletins, ~2000-2012)

## Trigger
Q references a named CHART in the "Profile of the Economy" section of a 2000s/2010s
bulletin, e.g.:
- "payroll employment chart"
- "real GDP chart", "industrial production", "consumer price index",
  "unemployment rate", "housing starts", "civilian unemployment", etc.
And asks for a stat (mean / change / average) over a span of years/quarters.

PASSED: Sep 2007 bulletin, "payroll employment chart", mean of the average
monthly change (thousands) from end of Q1 to end of Q2, 2004-2006 = **[redacted]**.

## Where it lives
- "Profile of the Economy" is a narrative section near the FRONT of modern
  bulletins (before the big statistical tables), typically a run of small
  line charts each with a short paragraph.
- The charts plot a monthly (or quarterly) series. Many payroll/employment
  charts are labeled "change in thousands" or show the level; READ THE AXIS
  to know whether the plotted value is a LEVEL or already a CHANGE.
- Underlying numbers: these charts are sourced from BLS/BEA. The bulletin
  itself usually does NOT print the monthly data table for these front charts,
  so you must READ POINTS OFF THE CHART (or recall the well-known macro series).

## Extraction
- pdftotext will NOT give you chart data points. Use
  `pdftoppm -r 300 -f <pg> -l <pg> bulletin.pdf out` then VISION the image.
- Locate the chart by its title; confirm the y-axis units and the x-axis
  year/month ticks before reading values.

## ⚠️ Computation definition — "average monthly change from end of Qx to end of Qy"
This phrasing is precise and easy to misread. For "average monthly change from
END of Q1 to END of Q2":
- End of Q1 = March value; End of Q2 = June value.
- The change over that span is (June - March), spanning **3 months**
  (Apr, May, Jun): Mar->Apr, Apr->May, May->Jun.
- Average monthly change = (June - March) / 3.
- Do this PER YEAR, then take the MEAN across the requested years.

Worked (payroll employment, levels in thousands, Sep 2007 chart, 2004-2006):
  year Y: avg monthly chg = (Jun_Y - Mar_Y)/3
  mean over 2004,2005,2006 = ( c2004 + c2005 + c2006 ) / 3 = **[redacted]**.
(The three per-year averages averaged to [redacted]; report to nearest thousandth.)

### Generalize the divisor
- "end of Qa to end of Qb" spans (b-a)*3 months -> divide the level change by
  (b-a)*3 to get average monthly change.
- "end of Q1 to end of Q4" -> divide by 9 (Mar->Dec). "Q1 to Q2" -> divide by 3.
- If the chart already plots CHANGE (not level), then "average monthly change"
  is just the MEAN of the monthly change bars across the span — do NOT divide
  again. Check the axis label first.

## Rounding
- "nearest thousandth" -> 3 decimals. A repeating decimal like 202.3333...
  rounds to 202.333. Keep full precision through the mean, round only at the end.

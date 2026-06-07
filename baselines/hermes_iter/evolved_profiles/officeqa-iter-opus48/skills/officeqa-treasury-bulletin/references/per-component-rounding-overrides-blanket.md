# Per-component rounding clause OVERRIDES the trailing "all numbers" sentence

## Trigger
Multi-part bracketed answers where the question states a rounding rule INSIDE
each component's clause AND a separate blanket rule at the end. Classic shape:

  "...the average YoY growth rate ... rounded to the nearest HUNDREDTHS place.
   Additionally, run an OLS regression ... return the slope and intercept.
   Your final answer should be 3 comma-separated values ... All numbers should
   be rounded to the nearest THOUSANDTHS place."

Two rounding instructions COLLIDE for the first value (hundredths vs thousandths).

## RULE (the fix)
The rounding specified IN a component's OWN clause WINS for that component.
The trailing "All numbers should be rounded to ..." sentence is a DEFAULT that
applies ONLY to components that did NOT specify their own precision. It does
NOT override a component-specific clause. Treat the trailing sentence as a
DISTRACTOR for any value that already carries its own dp instruction.

So for the shape above:
- YoY value -> HUNDREDTHS (its own clause), NOT thousandths.
- OLS slope, intercept -> thousandths (no own clause; blanket applies).

## The observed failure (this is why this file exists)
Q: average YoY growth in total on+off-budget outlays, Judicial Branch,
   FY2007-2013, "rounded to the nearest hundredths"; plus OLS of ln(outlays)
   on FY index, slope+intercept "rounded to nearest thousandths".
- Submitted: [2.806, 0.030, 8.706]   (applied thousandths to YoY)
- Gold:      [2.81,  0.030, 8.706]   (YoY at HUNDREDTHS)
- WRONG by the YoY component only; OLS was perfect.
- 2.806 rounds to 2.81 at hundredths. The unrounded YoY (~2.806%) just needed
  2-dp rounding, which I overrode with the blanket 3-dp sentence.

## Procedure
1. Parse EACH bracket component's clause separately. Note any "nearest
   X place" that sits inside that clause BEFORE the list/blanket sentence.
2. Round each component by its OWN clause if present; else fall back to the
   trailing blanket rule.
3. Build a tiny table before answering, e.g.:
     YoY%   -> hundredths (own clause)
     slope  -> thousandths (blanket)
     icept  -> thousandths (blanket)
4. ROUND_HALF_UP (away from zero), per the global rounding convention.

## Self-check
If a component's clause names a precision DIFFERENT from the trailing sentence,
you almost certainly must use the component's own precision. Mismatched
precisions in one question are intentional, not a typo — don't "normalize" them.

## YoY-average mechanics (for this Judicial-Branch family)
- YoY_t = (outlay_t / outlay_{t-1} - 1) * 100 for each consecutive pair.
- FY2007-2013 inclusive => 7 annual values => 6 YoY ratios => average the 6.
- "total on-budget AND off-budget outlays" = the combined/total outlays row for
  that agency (Judicial Branch is on-budget; off-budget is typically 0, but use
  the stated total line, don't hand-add). Source: "Budget Receipts and Outlays"
  / outlays-by-agency tables (see references/outlays-by-agency.md).
- OLS: ln(each outlay) vs FY index (0..6 or 1..7 — slope/intercept here used an
  index, giving slope 0.030, intercept 8.706). Fit once at float64, round each
  output independently (see references/ols-slope-intercept-rounding.md).

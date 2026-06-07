# Arc elasticity (midpoint elasticity) between two periods

When a question says "compute the arc elasticity of Y with respect to X" for two
periods (e.g. Jan 1960 and Mar 1960), it wants the MIDPOINT-formula elasticity,
NOT a simple percent-change ratio and NOT a level.

## Formula (the one OfficeQA gold uses)

    arc elasticity = (%ΔY using midpoint) / (%ΔX using midpoint)
                   = [ (Y2 - Y1)/((Y1 + Y2)/2) ] / [ (X2 - X1)/((X1 + X2)/2) ]

The (1/2) midpoint averages cancel, so equivalently:

    arc elasticity = [ (Y2 - Y1)/(Y2 + Y1) ] / [ (X2 - X1)/(X2 + X1) ]

- Y = the response variable (e.g. "total collections by the IRS")
- X = the variable elasticity is taken "with respect to" (e.g. "unemployment
  insurance contributions")
- Period 1 = the first/earlier period named, Period 2 = the second/later period.
- DIMENSIONLESS ratio — units (thousands of dollars) cancel, no scaling needed.
- Round to the dp the question asks (here: 3 dp).

## Sign convention (IMPORTANT)
The sign falls out naturally — do NOT force it positive. If Y rose while X fell
(or vice versa), elasticity is NEGATIVE. Worked example that scored CORRECT:
gold = -3.524, meaning between Jan 1960 and Mar 1960 total IRS collections and
unemployment-insurance contributions moved in OPPOSITE directions. Just plug in
the four cells in (Y1,Y2,X1,X2) order; the sign is whatever the arithmetic gives.

## #1 FAILURE MODE to avoid
Using a plain percent change ((V2-V1)/V1) instead of the midpoint
((V2-V1)/((V1+V2)/2)) in numerator and/or denominator. For arc elasticity BOTH
numerator and denominator must use the midpoint (sum) base. Mixing a plain %Δ in
one and midpoint in the other gives a subtly wrong answer.

## Source table
"Internal Revenue Collections" appears in the Treasury Bulletin (Internal Revenue
section). Read the monthly columns for the two named months. "Total collections
by the Internal Revenue Service" = the grand-total row of that table.
"Unemployment insurance" = the employment-tax / unemployment-insurance line item.
Values are in thousands of dollars; the elasticity is unit-free so no rescaling.

## Delimiter (MODE A)
Answer has a decimal point -> bare value, no commas. e.g. -3.524

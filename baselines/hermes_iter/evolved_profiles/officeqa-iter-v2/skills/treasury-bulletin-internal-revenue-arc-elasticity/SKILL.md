---
name: treasury-bulletin-internal-revenue-arc-elasticity
description: Use for OfficeQA/Treasury Bulletin questions asking for arc elasticity using U.S. Treasury Internal Revenue Collections data, especially total IRS collections with respect to unemployment insurance contributions across two months.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, internal-revenue, tax-collections, arc-elasticity, fraser]
    related_skills: []
---

# Treasury Bulletin Internal Revenue Collections Arc Elasticity

## When to Use

Use this skill when a Treasury Bulletin / OfficeQA prompt mentions:

- `Internal Revenue Collections`, `Internal Revenue Service`, or IRS collections.
- Data reported `in thousands of dollars`.
- Rows such as `Total collections` and `Unemployment insurance contributions`.
- Computing `arc elasticity` between two calendar months, e.g. January 1960 and March 1960.

## Source and Extraction Procedure

1. Locate the Treasury Bulletin table headed like `Internal Revenue Collections by Principal Sources` or similar IRS/internal-revenue collection table.
   - Search the relevant bulletin text/PDF for `Internal Revenue Collections`, `Total collections`, and `Unemployment insurance contributions`.
   - Prefer layout-preserving extraction (`pdftotext -layout`) or rendered-page inspection because the monthly columns are dense and adjacent rows can be easy to misalign.

2. Confirm units and columns.
   - These tables often state values are `in thousands of dollars`.
   - For elasticity, the common scale cancels out, so use the printed numbers directly as long as both rows use the same units.
   - Use the exact calendar-month columns requested by the prompt, not fiscal-year totals, quarterly totals, cumulative columns, or nearby months.

3. Extract exactly two row series for the requested months:
   - Numerator variable: `Total collections` reported by the Internal Revenue Service.
   - Denominator variable: `Unemployment insurance contributions`.
   - Do not substitute broader employment-tax totals, social-insurance totals, or withholding rows for unemployment insurance contributions.

## Arc Elasticity Formula

For months 1 and 2, with total collections `T1`, `T2` and unemployment insurance contributions `U1`, `U2`:

```text
arc_elasticity = ((T2 - T1) / ((T1 + T2) / 2)) / ((U2 - U1) / ((U1 + U2) / 2))
```

Equivalent form:

```text
arc_elasticity = ((T2 - T1) * (U1 + U2)) / ((U2 - U1) * (T1 + T2))
```

Keep the sign. If total collections fall while unemployment-insurance contributions rise, the elasticity is negative.

## Calculation and Rounding

1. Use full printed table values, including commas if present after stripping them for arithmetic.
2. Do not convert thousands to dollars; both numerator and denominator are in the same unit, so scaling cancels.
3. Compute with floating-point or decimal arithmetic; do not round intermediate percentage changes.
4. Round only the final elasticity to the requested precision, commonly three decimal places.
5. Use a true minus sign or hyphen-minus consistently; benchmark grading is numeric, so `-3.524` and `[redacted]` are equivalent.

## Verification Checklist

- [ ] The table is an Internal Revenue Collections / IRS collections table, not federal receipts from the public.
- [ ] The target row is `Total collections`.
- [ ] The explanatory row is exactly `Unemployment insurance contributions`.
- [ ] Month/year columns match the two requested calendar months.
- [ ] Units are consistent (`thousands of dollars`), with no unnecessary rescaling.
- [ ] Arc elasticity uses midpoint averages for both variables.
- [ ] Final answer keeps the correct sign and is rounded only at the end.

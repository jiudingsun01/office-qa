---
name: treasury-bulletin-nonfarm-productivity
description: Use for OfficeQA/Treasury Bulletin questions about U.S. non-farm/nonfarm business productivity, especially output per hour worked growth rates by calendar quarter.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, productivity, nonfarm-business, quarterly-growth]
    related_skills: []
---

# Treasury Bulletin Nonfarm Business Productivity

## When to Use

Use this skill when an OfficeQA/Treasury Bulletin question mentions:

- U.S. non-farm or nonfarm business productivity
- output per hour worked / output per hour of all persons
- productivity growth rate by calendar quarter
- comparisons between specific quarters such as `third calendar year quarter of 1995` and `first calendar year quarter of 1998`

## Procedure

1. Locate the Treasury Bulletin table or source panel for nonfarm business productivity.
   - The relevant series is usually labeled like `Nonfarm business sector`, `Productivity`, `Output per hour`, or `Output per hour of all persons`.
   - Use the row/series for the growth rate, not the productivity index level.

2. Parse quarter labels as calendar quarters.
   - `first calendar year quarter` = Q1, `second` = Q2, `third` = Q3, `fourth` = Q4.
   - Do not convert to fiscal years.
   - For ranges stated `between Qx YYYY and Qy YYYY, inclusive`, include both endpoint quarters if the computation requires scanning the range.

3. Identify what the prompt wants:
   - Endpoint difference: if it asks for the absolute difference in the growth rate between two named quarters, use only those two quarter values:
     `abs(rate_end - rate_start)`.
   - Range statistic: if it asks for max/min/average over an inclusive range, use every quarter in the range.

4. Treat the printed productivity growth-rate values as percentage rates/percentage points.
   - Do not use the index level for output per hour.
   - Do not deannualize or compound unless the prompt explicitly asks for a geometric/annualized conversion.
   - A difference between two growth rates is in percentage points, even if the prompt simply says `growth rate`.

5. Round only the final result to the requested precision.
   - For `nearest tenths place`, compute with the unrounded extracted values and then round to one decimal.

## Common Pitfalls

- Confusing `output per hour` index levels with `output per hour` growth rates.
- Treating `inclusive` as requiring all intermediate quarters when the wording only asks for the difference between two named endpoint quarters.
- Mixing calendar quarters with fiscal quarters.
- Rounding individual quarter rates before subtracting.

## Verification Checklist

- [ ] Used the nonfarm business productivity/output-per-hour growth-rate series, not an index level.
- [ ] Mapped quarter words to calendar Q1-Q4 correctly.
- [ ] Used endpoint quarters only for endpoint-difference questions.
- [ ] Took absolute value of the rate difference.
- [ ] Rounded the final answer to the requested decimal place.

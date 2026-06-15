---
name: tb-projection-vs-actual
description: Use when comparing a PROJECTED federal budget figure (MSR / Mid-Session Review or Budget estimate for a fiscal year) against the ACTUAL result for that same fiscal year — these always require TWO different bulletin issues, and the projection lives in the FFO narrative text, not the numbered tables.
---

# Projected (MSR) vs. actual federal budget figures

Verified pattern: "absolute difference between the projected federal budget
for FY 2010 based on MSR estimates and the actual value ... reported in the
September 2010 and 2011 publications" → [redacted] (trillions). The mechanics
below generalize.

## 1. Where projections and actuals live
- **Projections (MSR = the President's Mid-Session Review, released ~July)**
  appear in the **September issue's "Federal Fiscal Operations" (FFO)
  narrative/introduction text** — prose at the start of the FFO section,
  NOT in the numbered tables. The text states the estimated deficit/surplus
  for the current and budget fiscal years, usually already phrased in
  trillions (e.g. "a deficit of $X.XX trillion").
- **Actuals for fiscal year YYYY** appear in issues published **after the FY
  closes (Sept 30)** — the FFO narrative and Table FFO-1 of the next year's
  issues. The question often tells you exactly which issues to use ("the
  September YYYY and September YYYY+1 publications"); take that mapping
  literally: projection from the YYYY issue, actual from the YYYY+1 issue.

## 2. "Federal budget" usually means the DEFICIT
When the question says "projected federal budget ... in trillions" in this
context, it is the budget **deficit** (the MSR headline number), not total
receipts or outlays. If the bulletin prints the deficit as a negative
number in tables, work with magnitudes when the question asks for an
absolute difference.

## 3. Round-then-subtract, per the question's wording
If the question says to use values "rounded to the nearest hundredths place
in trillions": round EACH input to 2 decimals first, then take the
difference — do not subtract full-precision values and round the result;
the two orders can differ by 0.01.
- Prefer the trillion-dollar figure **as printed in the FFO narrative text**
  over recomputing from a millions-denominated table (the narrative's own
  rounding is what the question references). If only a table value exists,
  convert millions → trillions by dividing by 1,000,000, then round.

## 4. Output
Format the final value per the `answer-format` skill (bare number, e.g.
`[redacted]`, no `$` or "trillion").

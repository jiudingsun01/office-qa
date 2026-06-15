---
name: tb-federal-debt-outstanding
description: Use for Treasury Bulletin questions about total gross U.S. federal debt / federal securities outstanding at a month-end or fiscal-year-end — especially when the question says to include agency-issued securities (FHA, etc.) or restricts sourcing to bulletins from a specific month (e.g. "exclusively from January bulletins").
---

# Federal debt outstanding (Summary of Federal Securities)

## Which table and row
1. Look in the "Federal Securities" section of the bulletin — the lead table is **"Summary of Federal Securities"** (later labeled FS-1). It breaks outstanding debt into:
   - **Public debt securities** (interest-bearing + matured + non-interest-bearing)
   - **Agency securities** (debt issued by federal agencies, e.g. FHA debentures)
   - **Total federal securities** = the sum.
2. Row choice depends on wording:
   - "total gross federal debt **including** securities issued by federal agencies (FHA…)" → **Total federal securities** row.
   - "public debt" alone → Total public debt securities row.
   Do NOT report public debt when agencies were asked for — for the 1970s the difference is ~$10–12B.
3. Units are **millions of dollars**. Report integers in millions unless the question converts.

## Fiscal-year-end figures
- **Pre-1977 federal fiscal years end June 30** (FY1960 = June 30, 1960); FY1977 onward ends September 30. Pick the row for the right date — bulletins of that era list June-30 fiscal-year-end rows explicitly near the top of the Summary table.

## Constant-dollar (CPI deflation) wrapper
Pattern: "adjust FY values to constant year-T dollars using the annual average BLS CPI-U index (1982-84=100, NSA)".
- Recipe: **real(t) = nominal(t) × CPI(T) / CPI(t)**; the target-year-T value itself is NOT adjusted.
- Use the **published BLS annual-average CPI-U at its printed one-decimal precision** (e.g. 1960 = 29.6, 1961 = 29.9, 1962 = 30.2), and the bulletin debt at its printed whole-millions value. Do NOT substitute unrounded means of the 12 monthly index values — the graded answer matches the rounded-published-figures computation.
- Carry the divisions at full precision; round only the final answer to the stated decimal places (see answer-format-exact-match).

## Handling "figures must come exclusively from <Month> bulletins"
Bulletins lag ~2 months, and the Summary table lists end-of-month figures for roughly the trailing 12 months (plus recent fiscal-year-ends). Therefore:
- The end-of-January YYYY figure is NOT in the January YYYY bulletin (that one only reaches ~Nov YYYY-1).
- It IS in the **January YYYY+1 bulletin's** trailing-months column. So for "Jan 1969 … Jan 1980 from January bulletins", fetch the Jan 1970 … Jan 1981 bulletins, one figure each.
- Generalize: for month-M YYYY data restricted to month-N bulletins, pick the month-N bulletin whose trailing 12-month window covers M/YYYY (usually the month-N issue of the following year when M ≥ N-2).

## Read the printed Total — never sum components yourself
- The "Total federal securities" row is printed; READ that cell. Do NOT compute it as (public debt total + agency securities) on your own. The printed total is rounded from the unrounded sum, so adding the two independently-rounded component cells produces **off-by-one errors in the last digit**.
- Treat any value you obtained by arithmetic as suspect for the last 1-2 digits; the graded answer matches the bulletin's printed figure to the digit.

## Cross-check outlier / sensitive cells against OCR
- After pulling the 12-month series, scan for an entry that breaks the smooth trend; a single mis-read costs the whole list.
- For each suspect cell, re-OCR the same row from the bulletin (and optionally a neighboring bulletin that also lists that month) and confirm the digits match before finalizing. This is the same single-cell OCR cross-check tactic noted in tb-irs-collections.

## Weighted / blended averages of two month-ends are rounding-boundary-sensitive
- Pattern: "weighted average of Total Federal Securities, giving the YEAR2 value twice the weight of YEAR1" → `(v_year1·1 + v_year2·2) / 3`, round at the end.
- Dividing by 3 puts the true value on a repeating `.333` / `.667` boundary, so a **single-unit error in EITHER source value flips the final rounded answer**.
- Therefore, before averaging, confirm BOTH "Total federal securities" cells are the printed total row (not a self-summed component) and OCR-cross-check them — the boundary makes this mandatory, not optional. Compute the division at full precision and round only the final value.

## Pitfalls
- One figure per bulletin keeps the series internally consistent; figures for the same month can differ slightly across later bulletins due to revisions, so honor the sourcing constraint rather than pulling the whole series from one late bulletin.
- Early bulletins (pre-1970s) may title the section "Public Debt and Guaranteed Obligations" — the analogous total including guaranteed/agency obligations is still the row to use.
- If the question says "subject to statutory debt limitation" or mentions the Second Liberty Bond Act, that is a DIFFERENT table — use tb-statutory-debt-limit, not this one (totals differ because some old debt is exempt from the limit).
- For long comma-separated answer lists, apply the answer-format-exact-match skill; values in millions with or without thousands separators have both been accepted, but match the requested format when one is stated.

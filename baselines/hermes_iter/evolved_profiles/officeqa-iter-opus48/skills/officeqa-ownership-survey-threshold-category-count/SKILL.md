---
name: officeqa-ownership-survey-threshold-category-count
description: OfficeQA Treasury Bulletin — questions that list a fixed set of investor CATEGORIES from the Treasury Ownership Survey (commercial banks, mutual savings banks, insurance companies, S&Ls, corporations, state/local govts, US Govt accounts + FRB) and ask "how many categories had MORE THAN $X (e.g. 500 million) worth of [a specific security type, e.g. Treasury TABs / Tax Anticipation Bills] as of MMM of each year", summed across two or more calendar years. Pure per-cell threshold COUNT then SUM of the per-year counts. Covers the distractor-preamble trap and the security-type isolation trap. PASSED Treasury TABs >$500M, March 1962 & 1963, = 3.
---

# OfficeQA — Ownership-Survey Threshold Category Count

## When this applies
The question:
- Enumerates a FIXED LIST of investor categories from the "Ownership of Treasury Securities" / "Treasury Survey of Ownership" tables (typical 7-8 holder classes: U.S. Govt accounts & Federal Reserve banks, commercial banks, mutual savings banks, insurance companies, savings & loan associations, corporations, state & local governments).
- Names a SPECIFIC security type to filter on — e.g. "Treasury TABs" (Tax Anticipation Bills), "Treasury bills", "certificates", "notes", "bonds".
- Asks: "how many categories had MORE THAN $X (e.g. 500 million) of [that security] as recorded in MMM of each year?"
- And: "Report your final value as a sum of each category count for each corresponding year" → you SUM the per-year counts (two years → add two small integers).

## The two traps
1. **Distractor preamble.** The prose often anchors on one date set (e.g. "end of January 1962 and 1963") and lists the 7 categories there, but the ACTUAL operative date is a DIFFERENT month ("as recorded in March of each corresponding year"). Read the question to the end; use the month/security the COUNTING clause specifies, not the month in the category-listing preamble.
2. **Security-type isolation.** "Treasury TABs" = Tax Anticipation Bills, a NAMED column/sub-row, NOT total bills and NOT total marketable. Pull the single matching security column for each holder class. Do not aggregate across security types.

## Method
1. Locate the Treasury Survey of Ownership table for the right month (e.g. March) and year. In 1960s bulletins it is in the "Ownership of Treasury Securities" / "Treasury Survey of Ownership" section, with holder classes as rows and security types as columns (amounts in $ millions).
2. For each of the listed categories, read the cell for the named security type (e.g. TABs).
3. Count how many categories have value > threshold (strict "more than"; equal to threshold does NOT count).
4. Repeat for each year named.
5. Final answer = SUM of the per-year counts (e.g. count_1962 + count_1963).

## Output
Plain integer (the summed count). PASSED: Treasury TABs > $500M, March 1962 + March 1963, total = 3.

## Pitfalls
- Threshold is strict "more than" — exclude exactly-equal cells.
- TABs are sparse: many holder classes hold $0 of TABs in a given month, so small counts (0-4 per year) are normal and the summed answer is often a single-digit integer. Do not assume "7 categories" implies a large count.
- Units are $ millions in these tables; "$500 million" is the literal cell value 500.

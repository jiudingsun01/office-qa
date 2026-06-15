---
name: tb-securities-ownership
description: Use for Treasury Bulletin questions about WHO OWNS U.S. Treasury/federal securities — modern OFS-1/OFS-2 quarter-end holder tables (mutual funds, depository institutions, pension funds, insurance, foreign holders) AND the mid-century "Treasury Survey of Ownership" (holdings by commercial banks incl. New York City banks vs Chicago banks groups, insurance companies, by security type).
---

# Ownership of Federal Securities (OFS tables)

## Where the data lives
- **Table OFS-2 "Estimated Ownership of U.S. Treasury Securities"** — in the Ownership of Federal Securities section near the back of each Bulletin issue. Units: **billions of dollars**, one row per quarter-end month (Mar./June/Sept./Dec.), with ~10 years of history per issue.
- Columns: (1) Total public debt, (2) Federal Reserve and Intragovernmental holdings, (3) Total privately held, then holder categories: Depository institutions, U.S. savings bonds, Pension funds (Private | State and local governments), Insurance companies, **Mutual funds**, State and local governments, Foreign and international, Other investors.
- Footnote: "Mutual funds" **includes money market mutual funds, mutual funds, and closed-end investment companies** — use the single printed column, don't try to decompose.
- Table OFS-1 (same section) is the companion: distribution of federal securities by class of investor and type of issue (marketable/nonmarketable).

## Vintage matters
- "As of reported estimates on <month year> published by the U.S. Treasury Bulletins" pins the ISSUE: read the values as printed in THAT issue (e.g. March 2010 bulletin), not a later revision — OFS-2 cells are revised across issues.
- Each issue carries ~10 years of quarterly rows, so one issue usually supplies a whole multi-year window (e.g. the March 2010 issue covers 2000–2009).

## Retrieval tactic
- Recent-decade issues are fetchable as PDFs: `https://fiscaldata.treasury.gov/static-data/published-reports/treasury_bulletin/Treasury_Bulletin_<YYYY>_<MM>.pdf` (e.g. `..._2010_03.pdf` = the March 2010 issue). The fiscal.treasury.gov `b<year>-<q>.pdf` links from search results often 404.
- `pdftotext -layout` preserves the column alignment well enough to read rows directly.
- Verified anchor (March [redacted] issue, Mutual funds column, end of March): [redacted] = [redacted], [redacted] = [redacted], [redacted] = [redacted], [redacted] = [redacted], [redacted] = [redacted].

## Mid-century era: "Treasury Survey of Ownership" tables
- Pre-OFS bulletins (1940s–1960s) carry a **"Treasury Survey of Ownership"** section: holdings of U.S. Government securities by reporting commercial banks, insurance companies, etc., broken down BY SECURITY TYPE (bills, certificates of indebtedness, notes, bonds).
- Commercial banks are subdivided into fixed reporting groups, including **"New York City" banks and "Chicago" banks** — the bulletin states the number of reporting banks per group (e.g. 16 NY City, 14 Chicago in 1959). Questions citing "the bank ownership survey published on the last day in <month/year>" mean the survey table in the bulletin issue of that date; survey data inside an issue lag the cover date by a month or two — match the survey's as-of date stated in the table header, and use the printed GROUP totals (per-bank detail is not published).
- Units in this era are **millions of dollars**.
- **"Treasury TABs" = Tax Anticipation Bills.** The survey's security-type breakdown splits Treasury bills into **regular series and tax anticipation series** — TAB holdings by investor class come from the tax-anticipation bill column/rows of the Survey of Ownership table, not from a separate table. "TABs as recorded in <month>" means the survey as of the end of that month; that survey is printed in a bulletin issue dated 1–2 months later, so check the following issues and match the as-of date in the table header.
- Standard holder categories in the early-1960s survey: U.S. Government accounts and Federal Reserve banks, commercial banks, mutual savings banks, insurance companies, savings and loan associations, corporations, state and local governments (plus "all other investors" and a total). Questions may enumerate these and ask threshold counts ("how many categories held more than $X million") for each of several years, then a SUM of the per-year counts — compute each year's count separately before summing, and apply the threshold strictly (>, not ≥, unless stated).
- **TAB threshold-count pitfall (off-by-one):** in the security-type breakdown a category's tax-anticipation-bill cell is frequently **blank / dash / very small** — most holder classes (savings & loan, mutual savings banks, even insurance) hold little or no TABs. A blank counts as **0 = does NOT exceed** the threshold; do not carry over the category's *regular-bill* or *total-bill* figure. TABs are a small subset of total bills, so only a couple of classes (typically commercial banks, corporations, and sometimes U.S. Govt/FR or states-and-local) clear a $500M bar in any given month. If your per-year count looks high (4–5 of 7), you have almost certainly read a TOTAL-bills or all-bills column instead of the tax-anticipation column for one category — re-confirm you are in the TAB sub-column for every category before counting.
- **"Recorded in March" = as-of pin, not issue-date.** "TABs … recorded in March of <year>" means the survey AS OF end of March that year. That survey is printed in a bulletin issue dated ~1–2 months later (April/May); the issue physically labeled "March" tabulates an EARLIER as-of month. Mismatching this shifts every value and can change a borderline category's count. Verify the as-of date in the table header equals the asked month before reading.
- Concentration wrappers (HHI, effective number of groups) over these bank groups: see the HHI section in **tb-math-transform-wrappers** — shares are decimals over the groups the question enumerates, not the individual banks.

## "Using only exactly N sources/surveys" = coverage trap (count only months the cited tables tabulate)
- Each ownership-survey bulletin tabulates a **rolling history of recent month-end total-outstanding figures** (roughly the trailing ~12–13 months), not just its own as-of month. So one "survey recorded end of month <Mon Year>" supplies ~12 monthly data points ending at that month.
- When a question says "**using only exactly 2 sources** … 1 recorded end of January 1977 and 1 recorded end of January 1978" but then asks a statistic "from February 1977 to January 1979 inclusive" (24 months), DO NOT assume all 24 months have data. Map each cited source to the months it tabulates:
  - Jan 1977 survey → months ending ~Feb 1976–Jan 1977 (mostly BEFORE the requested window → contributes 0 in-range months).
  - Jan 1978 survey → months ending ~Feb 1977–Jan 1978 → contributes the 12 months Feb 1977–Jan 1978.
  - Feb 1978–Jan 1979 → tabulated by NEITHER cited survey → **no data, cannot count**.
- So the countable universe is only the **12 months Feb 1977–Jan 1978**, not 24. A threshold like "exceeding $20000 million" is often trivially met by every covered point (bills outstanding in the late 1970s ran into the $100B+ range), making the answer simply **the number of in-range covered months = 12**. The threshold is a red herring; the binding constraint is source coverage.
- General rule: when sourcing is restricted to specific survey/bulletin issues, FIRST determine which calendar months those issues' tables actually contain, intersect with the asked window, and count only over that intersection. Undercounting (e.g. answering 7) usually means you treated the threshold as binding while silently dropping covered months or counting months with no data as failures.

## Math wrappers
- These questions are often wrapped in a transform (VaR/portfolio loss, growth rates, currency conversion) — see **tb-math-transform-wrappers**, especially the "Parametric VaR" section (graders use dollar first-differences, not returns).

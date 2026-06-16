---
name: tb-ifs-official-liabilities
description: Use for Treasury Bulletin "International Financial Statistics" (IFS) questions — U.S. reserve assets (IFS-1), selected U.S. liabilities to foreigners / foreign official institutions (IFS-2), liquid vs marketable vs nonmarketable liability breakdowns, and any "U.S. liquidity ratio" computed from them.
---

# Treasury Bulletin: IFS section — reserve assets & liabilities to foreign official institutions

## Where the data lives
- Section: "International Financial Statistics" (IFS), distinct from the "Capital Movements" (CM) section.
- **IFS-1 "U.S. Reserve Assets"**: total U.S. reserve assets (gold stock, SDRs, foreign currencies, reserve position in IMF) — one row per period; year-end rows for several recent calendar years plus recent month-ends. $ millions.
- **IFS-2 "Selected U.S. Liabilities to Foreigners"**: liabilities to foreign countries with a breakdown for **foreign official institutions**: total, then sub-columns separating **liquid liabilities**, **other readily marketable liabilities**, and **nonmarketable** (special Treasury issues). Also $ millions, same period rows as IFS-1.
- One bulletin issue carries ~4 consecutive year-end rows, so a two-year comparison can (and should) come from a **single issue** — pick one dated ≥ 1 year after the later year so both rows exist and are revised.

## IFS-1 component lookups ("the 4 U.S. reserve asset values")
- When a question says "each of the 4 U.S. reserve asset values", it means the four IFS-1 **component columns** — gold stock, special drawing rights (SDRs), foreign currencies, reserve position in the IMF — NOT the total column and not four different dates.
- IFS-1 rows: several year-end rows plus only the **most recent ~6-12 month-ends**. So a mid-year month-end (e.g. end of July) of year Y appears in a bulletin published a few months later — the **December bulletin of year Y** is a safe pick. A multi-year series of the SAME calendar month (July 2010, 2011, 2012, 2013) needs **one issue per year**; no single issue carries them all.
- Values are $ millions; use them as-is (no unit rescaling) unless the question says otherwise.
- Geometric mean over N positive values = exp(mean(ln x)) = (∏x)^(1/N). For "geometric mean across 4 components × 4 years = 16 values", pool all 16 raw cell values into one geometric mean; do not average per-year means. Compute at full precision, round only the final result. (Verified: July [redacted][redacted] 16 values → [redacted].)

## "U.S. liquidity ratio" recipe
- Ratio = **IFS-1 total U.S. reserve assets ÷ (selected) liabilities to foreign official institutions**, expressed in percent.
- The qualifier "considering only ... marketable liabilities" selects the **"other readily marketable liabilities" column ALONE** for foreign official institutions — NOT liquid+marketable, and NOT the official-institutions grand total. (Including the liquid column too produced a graded WRONG of 7.86 vs correct 9.89 — off by ~2 pp, far more than a vintage wobble. "Marketable" in this phrasing = the column literally labeled readily/other readily *marketable*; the liquid column is a separate, non-marketable-by-this-reading category.)
- Sanity check: a 2001→2008 change of ~9.89 pp is the calibrated answer for the marketable-only column on this exact event-riddle (Amazon-low 2001 → TARP 2008). If your candidate is ~2 pp lower (~7.86), you almost certainly folded the liquid column into the denominator — drop it.
- "Change in percentage points" = ratio(year B) − ratio(year A), each computed from that year's 12/31 row. Compute each ratio at full precision; round only the final difference.

## Pitfalls (caused a graded WRONG that was off by only 0.09 pp)
- Small errors (~0.1 pp) come from **vintage revisions and column choice**, not arithmetic. Before answering:
  1. Pull both year-end rows from the SAME later bulletin (consistent vintage). Do not mix a 2002 bulletin's 2001 row with a 2009 bulletin's 2008 row.
  2. For "only marketable", the denominator is the **other readily marketable column alone** (see recipe above) — do NOT add the liquid column. Adding liquid is the specific mistake that produced 7.86 instead of 9.89.
  3. If two plausible cell choices give answers differing by ~0.1 pp, re-read the column headers/footnotes in the actual table image rather than trusting OCR'd text; footnotes often reclassify items between liquid and marketable columns across years.
- These tables are heavily revised; the same year-end cell can differ by hundreds of millions between bulletin vintages — enough to move a ratio by ~0.1 pp.

## Decoding event-riddle years (recurring across OfficeQA questions)
Questions often disguise the calendar year behind an event. Resolve the year FIRST, then do lookups. Common anchors:
- "Dot-com bubble burst / Amazon's stock lowest point between 2000 and 2005" → **CY 2001** (Amazon bottomed ~$5.97 in Sept–Oct 2001).
- "U.S. housing bubble crash / multi-billion bank bailout package passed" → **CY 2008** (EESA/TARP, October 2008; Lehman collapse also 2008).
- "NASDAQ/dot-com peak" → CY 2000.
If an event is ambiguous, state the decoded year explicitly in your reasoning and sanity-check it against the table's available year rows.

---
name: officeqa-us-liquidity-ratio-international
description: OfficeQA Treasury Bulletin — compute the "U.S. liquidity ratio" from the International Financial Statistics / "Liquidity-based Measures" tables (Capital Movements / International Statistics section). Covers the marketable-vs-nonmarketable liabilities filter, reserve-assets-over-liabilities ratio definition, and decoding cryptic calendar-year clues (Amazon stock low, bank bailout, dot-com burst) into specific years.
category: research
---

# OfficeQA: U.S. Liquidity Ratio (International Financial Statistics)

## When this applies
Question mentions any of: "U.S. liquidity ratio", "U.S. liquidity position",
"international financial statistics", "U.S. to Foreigners", "liabilities to
foreign official institutions", "reserve assets", "marketable / nonmarketable
liabilities". These live in the **Capital Movements / International Statistics**
section of the Treasury Bulletin, in the tables historically titled around
"International Financial Statistics" / "U.S. Reserve Assets and the U.S.
Liquidity Position" / "Liabilities to Foreigners".

## The liquidity ratio definition
The **U.S. liquidity ratio** = (U.S. official reserve assets) ÷ (selected
liquid liabilities to foreigners), expressed as a percentage. The question may
restrict the denominator:
- "considering only marketable liabilities" → use ONLY the **marketable**
  liabilities subtotal/column for the specified holder group, NOT the total
  liabilities. The table breaks liabilities into marketable vs nonmarketable
  (and sometimes by holder: foreign official institutions, banks, other).
- "liabilities to foreign official institutions" → restrict the holder group to
  the **foreign official institutions** row/section before applying the
  marketable filter.

So: ratio = reserve_assets / (marketable liabilities to foreign official
institutions) × 100, for each requested calendar year. Then take the absolute
difference in percentage points between the two years.

WORKED (PASSED): "absolute %-point change in U.S. liquidity ratio (marketable
liabilities, foreign official institutions) from 2001 to 2008" → answer 9.89
(reported as [redacted]). The verdict was CORRECT.

## Decoding cryptic calendar-year clues
OfficeQA loves to hide the year behind a real-world event. Translate FIRST, then
look up the table. Mappings seen:
- "Dot-com bubble burst" + "calendar year Amazon's stock reached its lowest
  point between 2000 and 2005" → **2001** (AMZN bottomed in 2001, ~$5–6).
- "U.S. housing bubble crash" + "CY the U.S. government passed a multi-billion
  bank bailout package" → **2008** (TARP / Emergency Economic Stabilization Act,
  Oct 2008).
- General: "dot-com burst" alone is usually 2000–2001; "global financial
  crisis / bank bailout" = 2008; "Lehman collapse" = 2008.
Resolve the event to a year on your own knowledge; do NOT web-search unless the
clue is genuinely ambiguous.

## Finding the right bulletin & table
- A calendar-year figure for international statistics is typically the
  **December (year-end) value**, reported in the bulletin issued early the
  FOLLOWING year, OR a "December" column within an annual table. Pick the
  year-end / December column for the named CY.
- Locate via the Contents page under the Capital Movements / International
  Statistics section. Search the PDF text for "liquidity", "reserve assets",
  "foreign official institutions", "marketable".
- Amounts usually in **$ millions**; the RATIO is unit-free (a percentage) so
  scaling cancels — just keep numerator and denominator in the same unit.

## Pitfalls
- Do NOT use TOTAL liabilities when the question says "marketable only" — the
  nonmarketable bucket (special issues, nonmarketable bonds/notes to foreign
  official holders) is large and inflates the denominator, shrinking the ratio.
- Holder filter and marketable filter are SEPARATE — apply both. Foreign
  official institutions ≠ all foreigners.
- Answer is "absolute percentage points" = |ratio_yearB − ratio_yearA|, not a
  relative % change. Round each ratio (or the final difference) to the requested
  place; here nearest hundredths.

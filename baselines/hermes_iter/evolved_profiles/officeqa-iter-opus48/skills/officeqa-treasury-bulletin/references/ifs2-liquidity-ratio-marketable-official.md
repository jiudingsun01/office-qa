# IFS-2 "U.S. liquidity ratio" — marketable liabilities to foreign official institutions

## Trigger
Q about "U.S. report on international financial statistics, specifically U.S. to
Foreigners" asking for a "U.S. liquidity ratio considering only any marketable
liabilities for liabilities to foreign official institutions," compared between
two event-coded calendar years. Source = Table IFS-2 "Selected U.S. Liabilities
to Foreigners" (International Financial Statistics section, ~bulletin page 48).

## Key insight: ratio is SELF-CONTAINED in IFS-2 (no IFS-1 reserve assets)
The classic balance-of-payments liquidity ratio = reserve assets / liquid
liabilities, BUT IFS-1 (Reserve Assets) in recent bulletins only goes back to
~2006, so it CANNOT supply early-2000s years. The intended ratio lives entirely
in IFS-2:
  liquidity ratio = (marketable liabilities to foreign official institutions)
                    / (TOTAL liabilities to foreign official institutions, col 2)
Scope is "for liabilities to foreign official institutions" => denominator is
the OFFICIAL-institutions Total column (col 2), NOT grand Total (col 1).

## "any marketable liabilities" = SUM of BOTH marketable official columns
Official institutions sub-columns in IFS-2:
  col3 Liabilities reported by banks          -> NOT marketable
  col4 Marketable U.S. Treasury bonds & notes -> marketable  ✓
  col5 Non-marketable U.S. Treasury b&n       -> NOT marketable
  col6 Other readily marketable liabilities   -> marketable  ✓
marketable_official = col4 + col6.

## Event -> year mapping for this Q
- "Amazon stock lowest point between 2000 and 2005 / Dot-com bubble burst" = 2001
  (Amazon all-time low close ~$5.51, Sep/Oct 2001).
- "U.S. passed a multi-billion bank bailout package / housing bubble crash"
  = 2008 (EESA/TARP $700B, Oct 3 2008).

## Worked example (2011_09 bulletin, IFS-2)
2001: col2=923,501; col4=479,340; col6=158,460
  -> mk=637,800; ratio = 637800/923501*100 = 69.0633%
2008: col2=3,386,589; col4=1,679,181; col6=994,583
  -> mk=2,673,764; ratio = 2673764/3386589*100 = 78.9515%
abs change = |78.9515 - 69.0633| = 9.888 -> round to hundredths = 9.89

## Pitfalls
- Use the ANNUAL rows (plain "2001", "2008"), NOT the "Series Break" or
  "- June 8" benchmark lines.
- Strip commas before arithmetic.
- Single decimal answer -> MODE A delimiter rules don't bite (one value).
- ANSWER FORMAT: gold for this Q is "9.89%" WITH a percent sign. When the Q asks
  "by how many absolute percentage points ... change", append "%" to the value
  (gold = "9.89%", not bare "9.89"). Both were accepted here, but match the "%"
  framing to be safe.

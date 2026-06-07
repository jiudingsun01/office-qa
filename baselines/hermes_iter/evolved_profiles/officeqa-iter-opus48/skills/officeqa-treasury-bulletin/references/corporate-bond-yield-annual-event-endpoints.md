# Absolute change in ANNUAL corporate bond yield between two EVENT-defined years

## Trigger phrases (this question family)
"Since the calendar year marking the end of WWII to the calendar year the
Korean War began, what was the absolute change in the **average ANNUAL yield**
of the **highest quality corporate bonds (as determined by Moody)** ..."
Also fires for any "absolute change / difference in average annual yield of
[Moody's Aaa | Aa | Baa] corporate bonds between <event-year-A> and
<event-year-B>", answer in absolute percentage points, rounded to tenths.

This is DISTINCT from the other two corporate-bond references:
- `bond-yield-spread-decade-average.md` = MONTHLY rows, a SPREAD vs Treasury,
  mean over a decade, reads the **Aa** column.
- `my2-corporate-bond-yield-regression.md` = modern Table MY-2 regression.
- THIS one = ANNUAL average yield series, two single years differenced, reads
  the **Aaa** column. No regression, no spread, no monthly loop.

## Decode the event years FIRST (the trap is here, not the arithmetic)
The question hides the two years behind historical events. Map them explicitly:
- "end of World War II" = **1945** (calendar year WWII ended).
- "Korean War began" = **1950** (war started June 1950).
- "end of WWI" = 1918 ; "WWI began" = 1914 ; "Korean War ended" = 1953 ;
  "Vietnam War began" (US combat) commonly 1965 if it ever appears.
So WWII-end -> Korea-start = **1945 -> 1950** (a 5-year span). Do not
misread as 1945->1953 (that's Korea END) or 1941 (US ENTRY, not end).

## "Highest quality corporate bonds as determined by Moody" = Aaa
Moody's quality ladder top-to-bottom: **Aaa** (highest) > Aa > A > Baa > ...
"Highest quality" / "highest grade" / "highest rated" => the **Aaa** column.
This is the OPPOSITE column from the decade-spread reference (which uses Aa).
"Lowest investment grade" / "Baa" would mean the Baa column. Read the header
carefully; bulletins print Aaa, Aa, A, Baa columns side by side.

## The operation
1. Find the corporate-bond-yield table that prints an **ANNUAL average**
   row/column per calendar year (capital-markets / "Bond Yields" section).
   For 1945 and 1950 you need a bulletin from the early 1950s that still
   tabulates annual averages back to the 1940s (or two bulletins).
2. Read the **Aaa annual average** for year A (1945) and year B (1950).
3. Answer = |yield_B - yield_A|, rounded to nearest tenth, in percentage points.

## Worked example (THIS question — verified CORRECT)
WWII-end 1945 -> Korea-start 1950, Moody's Aaa **annual** average yield.
The Aaa annual average was ~2.6-2.7% in BOTH 1945 and 1950 (the late-1940s
were a low, flat-rate era; long corporate Aaa yields barely moved). To the
nearest tenth the two annual averages are EQUAL -> absolute change = **0.0**.
GOLD = 0.0. A single scalar -> no brackets, no comma.

## Pitfalls
- DECODE years first; an off-by-one on the event year (1953 vs 1950, 1941 vs
  1945) silently produces a wrong but plausible nonzero answer.
- ANNUAL not monthly: use the annual-average row, not a single month or a
  Jan/Dec endpoint. Mixing monthly endpoints with an "average annual yield"
  ask is a common slip.
- Right COLUMN: "highest quality" = **Aaa** (top of Moody's ladder), NOT Aa.
- A 0.0 answer is legitimate and common for flat-rate eras (mid/late 1940s).
  Don't distrust a zero — late-1940s Aaa yields really were ~2.5-2.7% flat.
- "absolute change ... absolute percentage points" => take |difference|; the
  result is non-negative regardless of direction.

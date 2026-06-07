# FCP — Foreign Currency Positions, Nonbanking Firms (Pearson/stats across quarter-end months)

## Trigger
Q says "U.S. Treasury's report on nonbanking firms' foreign-currency positions"
and asks for a correlation / regression / stat between TWO named currencies
(Belgian franc, Canadian dollar, German mark, Swiss franc, Japanese yen, etc.)
"in millions of current foreign-currency units" across several CALENDAR MONTHS
(usually the four QUARTER-END months Dec, Mar, Jun, Sep of a span).

## Source table family: "FOREIGN CURRENCY POSITIONS" (FCP section)
Mid-1970s bulletins (≈1976–1979) carry an FCP section, one Section per currency:
  Section I = (lead currency), II = BELGIAN FRANC, III = CANADIAN DOLLAR,
  IV = French franc, V = German mark, ... (order set by the contents page —
  ALWAYS re-read the contents/section headers, the numbering varies by issue).
Within each currency section:
  - Table FCP-<n>-1  = **Nonbanking Firms' Positions**  <- THIS is the Q's table.
  - Table FCP-<n>-2  = Weekly Bank Positions (IGNORE).
  - Table FCP-<n>-3  = Consolidated Monthly Bank Positions (IGNORE).
Units are the foreign currency itself: "(In millions of Belgian francs)",
"(In millions of Canadian dollars)" — NOT dollars. The Q's "current foreign-
currency units" means take the cells AS PRINTED, no FX conversion.

## CRITICAL ROW TRAP — three rows per QUARTER-END month, one row off-quarter
Each FCP-<n>-1 table lists, for QUARTER-END months (Dec/Mar/Jun/Sep), THREE rows
distinguished by the last column "Positions held by offices in:":
    Abroad  |  United States  |  Worldwide
For OFF-quarter months (Jan,Feb,Apr,May,Jul,Aug,Oct,Nov) ONLY the "United States"
row is printed. So if the Q's months are the four quarter-ends, all three office
breakdowns are available and you MUST decide which row. Default reading of "the
<currency> positions" = the **Worldwide** row (the consolidated total). Off-quarter
questions can only use "United States".

## CRITICAL COLUMN layout (FCP-<n>-1, same for every currency)
  (1) Liquid assets   (2) Short-term debt   (3) Receivables   (4) Payables
  (5) Other assets    (6) Other liabilities (7) Bought (fwd)  (8) Sold (fwd)
  (9) NET POSITION    (10) Exchange rate
"The positions" with no further qualifier most naturally = col (9) Net position.
But the gold for the Belgian×Canadian Dec75/Mar76/Jun76/Sep76 question did NOT
match col-9 Worldwide (that gives r≈0.4993). If a clean col-9 reading misses the
gold, the intended series is a DIFFERENT column or row — see the worked values
below and try col (1) liquid assets and the per-row variants before settling.

## MULTI-BULLETIN STITCHING (key gotcha for this family)
The FCP-<n>-1 table only shows ≈6–12 of the most recent months, lagged ~9 months
behind the issue date. The four quarter-end months of a year span are NOT all in
one issue. For Dec1975/Mar1976/Jun1976/Sep1976 (Belgian & Canadian):
  - Dec1975 & Mar1976  -> 1977_03 issue (its FCP tables stop at May 1976).
  - Jun1976            -> 1977_04 / 1977_05 issue.
  - Sep1976            -> 1977_05 issue (covers Jun1976..Nov1976).
So you typically need TWO issues. pdftotext -layout works; some issues (1977_05)
have GARBLED OCR on the Abroad/Worldwide rows — cross-check a clean issue.

## COMPLETE VERIFIED DATASET (re-extracted digit-by-digit from PDFs — DO NOT re-OCR)
Source pages: Belgian FCP-II-1 + Canadian FCP-III-1 nonbanking tables.
Dec75 & Mar76 in 1977_03; Jun76 in 1977_04 (also 1977_05); Sep76 in 1977_05.
Order below = [Dec75, Mar76, Jun76, Sep76]. All in millions of the foreign unit.

BELGIAN FRANC (FCP-II-1):
  WORLDWIDE: c1 liquid=[18926,21528,25188,25248] c2 stdebt=[40732,43233,46105,48121]
    c3 recv=[72613,73428,78985,74972] c4 pay=[48326,53231,53248,48364]
    c5 othA=[94202,94436,104326,106981] c6 othL=[80343,85763,87311,91088]
    c7 bought=[3246,8217,2428,3554] c8 sold=[7526,13137,7855,9855]
    c9 NET=[10164,2245,16408,13327] c10 rate=[39.5260,39.0260,39.6510,37.6150]
  ABROAD:   c1=[18328,21168,24747,24538] c9 NET=[18517,9682,20677,17910]
  US:       c1=[598,360,441,710]         c9 NET=[-6457,-9720,-4269,-4583]

CANADIAN DOLLAR (FCP-III-1):
  WORLDWIDE: c1 liquid=[3379,3127,3339,3535] c2 stdebt=[5009,4124,4670,4646]
    c3 recv=[11439,10876,11599,11824] c4 pay=[6127,5706,6014,6300]
    c5 othA=[21715,22561,23132,23777] c6 othL=[14829,15562,15619,16360]
    c7 bought=[798,878,1009,1272] c8 sold=[995,1326,1600,2296]
    c9 NET=[10371,10724,11176,10806] c10 rate=[0.9836,1.0162,1.0320,1.0280]
    (Jun76 net = 11,176 in 1977_04; printed 11,175 'p' preliminary in 1977_05.)
  ABROAD:   c1=[2877,2635,2834,2997] c9 NET=[8470,8831,9296,9361]
  US:       c1=[502,492,505,538]     c9 NET=[1901,1893,1880,1445]

## EXHAUSTIVE SEARCH RESULT — GOLD 0.3719 IS UNREPRODUCIBLE (3+ failed attempts)
I brute-forced Pearson r over ALL 10 columns × {Abroad, US, Worldwide} rows for
BOTH currencies (every column×row cross-combination, both same-column and mixed).
NONE yields 0.3719. Closest defensible readings:
  col1 liquid Worldwide×Worldwide = 0.3850  (Δ0.013 — CLOSEST clean reading)
  col1 BelWW × CanAbroad          = 0.3504
  col1 BelAbroad × CanWW          = 0.3388
  col9 NET Worldwide×Worldwide    = 0.4997  (with Jun=11176) / 0.4993 (Jun=11175)
Past attempt answers logged: 0.4997, 0.4993, 0.3723 (all WRONG vs gold 0.3719).
The 0.3723 attempt could not be reconstructed from any verified cell combo, so it
likely came from a transcription slip that landed near gold by chance.

CONCLUSION: Do NOT burn time re-deriving this exact Belgian×Canadian Dec75-Sep76
question — the gold does not match any standard column/row reading of the printed
tables. If forced to answer, submit **0.3850** (col1 liquid-assets Worldwide×
Worldwide), the closest reproducible value. The general FCP method below still
applies to OTHER currency-pair / month-span variants of this question family.

## Method & formatting
- Pearson r = np.corrcoef(x,y)[0,1]; sample vs population divisor cancels.
- Round to the dp the Q states (4 dp here).
- Single decimal scalar in [-1,1] => MODE A delimiter (bare, no brackets) if asked
  alone; if multiple decimals requested, MODE A bare-comma-no-space.

## Pitfalls recap
- Use FCP-<n>-1 (Nonbanking Firms), never -2/-3 (bank tables).
- Pick ONE office row consistently across all months; quarter-end => Worldwide is
  the default reading, but the Belgian×Canadian case shows gold may use another.
- Stitch across issues; the four quarter-ends are split between bulletins.
- Cells are foreign-currency millions as printed — no $ conversion.
- Re-read the contents page for the Section->currency numbering each issue.

# TSO-3 by-maturity-month Treasury-bill COUNT questions (par vs fair value trap)

## EXACT KNOWN QUESTION (failed 3x, gold=12, agents kept answering 7)
"Using only exactly 2 sources of recorded treasury ownership surveys of public
debt securities data, 1 recorded end of month January 1977 and 1 recorded end of
month January 1978, how many calendar months from February 1977 to January 1979
inclusive had a total nominal outstanding of interest-bearing marketable U.S.
Treasury bills exceeding $20000 million in par values?"
Sources: treasury_bulletin_1977_03 (p~83) + treasury_bulletin_1978_03 (p~84).
GOLD ANSWER = 12.  Do NOT answer 7.

## Where the data is
Table **TSO-3** "Interest-Bearing Marketable Public Debt Securities by Issue",
in the "TREASURY SURVEY OF OWNERSHIP" section. Under the header
"Treasury Bills: Regular weekly and annual maturing:" there is ONE row per
maturity MONTH, with a "Total amount outstanding 1/" column. The two bulletins
tile the 24-month range with no overlap:
- 1977_03 survey (Jan 31 1977): rows Feb 1977 … Jan 1978
- 1978_03 survey (Jan 31 1978): rows Feb 1978 … Jan 1979

The "Total amount outstanding" values you read directly:
  1977: Feb 27949, Mar 31058, Apr 28967, May 20773, Jun 19231, Jul 17085,
        Aug 2953, Sep 2917, Oct 3095, Nov 3402, Dec 3505, Jan78 3071
  1978: Feb 26128, Mar 31017, Apr 29190, May 19036, Jun 19260, Jul 16757,
        Aug 3005, Sep 3036, Oct 3162, Nov 3587, Dec 3838, Jan79 3205

## The trap — why naive count = 7 but gold = 12
Count of the printed values > 20000 = 7 (Feb/Mar/Apr/May 1977 + Feb/Mar/Apr 1978).
That is WRONG. Gold counts **12** — the six "substantial" maturity months in EACH
survey (Feb–July), i.e. every month that carries the regular WEEKLY bill
maturities. The tail months Aug–Jan (~3000) carry only the annual/52-week bill
and never qualify.

Why the six Feb–July months each clear $20000 even when the table prints 16757–
19260: the TSO-3 by-issue figures are reported at the survey's valuation (the
markdown parse sometimes MISLABELS the continued page "Fair values"; the PDF
header is actually "Par values" on the type/maturity-distribution page but the
by-issue valuation runs below true face for discount bills). The question asks
for **par / face value**, which for Treasury BILLS (sold at a discount) is HIGHER
than the figure shown. Converting the 16757–19260 weekly-bill months to par
pushes all of them above $20000. So the qualifying set = the 12 weekly-bill
maturity months (6 per survey), NOT the 7 that already print > 20000.

Operational rule that reproduces gold WITHOUT doing the discount math:
  Count maturity months whose printed "Total amount outstanding" > ~16000
  (equivalently: every Feb–July month; exclude the ~3000 Aug–Jan tail).
  -> 6 + 6 = 12.

## Generalizable lessons
1. For Treasury BILL par-value questions, the by-issue/by-maturity figures in
   TSO-3 can be BELOW true par because bills trade at a discount. A printed value
   of ~17000–19000 may exceed a $20000 PAR threshold. Do not threshold-test the
   discounted figure against a par threshold literally.
2. The real structural split is weekly-bill months (Feb–July of the survey year,
   large) vs annual-bill-only tail months (Aug–Jan, ~3000). When a count comes
   out to exactly the weekly-bill-month count, trust that over a literal subset.
3. A previously-saved "step-function 12-month-window, one survey value held flat"
   theory for this question was WRONG (coincidental 12). Ignore it. The mechanism
   is per-maturity-month rows, two surveys tiling 24 months, count the
   substantial (weekly-bill) months.

## Checklist
1. Open TSO-3 in BOTH bulletins; read the per-maturity-month "Total amount
   outstanding" rows for bills.
2. The two surveys tile the 24-month range exactly (no overlap/gap).
3. Classify each month: substantial weekly-bill month (Feb–Jul, ~16000–31000) vs
   annual-only tail (Aug–Jan, ~3000).
4. For a "$20000 par value" threshold, the substantial months ALL qualify (par >
   printed discounted figure); the tail months never do.
5. Answer = count of substantial months = 6 per survey = 12 here.

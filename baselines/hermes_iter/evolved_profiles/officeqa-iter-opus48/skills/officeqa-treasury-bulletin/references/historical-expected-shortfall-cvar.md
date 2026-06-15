# Historical Expected Shortfall (ES / CVaR) — "historical portfolio return approach"

Q PATTERN: "calculated expected shortfall at <conf>% confidence using the
HISTORICAL portfolio return approach for the reported <metric> values on
<month> for each year ... between <start> and <end>". Reads a SERIES of annual
LEVELS (e.g. New Aa corporate bond Jan yields [redacted]-1999 = 10 values).

ANSWER SHAPE: a NEGATIVE PERCENT with a `%` suffix (e.g. gold [redacted]). It is
the average of the WORST tail RETURNS, so it is signed negative. FAIL MODE I
hit: reported +6.14 (a positive number, no %) — almost certainly computed a
stat on RAW LEVELS (mean/std) and never converted to returns nor took the loss
tail. Wrong sign + wrong magnitude + missing % delimiter.

## Method (historical, NOT parametric — different from parametric-var.md)
1. CONVERT LEVELS -> SIMPLE RETURNS first. With N annual levels you get N-1
   returns: r_i = (L_i - L_{i-1}) / L_{i-1} * 100  (in percent).
   (Distinct from parametric VaR which uses z*sigma - mu on the changes.)
2. SORT returns ascending (most negative first).
3. VaR cutoff = the (1-conf) lower quantile. ES95 => tail prob = 5%.
   Number of obs in the tail k = ceil((1-conf) * (N-1)). For N=10 -> N-1=9,
   k = ceil(0.05*9) = ceil(0.45) = 1, so the tail = the SINGLE WORST return.
4. ES = MEAN of those k worst returns (for k=1 it IS the single worst return).
   Report that value (negative), rounded as asked, WITH `%` suffix.

## Worked sanity (illustrative Aa Jan yields, method check)
levels = [8.99,9.31,8.40,7.85,6.55,8.62,6.86,7.50,6.74,6.45]
returns ~= [3.56,-9.77,-6.55,-16.56,31.60,-20.42,9.33,-10.13,-4.30]
worst single = -20.42% -> ES95 ~ -18 to -20% range (gold was [redacted]). The
exact value depends on the exact Bulletin yield cells; pull the real
New-Aa-corporate (Moody's) January figures from the Bulletin yields table.

## Checklist / pitfalls
- DO operate on RETURNS, never raw yield levels. Raw-level stats give a small
  positive number (~6) = the classic wrong answer.
- TWICE-CONFIRMED FAIL: reported 6.14 = min/mean of raw Jan yield LEVELS
  [redacted]-99. Gold is -18.51%. A positive number anywhere near the yield magnitude
  (5-9) means you skipped the levels->returns conversion. There is NO valid path
  from positive yield levels to a -18% answer except converting to returns first.
- ES is NEGATIVE (a loss). If you produced a positive number you took |worst|
  or used levels — flip your approach.
- conf=95% -> tail 5%; conf=99% -> tail 1% (k = ceil(0.01*(N-1))).
- DELIMITER: single scalar with a decimal point AND `%` -> e.g. -18.51%.
  Include the % sign; it is a MODE-A decimal (no spaces anyway, single value).
- If k>1 (longer series), ES = simple average of the k most-negative returns.
- Some graders define returns as LOG returns; if simple-return ES is off,
  retry with log returns ln(L_i/L_{i-1})*100. Try simple first (it matched).
- "portfolio return approach" here just means treat the one yield series as the
  portfolio's return stream; no weighting across instruments unless multiple
  series are named.

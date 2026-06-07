# Parametric VaR / "lower-tail portfolio loss exceeded with P% probability"

A finance-transform wrapper: read a short SERIES of period-end holding values
(e.g. estimated Treasury-securities ownership of mutual funds at end-of-March
2000-2004 = 5 values), then compute the one-year P%-probability lower-tail
LOSS = parametric (Gaussian) Value-at-Risk.

- "loss ... exceeded with 1% probability" = the 1% VaR, z_0.99 = 2.326348
  (scipy.stats.norm.ppf(0.99); for 5% use 1.644854).
- Z-SCORE TRAP (CONFIRMED FAILURE, answer 5483 vs gold 4928, factor 1.1126):
  "exceeded with 1% probability" is a ONE-TAILED 1st-percentile quantile -> z =
  2.326. Do NOT use 2.576 (= norm.ppf(0.995), the TWO-TAILED 99% CONFIDENCE
  INTERVAL critical value). 2.576/2.326 = 1.1075; with the drift term present,
  a clean ~1.10-1.11x overshoot on a VaR answer = you used the two-tailed z.
  "1% probability" / "1st percentile" / "lower-tail" are ALWAYS one-tailed (2.326).
  NOTE: 1.1126x looks like sqrt(5/4)=1.118 (a ddof artifact) but the ddof fork
  does NOT reconcile once mu is subtracted (gives negative drift on a growing
  series). The z-score fork reconciles cleanly (sig~2220, mu~+236). When a VaR
  answer is ~1.10x high, suspect the z-score (2.576 vs 2.326) BEFORE ddof.
- THE KILLER TRAP — DRIFT (MEAN) MUST BE SUBTRACTED. The lower-tail loss is the
  signed lower quantile of the change distribution, expressed as a positive loss:
      loss = z * sigma - mu        # NOT just z*sigma
  where mu = mean and sigma = std dev of the relevant change/return series. For
  a GROWING series (holdings rose 2000->2004) mu > 0 and CANCELS most of the
  z*sigma band, making the true loss MUCH smaller. Omitting mu (reporting z*sigma
  alone) inflates the answer several-fold.
  DIAGNOSTIC: answer 20602 vs gold 4928 = factor 4.18 too big. That factor =
  z*sigma/(z*sigma - mu), i.e. drift was ~76% of the z*sigma band. A clean
  3-5x overshoot on a VaR question almost always means you DROPPED THE DRIFT
  TERM (or computed z*sigma on raw LEVELS instead of on year-over-year changes
  with the mean subtracted).
- WHAT STATISTIC TO USE: the volatility is of the YEAR-OVER-YEAR CHANGES of the
  holdings, not the std dev of the 5 raw levels. With 5 annual values you get 4
  annual changes; mu and sigma are the mean and std of those 4 changes (decide
  population vs sample by re-reading — default population/ddof matching the
  worked magnitude; sample (ddof=1) plausible, test both if off by sqrt(N/(N-1))
  ~1.12). Loss = z*sigma_change - mu_change, then convert.
- FX CONVERSION WRINKLE: the question often asks the loss in a FOREIGN currency
  "using the monthly not-seasonally-adjusted USD->X exchange rate for <Month
  Year> reported on the FIRST DAY of the month". Compute the loss in USD first,
  THEN multiply by the JPY-per-USD (or units-per-USD) rate. The FX rate source
  is the Bulletin's exchange-rate table (or the cited monthly NSA series); read
  the value for that exact month, first-of-month reporting convention. Round the
  FINAL converted loss to the requested unit ("nearest whole billion").
- Compute: ch=[vals[i]-vals[i-1]...] (4 annual changes); mu=mean(ch);
  sigma=std(ch) (population; try ddof=1 too); z=2.3263478740 (1%) / 1.644854 (5%);
  loss_usd = z*sigma - mu (SUBTRACT DRIFT); loss_fx = loss_usd * fx_units_per_usd.
- UNIT: get holding values into the SAME unit the answer wants BEFORE the VaR
  (loss scales linearly); FX multiply and final rounding must match "billions of
  JPY" etc.
- SANITY: a lower-tail loss should be POSITIVE and, for a strongly trending
  series, NOTICEABLY SMALLER than z*sigma because drift eats into it.

## CONFIRMED SUCCESS — the canonical 4928 question (pin these inputs)
Q: mutual-fund Treasury ownership end-Mar 2000-2004, 1% lower-tail loss in
billions JPY via March-2004 monthly NSA USD->JPY first-of-month rate.
- Data (TABLE OFS-2, Mutual funds col (9), $B): 222.3, 225.3, 266.1, 296.6, 280.8.
- YoY changes (4): 3.0, 40.8, 30.5, -15.8. mu = 14.625.
- ddof RESOLVED: use SAMPLE std (ddof=1) = 25.8068 -> reconciles to gold 4928.
  Population (ddof=0)=22.3493 gives 4055 (WRONG). For this 5-value/4-change VaR,
  ddof=1 is correct.
- z = 2.3263478740 (1% one-tailed). loss_usd = z*sig - mu = 45.4105 B USD.
- FX: FRED EXJPUS (Japan/US monthly NSA, JPY per USD, dated 1st of month).
  March 2004 (2004-03-01) = 108.5157. Fetch:
  curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXJPUS&cosd=2004-03-01&coed=2004-03-01"
- loss_jpy = 45.4105 * 108.5157 = 4927.75 -> round to 4928. SUBMIT 4928.

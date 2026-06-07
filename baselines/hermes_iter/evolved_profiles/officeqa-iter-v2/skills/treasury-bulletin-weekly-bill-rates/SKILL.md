---
name: treasury-bulletin-weekly-bill-rates
description: Use when OfficeQA/Treasury Bulletin questions ask for weekly average discount rates on new Treasury bills (e.g., 91-day weekly bills) across calendar months or years. Gives source/table selection, date handling, geometric mean, and rounding pitfalls.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, treasury-bills, rates, geometric-mean]
    related_skills: [treasury-bulletin-table-digit-counting]
---

# Treasury Bulletin Treasury Bill Discount Rates

## Overview

Treasury Bulletin questions about Treasury bill issues often use the marketable securities / financing operations tables that report average bank discount rates by issue date or by tender opening date. The prompt may phrase the target as “weekly average discount rates,” “new 91-day weekly bills,” “Cash Management Treasury bills,” “tenders opened,” or “average bank discount rates.” Treat the quoted rates as percentage points as printed in the table during lookup; convert to decimal fractions only when the prompt explicitly asks for a decimal-value output (e.g. for log-rate variance).

## When to Use

Use this skill when the question asks for:

- Weekly average discount rates for new Treasury bills, especially 91-day weekly bills.
- Cash Management Treasury bills in the Financing Operations section, including short tenors such as 19-day or 2-day bills.
- Calendar-month subsets across one or more years (e.g., all September weeks in 1953-1955).
- Rows selected by issue date, report/Thursday date, or tender-opening date.
- A geometric mean, arithmetic mean, min/max, log difference, or realized variance/comparison across Treasury bill discount-rate observations.
- Rates “reported on Thursday,” issue dates that are weekly Thursdays, or tenders opened on named calendar dates.

Do not use this skill for savings bonds, capital movements, General Fund balances, ESF balance sheets, or expenditure tables unless Treasury bill discount rates are also involved.

## Source Pattern

1. Locate the Treasury Bulletin issue that contains the relevant bill-rate table for the year(s) in question. For older years, the table is commonly in the Public Debt / marketable securities section and lists Treasury bills by issue date with discount-rate columns. For 1980-era Cash Management bills, use the `Financing Operations` section/table, which can list bills by `tenders opened` date, maturity, days-to-maturity, amount, and `average bank discount rate`. In the June 1980 Bulletin, the relevant official Cash Management bill rows for May-June 1980 are in Financing Operations and should be matched by the printed `tenders opened` calendar date plus the short tenor/days-to-maturity (e.g. 19-day, 2-day), not by publication month alone.
2. Search within the extracted PDF text for terms such as:
   - `91-day`
   - `weekly bills`
   - `average discount rate`
   - `average bank discount rate`
   - `Cash Management`
   - `tenders opened`
   - `Financing Operations`
   - `new 91-day`
   - month names plus the year, e.g. `September 1954` or `May 27 1980`
3. In 1980-era `Financing Operations` tables, Cash Management bill rows can be keyed by very short maturities (e.g. 19-day, 2-day) and `tenders opened` calendar dates. Match both the requested tenor/days-to-maturity and the tender-open date before reading the `average bank discount rate` column; do not substitute high/low discount rates, investment rates, price, issue date, or maturity date.
4. Prefer layout-preserving extraction (`pdftotext -layout`) when columns are tight. Verify suspicious rows against the rendered page if OCR or text extraction collapses columns.

## Date Selection Rules

- Interpret “calendar month of September across 1953-1955” as all weekly issue/report rows whose printed Thursday date falls in September for each of those calendar years.
- For Cash Management bill questions, select rows by the prompt’s requested date field exactly. If it says `tenders opened on May 27, 1980`, use the `tenders opened` date, not issue date or maturity date.
- Include every Thursday in a requested weekly-bill month. Some months have four Thursdays and some have five; do not force a fixed count per year.
- Use the printed issue/report/opening date specified by the prompt, not the maturity date and not a fiscal-period heading.
- If the table has multiple bill tenors, select the requested tenor only (`new 91-day weekly bills`, `19-day Cash Management bills`, `2-day Cash Management bills`, etc.). Do not mix 91-day, 182-day, tax anticipation, special, cash management, or reopened issues unless explicitly requested.

## Arithmetic: Geometric Mean of Rates

For N printed rates `r_i` expressed as percentage points, compute:

```text
geometric_mean = (prod(r_i)) ** (1 / N)
```

Keep the rates in the same units as the prompt/table (usually percent). For example, rates around 1.5 are entered as `1.5`, not `0.015`, when the answer is expected as a Treasury Bulletin rate.

Recommended Python pattern:

```python
import math
rates = [/* printed weekly average discount rates as percentages */]
gm = math.exp(sum(math.log(r) for r in rates) / len(rates))
print(round(gm, 3))
```

Using logs avoids avoidable floating-point overflow/underflow and makes it easy to audit the count.

## Arithmetic: One-Step Realized Variance / Annualized Volatility of Log Rates

If a prompt asks for the realized variance of log average bank discount rates from two successive quoted observations, convert the printed percentage rates to decimal values first if the requested answer is in decimal-value units. For two observations `r1_pct`, `r2_pct`:

```python
import math
r1 = r1_pct / 100.0
r2 = r2_pct / 100.0
ret = math.log(r2) - math.log(r1)
rv = ret ** 2
print(round(rv, 3))
```

Do not inflation-adjust nominal bank discount rates unless explicitly instructed. With exactly two successive observations, “one step realized variance” means the single squared log return/log difference, not a sample variance with `n-1` denominator.

For Brownian-motion annualized realized volatility from dated Treasury-bill observations, use the realized variance estimator based on squared log returns, then annualize by the elapsed calendar time between the printed issue/tender dates unless the prompt explicitly specifies a different annualization factor. In OfficeQA Treasury Bulletin bill questions with two issue dates exactly one week apart, the gold convention is calendar-day Brownian scaling `365 / 7`, not hard-coded `52`; using `52` can shift a borderline answer by 0.01 percentage point (e.g. 6.15 vs 6.16).

```python
import math
from datetime import date
rates_pct = [/* printed rates, e.g. first Thursday and one week later */]
dates = [date(1960, 9, 1), date(1960, 9, 8)]  # use the actual printed issue/tender dates
rets = [math.log(rates_pct[i] / rates_pct[i-1]) for i in range(1, len(rates_pct))]
rv = sum(x*x for x in rets)
days = (dates[-1] - dates[0]).days
ann_factor = 365 / days   # for one 7-day interval, 52.142857..., not 52
ann_vol_decimal = math.sqrt(ann_factor * rv)
ann_vol_percent = ann_vol_decimal * 100
print(f"{ann_vol_percent:.2f}%")
```

If the prompt explicitly says to annualize using 52 weekly periods, use `52` instead of `365/days`; otherwise for Brownian-motion wording tied to actual issue dates, use the calendar-day elapsed-time factor. Because the log ratio is unitless, using printed percent rates directly inside `log(r2_pct/r1_pct)` gives the same return as converting both rates to decimals. For an answer requested as a percent value, multiply the annualized volatility decimal by 100 and round only the final displayed value to the nearest hundredth; do not truncate or round the log return, squared return, weekly RV, or annualized decimal first.

If the value is close to a .005 boundary, verify rounding with the exact printed rates and conventional half-up decimal rounding rather than by eyeballing or truncating an intermediate. Example pattern:

```python
from decimal import Decimal, ROUND_HALF_UP
answer = Decimal(str(ann_vol_percent)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print(f"{answer}%")
```

Older Bulletin tables can label the relevant field `average rate of discount` rather than `average bank discount rate`; this is the same printed nominal discount-rate percentage for the requested bill issue. Match the requested tenor/date first (e.g. 26-week bills by issue date) before applying the volatility formula.

## Common Pitfalls

1. **Using an arithmetic mean.** If the prompt says geometric mean, multiply/log-average the rate values; do not sum and divide.
2. **Decimal conversion error.** Treasury Bulletin discount rates are printed as percentages. If the table shows `1.558`, the answer in rate units is `1.558`, not `0.01558`; however, if the prompt explicitly says output a decimal value for a log-rate calculation, use `0.01558` inside the log calculation.
3. **Dropping a fifth Thursday.** Calendar months can contain five Thursday issue/report dates. Count dates, not rows per month by assumption.
4. **Mixing tenors.** The table may put 91-day, 182-day, Cash Management, and other bill types near each other. Select only the requested bill type/tenor/date rows.
5. **Using the wrong date column.** Cash Management bill prompts may specify `tenders opened`; do not substitute maturity date, issue date, or the bulletin publication date.
6. **Including non-month rows.** Do not include late-August or early-October rows just because they appear on the same page or under a monthly heading.
7. **Rounding too early.** Use the printed rates as exact source values, compute the full geometric mean/log variance, then round the final result to the requested precision (nearest thousandth for three decimals).
8. **Sample-variance formula for one-step realized variance.** For two successive rate observations, realized variance is the squared log change. Do not divide by `n-1` or subtract a sample mean.

## Verification Checklist

- [ ] Confirmed the table is for Treasury bill discount rates, not bond yields or savings bonds.
- [ ] Confirmed whether the relevant table is weekly bill rates or Financing Operations / Cash Management bills.
- [ ] Selected only the requested bill type and tenor (e.g., new 91-day weekly, 19-day Cash Management, 2-day Cash Management).
- [ ] Used the requested date field exactly: issue/report date for weekly bills, or `tenders opened` date for Cash Management bills when specified.
- [ ] Included all Thursday dates in the requested calendar month(s) and years when doing weekly-month aggregation.
- [ ] Audited the number of rates against the calendar or prompt-specific rows.
- [ ] Computed geometric mean or log realized variance from source rate units as required by the prompt.
- [ ] For log variance with decimal-value output, converted printed percent rates to decimals before applying `log`.
- [ ] Rounded only the final answer to the requested decimal place.

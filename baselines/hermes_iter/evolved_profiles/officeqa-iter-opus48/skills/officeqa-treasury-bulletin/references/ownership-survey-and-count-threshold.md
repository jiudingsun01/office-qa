# Ownership Survey, TABs, and "count categories over a threshold" questions

## The Treasury Ownership Survey table
The Bulletin's "Treasury Survey of Ownership" section breaks down holdings of
interest-bearing marketable public debt by INVESTOR CLASS. The recurring set of
investor categories (1960s era) is:
- U.S. Government accounts and Federal Reserve banks
- Commercial banks
- Mutual savings banks
- Insurance companies
- Savings and loan associations
- Corporations
- States and local governments
(plus "all other investors" / nonbank totals depending on the year)

The survey table is typically reported for MONTH-END dates and may carry several
security TYPES as columns/sub-tables: Treasury bills, Tax Anticipation Bills
(TABs), certificates, notes, bonds, etc. EACH security type has its own column of
holdings broken out by the investor categories above.

## DISTRACTOR TRAP: framing month/table != metric month/table
A question can frame the universe of categories using one snapshot
("...recorded on the end of January 1962 and end of January 1963...") and then ask
the actual numeric metric on a DIFFERENT month and a DIFFERENT security column
("...total Treasury TABs as recorded in March of each corresponding year...").
- The January framing only establishes WHICH 7 categories exist / are in scope.
- The number you actually read comes from the MARCH survey table, **TABs column**.
- Do NOT pull the bill/total/January numbers. Read the TABs (Tax Anticipation
  Bills) column for the March survey of each year.

## "How many categories had more than $X" = COUNT, then SUM across years
Question type: "how many total categories ... had more than 500 million dollars
... Report your final value as a sum of each category count for each year."
Procedure:
1. For year 1 (e.g. March 1962): in the TABs column, count how many of the named
   categories have a value > 500 (units are millions of $; threshold "500 million"
   = value > 500 in a millions-denominated table). Watch for blanks/dashes = 0.
2. For year 2 (March 1963): same count.
3. Final answer = count_year1 + count_year2 (a SUM of the two counts, a small
   integer like 3, not the dollar totals).
Answer is a bare integer, no brackets/units unless the question says otherwise.

## MATURITY-DISTRIBUTION TRAP: "total bills outstanding per month" != the by-maturity-month rows
TSO-3 ("Interest-Bearing Marketable Public Debt Securities by Issue") lists, under
"Treasury Bills: Regular weekly and annual maturing:", one row PER MATURITY MONTH
(Feb, Mar, Apr ... 12 forward months from the survey date). The "Total amount
outstanding" cell on each such row is the par value of bills **MATURING in that
month**, NOT the running stock of all bills outstanding as of that month.
- Signature of this table: values DECAY hard down the column — first ~6 months are
  large (20k-31k), then they collapse to ~3k. That decay is the tell that these are
  maturity buckets, not a stock time series.
- The TOTAL stock of Treasury bills outstanding is the "Total Treasury Bills" line
  (and the TSO-2 "Treasury bills" row) — e.g. Jan 31 1977 = 164,005; Jan 31 1978 =
  161,221 (millions, par). THAT is "total nominal outstanding of interest-bearing
  marketable U.S. Treasury bills."

When a question asks "how many calendar months from <A> to <B> had TOTAL nominal
outstanding of Treasury bills exceeding $X million" using 2 surveys (e.g. Jan 1977
+ Jan 1978), the intended metric is the TOTAL bills outstanding STOCK, which is
~160k+ and therefore exceeds any small threshold ($20,000M) in EVERY month each
survey covers. Each Survey of Ownership is a single month-end snapshot that stands
in for the 12 months it spans:
- Jan 1977 survey -> stands for Feb 1977..Jan 1978 (12 months, total stock 164,005 > 20,000).
- Jan 1978 survey -> stands for Feb 1978..Jan 1979 (12 months, total stock 161,221 > 20,000).
So a "Feb 1977..Jan 1979 inclusive" window resolves via the per-survey 12-month
spans; the gold answer was 12 (one survey's worth of months all clearing the
threshold), NOT a count derived from the decaying maturity rows. I WRONGLY read the
by-maturity-month "Total amount outstanding" cells and counted only the 7 months >
20,000 across both tables. The maturity rows are a distractor for a stock question.

RULE: "total ... outstanding" of a security type = the type's TOTAL / grand-total
line in TSO-2 or the "Total <type>" line in TSO-3, NOT individual issue/maturity
rows. Read by-issue / by-maturity-month rows ONLY when the question names a specific
issue, coupon, or maturity date.

## Pitfalls
- Threshold is on the per-category value, in the table's native unit (millions).
  "More than 500 million" with a millions table means strictly > 500.0.
- A category present in the Jan snapshot may be blank/zero in the March TABs
  column (TABs are sporadic, seasonal short-term instruments) -> does not count.
- Don't sum the dollar values; the answer is a count-of-counts (sum of two integer
  counts), which is why correct answers are tiny (0-14 range for 7 categories x 2
  years).

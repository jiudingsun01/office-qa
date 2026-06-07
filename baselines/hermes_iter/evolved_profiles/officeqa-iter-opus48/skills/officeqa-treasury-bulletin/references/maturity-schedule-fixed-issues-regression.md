# Maturity Schedule "Fixed maturity issues" + OLS regression (late-1940s bulletins)

## Trigger
Q gives 4 EARLY bulletins (1948_03, 1949_03, 1950_03, 1951_03) and asks for
"interest-bearing public marketable securities ... of FIXED MATURITY type" as of
the **Maturity Schedule** published "last day of January" of each year, then fit
OLS linear regression to project the next January (1952). Answer in BILLIONS,
rounded to tenths. GOLD = 39.5.

## ★★★ SOLVED — verified gold answer 39.5 ★★★
This exact question was attempted and FAILED 3 TIMES (answers 50.0, 50.0, 57.0)
by SUMMING the fixed column across the whole schedule. THAT IS WRONG.

CORRECT interpretation: use ONLY the FIRST / NEAREST maturity-year group's
"Total" in the Fixed-maturity-issues column — i.e. the total of fixed-maturity
securities maturing IN THAT BULLETIN'S OWN CALENDAR YEAR (the within-the-year
bucket = bills + certificates + short notes). One value per bulletin, NO summing
across out-year groups, NO Panama Canal bond, NO callable issues.

### Verified inputs (first-year-group "Total", Fixed column, MILLIONS)
- Jan 31 1948 (1948_03): 1948-group Total fixed = **46,615**
- Jan 31 1949 (1949_03): 1949-group Total fixed = **36,068**
- Jan 31 1950 (1950_03): 1950-group Total fixed = **44,467**
- Jan 31 1951 (1951_03): 1951-group Total fixed = **40,537**

### Regression
Convert to billions [46.615, 36.068, 44.467, 40.537], x=[1948,1949,1950,1951],
OLS, project x=1952 -> **39.463 -> 39.5**. ✓ MATCHES GOLD.
```python
def ols(ys,xs,xt):
    n=len(xs);xb=sum(xs)/n;yb=sum(ys)/n
    m=sum((xs[i]-xb)*(ys[i]-yb) for i in range(n))/sum((xs[i]-xb)**2 for i in range(n))
    return m*xt+(yb-m*xb)
ols([46.615,36.068,44.467,40.537],[1948,1949,1950,1951],1952)  # 39.463 -> 39.5
```

## WHY the first group, not the sum
"of fixed maturity type ... as of the maturity schedule published on the last day
of January of each calendar year" — the relevant figure is the fixed-maturity
total of securities scheduled to mature in that SAME year the schedule is dated
(the leading/top year-group block whose label == the bulletin's January year).
The schedule's first block is always the current calendar year. Read its "Total"
row, FIXED column only. Ignore all later year-group blocks.

## The table layout
"Table 1.- Maturity Schedule of Interest-Bearing Public Marketable Securities ...
Outstanding January 31, YYYY". In millions. 2-up layout (two halves per page).
Columns: Year/month | Description | **Fixed maturity issues** | Callable: First
call | Callable: Final maturity | Date bank restricted. Securities grouped by
maturity year; each group ends with a "Total" row. The FIRST group (= January
year of the bulletin) is at top-left of the page.

PDF page (these four bulletins): 1948_03 p.28, 1949_03 p.29 (printed 19),
1950_03 p.31 (printed 21), 1951_03 p.32 (printed 22).

## Reading method (parse is UNRELIABLE)
sonnet46 markdown column-scrambles this table and `pdftotext` is OCR garbage.
Render the page image and read with vision:
`pdftoppm -r 200 -png -f P -l P <pdf> /tmp/x`, then vision_analyze the first
year-group's "Total" row, Fixed-maturity-issues (leftmost numeric) column.

## Delimiter
Single decimal value -> "39.5" (MODE A: has a decimal point).

## Reference: the WRONG grand-total sums (do NOT use — kept as a warning)
Summing all year-group fixed Totals + the 3% Panama Canal 6/1/61 bond (=50) gives
1948=55,427 / 1949=48,044 / 1950=54,565 / 1951=57,479 -> projects 57.0. WRONG.
(Earlier I even mis-summed to 49,890/52,804 -> 50.0; also WRONG.) The grand-total
reading is NOT what "fixed maturity type" means here.

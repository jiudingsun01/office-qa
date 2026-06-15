---
name: treasury-bulletin-personal-saving-rates
description: Use when OfficeQA/Treasury Bulletin questions ask about U.S. personal saving rates, household saving as a percent of after-tax income, or related line charts. Maps the wording to the BEA/FRED PSAVERT series and gives a concrete chart-extraction workflow when the Bulletin has no table.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [officeqa, treasury-bulletin, personal-saving, charts, psavert]
    related_skills: []
---

# Treasury Bulletin Personal Saving Rates

## Overview

Treasury Bulletin questions can refer to “U.S. personal saving rates,” often defined parenthetically as “household saving as a percent of after-tax income.” This wording maps to the personal saving rate: personal/household saving as a percent of disposable (after-tax) personal income. In modern external data this is the BEA/FRED `PSAVERT` series.

In the September 1991 Treasury Bulletin, this appears as a chart titled “Personal Saving” near the hinted page rather than as a clean numeric table. `pdftotext -layout` may find the title but not the plotted values, so be ready to rasterize the page and read the line chart.

## When to Use

Use this skill when the question mentions any of:

- “personal saving rate” or “personal savings rate”
- “household saving as a percent of after-tax income”
- a year range over which the saving-rate line peaks/troughs
- a hinted Treasury Bulletin page containing a “Personal Saving” chart

Do not use it for savings bonds, Treasury securities, or General Fund cash balances; those are different Treasury Bulletin tables.

## Procedure

1. Start with the hinted page window:
   ```bash
   pdftotext -layout -f <hint-2> -l <hint+2> <pdf> -
   ```
   Search for `Personal Saving`, `household saving`, and `after-tax income`.

2. If text extraction only returns the title/labels, rasterize the hinted page:
   ```bash
   pdftoppm -r 200 -f <page> -l <page> <pdf> /tmp/tb_personal_saving
   ```
   Inspect the PNG/PPM directly or use image/OCR tools to locate:
   - chart title: `Personal Saving`
   - x-axis year labels (e.g. 1950, 1955, …, [redacted])
   - y-axis saving-rate scale
   - the highest/lowest point of the plotted line in the requested year range

3. For peak-year questions, use chart geometry rather than eyeballing if the line is close:
   - identify pixel centers for two or more printed year labels on the x-axis;
   - fit a linear mapping `pixel_x = a + b * year`;
   - locate the line’s highest point (smallest y pixel on a standard image coordinate system);
   - convert that x-coordinate back to a year and round to the nearest printed/data year.

4. Cross-check the interpretation, if network access is allowed, with FRED `PSAVERT`:
   ```python
   import csv, io, urllib.request
   url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=PSAVERT'
   text = urllib.request.urlopen(url, timeout=10).read().decode()
   rows = list(csv.DictReader(io.StringIO(text)))
   by_year = {}
   for r in rows:
       if r['PSAVERT'] == '.':
           continue
       year = int(r['observation_date'][:4])
       if START <= year <= END:
           by_year.setdefault(year, []).append(float(r['PSAVERT']))
   annual_avg = {y: sum(v)/len(v) for y, v in by_year.items()}
   print(max(annual_avg.items(), key=lambda kv: kv[1]))
   ```
   Treat this as a cross-check, not a replacement for reading the provided Treasury Bulletin PDF, unless the benchmark instructions explicitly allow outside data.

## Common Pitfalls

1. Do not confuse personal saving rates with savings bond sales/redemptions. “Household saving as a percent of after-tax income” is the personal saving rate, not a Treasury debt instrument.

2. `pdftotext` may not expose plotted chart data. A missing table in text extraction does not mean the data is absent; rasterize the hinted page.

3. The page number in the prompt can refer to a printed article page while the PDF page differs. Use the prompt’s source PDF hint first, then search a small window around it.

4. In raster images, the maximum value on a line chart corresponds to the smallest y pixel coordinate, because image coordinates increase downward.

5. If using FRED as a cross-check, align the frequency with the chart/question. For a broad year-range question asking “in which year,” use annual averages or the annual chart point, not a single monthly spike, unless the Treasury Bulletin chart is explicitly monthly.

## Verification Checklist

- [ ] Confirmed the PDF/page contains `Personal Saving` or equivalent wording.
- [ ] Confirmed the question’s definition matches personal saving as percent of after-tax/disposable income.
- [ ] Used the requested inclusive year range only.
- [ ] If extracting from a chart, mapped x-axis labels to years rather than guessing from page position.
- [ ] If cross-checking externally, used `PSAVERT` only as validation and kept the final answer grounded in the Treasury Bulletin prompt.

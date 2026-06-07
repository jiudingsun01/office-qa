---
name: treasury-bulletin-marketable-securities-offerings
description: Use for OfficeQA/Treasury Bulletin questions about marketable Treasury security offerings/auctions, bids, tenders, accepted amounts, cash vs noncash rollover tenders, foreign/international investor categories, issue/maturity dates, and notes/bonds/bills sold.
---

# Treasury Bulletin marketable security offering / tender tables

Use this skill when a question asks about bids or tenders for Treasury bills, notes, or bonds, especially phrases like `bids submitted`, `tenders accepted`, `cash tenders`, `noncash rollover tenders`, `foreign`, `international`, or a security identified by maturity date.

## Locate the right table

1. Work in the Treasury Bulletin issue covering the auction/issue period. These tables are usually in the Public Debt section, near titles such as:
   - `Offerings of Marketable Securities`
   - `Disposition of Marketable Securities`
   - `Public Debt Operations`
   - `Treasury Bills, Notes, and Bonds`
   - `Results of Treasury Market Financing`
2. Search by exact maturity date first, then by issue date/security type. A prompt like `2-year U.S. Treasury notes maturing at the end of July 1984` points to the row/security with maturity `July 31, 1984` (2-year note issued around July 31, 1982), not every security in July 1984.
3. Match security type and term exactly: `2-year notes` are separate from 4-year notes, bonds, and bills even if issue/maturity dates are nearby.
4. Use the table's printed unit. Late-20th-century offering tables are commonly in `millions of dollars`; if the prompt asks for total dollar value, multiply by 1,000,000 and round to the nearest nominal dollar.

## Read bids and tenders correctly

1. Distinguish `bids/tenders submitted` from `tenders accepted`; the first is total demand and the second is awarded amount.
2. If the question asks `total dollar value of bids submitted by investors`, use the `Total bids received/submitted` amount for the matched security, not the amount accepted.
3. `Noncash rollover tenders accepted` are normally a subset of accepted tenders, often listed separately from cash tenders. Do not add them to cash accepted unless the prompt asks for total accepted.
4. For foreign/global non-domestic investor wording, use the column/category for foreign and international accounts (often `Foreign official and international accounts`, `foreign and international`, or similar). Phrases like `submitted on behalf of global non-domestic investors` are benchmark paraphrases for the foreign/international account category; do not use domestic Federal Reserve/Treasury account columns as a proxy.

## Percent denominators

For prompts asking what percent of the bids submitted were a particular category of accepted tenders, follow the grammar literally:

- numerator: the requested accepted-tender subset (e.g. noncash rollover tenders accepted submitted on behalf of foreign/international investors);
- denominator: total bids submitted/received for that same security.

Example pattern from the 2-year note maturing July 31, 1984: total bids submitted were 10,102 million dollars and foreign/international noncash rollover tenders accepted were 478 million dollars, so the percent is `478 / 10102 * 100 = 4.73`, not `478 / total accepted`.

## Extraction tips

1. `pdftotext -layout` usually preserves these wide Public Debt tables better than raw text. If columns wrap, crop or inspect adjacent pages because securities-offering tables often span multiple pages.
2. When page text is crowded, search for the maturity date string (`July 31, 1984`) and nearby labels (`Total`, `noncash`, `foreign`) rather than searching only the security name.
3. Check table continuation headers: the category labels may appear on a previous page while the numeric row appears on the next page.

## Rounding and formatting

1. Convert printed millions to nominal dollars only at the final answer if requested.
2. Percent values should be computed from unrounded printed amounts and rounded only at the final step to the requested precision, usually nearest hundredth.
3. For bracketed comma-separated benchmark answers, do not include thousands separators inside numeric values unless explicitly requested; e.g. `[10102000000, 4.73]`.

## Verification checklist

Before answering, confirm:

1. exact security type/term matched;
2. exact maturity date matched;
3. amount used for `bids submitted` is not `accepted`;
4. noncash rollover and foreign/international category match the prompt;
5. percent denominator follows the prompt (often total bids submitted);
6. table units and final output units are converted correctly.

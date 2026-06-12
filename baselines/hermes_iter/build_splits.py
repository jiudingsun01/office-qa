#!/usr/bin/env python3
"""Split officeqa_pro.csv into train/eval/test (seed 42) and write JSONL
prompts for Hermes Agent. Each prompt points Hermes at the source corpus with
a page hint and demands a <FINAL_ANSWER> tag.

Two corpus options are supported:

  --corpus pdf            (default) Hermes reads the original Treasury Bulletin
                          PDFs via `pdftotext` / `pdftoppm`.
  --corpus parsed-md      Hermes reads pre-parsed Markdown (Sonnet-4.6 augmented
                          with chart/figure descriptions) from
                          data/final_parsed_db_augmented/.
  --corpus parsed-md+pdf  Both paths surfaced in the prompt; agent uses the
                          parsed Markdown by default and can fall back to the
                          PDF for verification or for content the parse missed.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
PDFS = DATA / "treasury_bulletin_pdfs"
PARSED_MD = DATA / "final_parsed_db_augmented"
DEFAULT_OUT = ROOT / "baselines" / "hermes_iter" / "splits"

SPLIT_SIZES = {"train": 80, "eval": 25, "test": 28}
SEED = 42

PDF_INSTRUCTIONS = """You are an analyst answering questions about U.S. Treasury Bulletins.

You will receive a question and the path to a Treasury Bulletin PDF (typically 100-200 pages of tables, charts, and narrative). The relevant content is on or near a hinted page. Extract the data you need and answer the question.

Environment available to you:
- `pdftotext -layout -f <start> -l <end> <pdf> -` extracts text from a specific page range. Try this FIRST; the bulletins have text layers.
- `pdftoppm -r 200 -f <start> -l <end> <pdf> /tmp/page` rasterizes pages as PNG, useful for tables/figures the text layer mangles.
- You can run shell commands (e.g. via `terminal`) and Python (`execute_code`).

Do NOT install packages. `poppler-utils` (pdftotext, pdftoppm) is already installed. If a command fails, try the other tool or a different page range — do not attempt apt/sudo.

Be economical: try `pdftotext` on a 3-5 page window around the hint first. Only fall back to rasterized image inspection if the text is mangled.

OUTPUT FORMAT (mandatory):
- End your reply with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question requires them.
- Match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not write "$" or "million").
- For a list of numbers, comma-separate them inside the tags."""

PARSED_MD_INSTRUCTIONS = """You are an analyst answering questions about U.S. Treasury Bulletins.

You will receive a question and the path to a pre-parsed Treasury Bulletin Markdown file (extracted text + Markdown tables + appended chart/figure descriptions). Each file typically runs 2,000-10,000 lines. The relevant content is on or near a hinted page in the original PDF.

Environment available to you:
- Use the `read_file` tool (or `terminal` with `sed -n '<start>,<end>p' <file>`) to inspect ranges of the markdown rather than loading the whole file.
- Tables are formatted as Markdown pipe tables. Numeric cells preserve the original column layout but may include footnote markers (e.g. `(r)`, `*`, `1/`) — strip these before arithmetic.
- Original PDF page boundaries are marked by lines like `-15-` (a hyphen-wrapped page number on its own line). These are best-effort and not always present; use `grep -n` to locate hinted topics by keyword as well.
- Charts, figures, and exhibits that were rasterized in the source PDF have plain-text descriptions appended near the end of the file under a `# Chart Descriptions` heading (organized by page).
- You can run shell commands (e.g. via `terminal`) such as `grep -nE`, `head`, `sed`, and Python (`execute_code`).

Be economical: `grep -n` for likely table titles or section headers (e.g. `grep -nE "Statutory Debt|Net interest|Table 1"`), then read a focused window. Only consult the chart descriptions section when the question involves a chart, plot, or figure.

OUTPUT FORMAT (mandatory):
- End your reply with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question requires them.
- Match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not write "$" or "million").
- For a list of numbers, comma-separate them inside the tags."""

PARSED_MD_PDF_INSTRUCTIONS = """You are an analyst answering questions about U.S. Treasury Bulletins.

You will receive a question and TWO paths per source document: a pre-parsed Treasury Bulletin Markdown file AND the original PDF. The Markdown is faster and easier to grep; the PDF is the authoritative source when the parse is ambiguous, when you need to inspect a chart/figure visually, or when columns or footnote markers may have been mangled.

PRIMARY tool (use first): the Markdown file.
- Use the `read_file` tool (or `terminal` with `sed -n '<start>,<end>p' <file>`) to inspect ranges.
- Tables are Markdown pipe tables; multi-level headers are flattened with `>` separators inside one header row. Numeric cells may include footnote markers (e.g. `(r)`, `*`, `1/`) — strip these before arithmetic.
- Original PDF page boundaries are marked by lines like `-15-`. These are best-effort; use `grep -n` for likely table titles too.
- Charts and figures are described in plain text at the end of the file under a `# Chart Descriptions` heading (organized by page).

FALLBACK tool (use when the parse is unreliable): the original PDF.
- `pdftotext -layout -f <start> -l <end> <pdf> -` extracts text from a page range. Useful when a Markdown table looks misaligned, a numeric cell is missing, or a column header didn't survive parsing.
- `pdftoppm -r 200 -f <start> -l <end> <pdf> /tmp/page` rasterizes pages as PNG, useful for charts/figures or when the text layer is mangled.
- Do NOT install packages. `poppler-utils` is already installed.

Be economical: try the Markdown FIRST with a focused `grep -n`, read a narrow window, and only open the PDF if a number looks suspicious or you need to confirm a column header / figure detail.

OUTPUT FORMAT (mandatory):
- End your reply with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question requires them.
- Match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not write "$" or "million").
- For a list of numbers, comma-separate them inside the tags."""


PDF_NOORACLE_INSTRUCTIONS = """You are an analyst answering questions about U.S. Treasury Bulletins.

You are given ONLY a question. You must FIND the relevant Treasury Bulletin issue(s) yourself from the full corpus, then extract the data and answer. You are NOT told which file or page to use.

Corpus:
- All Treasury Bulletin PDFs live in a single directory (path given below): U.S. Treasury Bulletins, monthly issues 1939-2025.
- Filename convention: `treasury_bulletin_{YEAR}_{MONTH_NUM}.pdf`, e.g. `treasury_bulletin_1953_07.pdf` for July 1953.
  Month mapping: january=01 february=02 march=03 april=04 may=05 june=06 july=07 august=08 september=09 october=10 november=11 december=12.
- Note: a given statistic is usually published in the issue for (or shortly after) the period it covers; annual/fiscal-year tables often appear in a later issue. You may need to reason about WHICH issue reports the figure, not just match a date.

Environment available to you:
- `ls <dir>` to see which issues exist; `pdftotext -layout -f <start> -l <end> <pdf> -` to read a page range; `pdftoppm -r 200 -f <s> -l <e> <pdf> /tmp/page` to rasterize.
- You can run shell commands (e.g. via `terminal`) and Python (`execute_code`).
- `poppler-utils` is installed. Do NOT install packages or use apt/sudo.

Approach: figure out which issue(s) the question needs, locate them in the corpus directory, find the right table/page, extract, and compute.

OUTPUT FORMAT (mandatory):
- End your reply with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question requires them.
- Match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not write "$" or "million").
- For a list of numbers, comma-separate them inside the tags."""


PARSED_MD_NOORACLE_INSTRUCTIONS = """You are an analyst answering questions about U.S. Treasury Bulletins.

You are given ONLY a question. You must FIND the relevant Treasury Bulletin issue(s) yourself from the full corpus of pre-parsed Markdown files, then extract the data and answer. You are NOT told which file or page to use.

Corpus:
- All bulletins are pre-parsed to Markdown in a single directory (path given below): extracted text + Markdown tables + appended chart/figure descriptions, monthly issues 1939-2025.
- Filename convention: `treasury_bulletin_{YEAR}_{MONTH_NUM}.sonnet46.md`, e.g. `treasury_bulletin_1953_07.sonnet46.md` for July 1953.
  Month mapping: january=01 february=02 march=03 april=04 may=05 june=06 july=07 august=08 september=09 october=10 november=11 december=12.
- Note: a statistic is usually published in the issue for (or shortly after) the period it covers; annual/fiscal-year tables often appear in a later issue. You may need to reason about WHICH issue reports the figure, not just match a date.

Environment available to you (these files are PLAIN TEXT — grep is instant, no PDF parsing needed):
- `grep -rn "<table title or keyword>" <dir>` to find which issue/line has the data across the whole corpus at once; `grep -l` to list matching files.
- `read_file` (or `sed -n '<a>,<b>p' <file>`) to read a focused line range once you've located it.
- Tables are Markdown pipe tables; multi-level headers are flattened with `>` separators. Numeric cells may include footnote markers (`(r)`, `*`, `1/`) — strip before arithmetic. Charts/figures are described under a trailing `# Chart Descriptions` heading.
- You can run shell commands (`terminal`) and Python (`execute_code`). Do NOT install packages.

Be economical: a single `grep -rn` over the corpus directory usually locates the right issue(s) and line(s) immediately — prefer that over opening files one by one. Then read a narrow window and compute.

OUTPUT FORMAT (mandatory):
- End your reply with the final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER> tags.
- Inside the tags, output only the value: a number, a date, a short phrase. No commentary, no units unless the question requires them.
- Match the scale implied by the question (e.g. "in millions of dollars" -> just the number in millions; do not write "$" or "million").
- For a list of numbers, comma-separate them inside the tags."""


def page_from_url(url: str) -> str:
    m = re.search(r"[?&]page=(\d+)", url)
    return m.group(1) if m else ""


def _corpus_paths(corpus: str, source_file: str) -> list[Path]:
    """Return one or more on-disk paths for a CSV source_file entry, depending
    on the selected corpus mode."""
    stem = source_file.replace(".txt", "").replace(".pdf", "")
    if corpus == "pdf":
        return [PDFS / f"{stem}.pdf"]
    if corpus == "parsed-md":
        return [PARSED_MD / f"{stem}.sonnet46.md"]
    if corpus == "parsed-md+pdf":
        return [PARSED_MD / f"{stem}.sonnet46.md", PDFS / f"{stem}.pdf"]
    raise ValueError(f"unknown corpus: {corpus}")


def make_prompt(row: dict, corpus: str, no_oracle: bool = False) -> str:
    if no_oracle:
        # Retrieval setting: hand the agent only the corpus directory, not the
        # gold source file(s) or page hint.
        if corpus == "pdf":
            return (
                f"{PDF_NOORACLE_INSTRUCTIONS}\n\n"
                f"Question: {row['question']}\n\n"
                f"Treasury Bulletin corpus directory: {PDFS}\n\n"
                f"Identify the relevant issue(s) and page(s) yourself, read them, then "
                f"provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."
            )
        if corpus == "parsed-md":
            return (
                f"{PARSED_MD_NOORACLE_INSTRUCTIONS}\n\n"
                f"Question: {row['question']}\n\n"
                f"Treasury Bulletin corpus directory: {PARSED_MD}\n\n"
                f"Identify the relevant issue(s) and section(s) yourself (grep the corpus), "
                f"read them, then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."
            )
        raise ValueError("--no-oracle supports --corpus pdf or parsed-md")

    files = [s.strip() for s in row["source_files"].splitlines() if s.strip()]
    docs = [s.strip() for s in row["source_docs"].splitlines() if s.strip()]
    lines = []
    for i, fn in enumerate(files):
        paths = _corpus_paths(corpus, fn)
        hint = page_from_url(docs[i]) if i < len(docs) else ""
        hint_str = f"  (hint: relevant content is near page {hint})" if hint else ""
        if len(paths) == 1:
            lines.append(f"- {paths[0]}{hint_str}")
        else:
            lines.append(f"- markdown: {paths[0]}{hint_str}")
            lines.append(f"  pdf:      {paths[1]}")
    files_block = "\n".join(lines)

    if corpus == "pdf":
        header = PDF_INSTRUCTIONS
        source_label = "Source PDFs"
        tail = "Read the relevant pages, then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."
    elif corpus == "parsed-md":
        header = PARSED_MD_INSTRUCTIONS
        source_label = "Source Markdown files"
        tail = "Read the relevant section(s), then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."
    elif corpus == "parsed-md+pdf":
        header = PARSED_MD_PDF_INSTRUCTIONS
        source_label = "Source documents (markdown + PDF per bulletin)"
        tail = "Read the relevant section(s) — Markdown first, PDF as fallback — then provide your final answer wrapped in <FINAL_ANSWER>...</FINAL_ANSWER>."
    else:
        raise ValueError(f"unknown corpus: {corpus}")

    return (
        f"{header}\n\n"
        f"Question: {row['question']}\n\n"
        f"{source_label}:\n{files_block}\n\n"
        f"{tail}"
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", choices=["pdf", "parsed-md", "parsed-md+pdf"], default="pdf",
                   help="which corpus to point Hermes at when building prompts")
    p.add_argument("--no-oracle", action="store_true",
                   help="retrieval setting: omit gold source file + page hint; agent must "
                        "find the right bulletin(s) itself (pdf corpus only)")
    p.add_argument("--out-dir", default="",
                   help="splits output directory (default: splits/ for pdf, splits_<corpus>/ otherwise)")
    args = p.parse_args()

    if args.out_dir:
        out_dir = Path(args.out_dir)
    elif args.corpus == "pdf" and not args.no_oracle:
        out_dir = DEFAULT_OUT
    else:
        slug = args.corpus.replace("-", "_").replace("+", "_plus_")
        if args.no_oracle:
            slug += "_nooracle"
        out_dir = DEFAULT_OUT.parent / f"splits_{slug}"

    # Validate the corpus roots exist so we fail fast.
    needs_md = args.corpus in ("parsed-md", "parsed-md+pdf")
    if needs_md and not PARSED_MD.exists():
        raise SystemExit(
            f"corpus dir not found: {PARSED_MD}\n"
            f"extract final_parsed_db_augmented.tar.gz into data/ first."
        )

    rows = list(csv.DictReader(open(DATA / "officeqa_pro.csv")))
    assert len(rows) == sum(SPLIT_SIZES.values()), f"size mismatch: {len(rows)} vs {sum(SPLIT_SIZES.values())}"

    rng = random.Random(SEED)
    rng.shuffle(rows)

    splits = {}
    i = 0
    for name, n in SPLIT_SIZES.items():
        splits[name] = rows[i : i + n]
        i += n

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"corpus: {args.corpus}  out_dir: {out_dir}")
    for name, rs in splits.items():
        out_path = out_dir / f"{name}.jsonl"
        with open(out_path, "w") as f:
            for r in rs:
                rec = {
                    "uid": r["uid"],
                    "prompt": make_prompt(r, args.corpus, no_oracle=args.no_oracle),
                    "gold_answer": r["answer"],
                    "question": r["question"],
                    "source_files": [s.strip() for s in r["source_files"].splitlines() if s.strip()],
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"  {name}: {len(rs)} -> {out_path}")

    # Also write a manifest with uid->split for scoring
    manifest = {
        "seed": SEED,
        "corpus": args.corpus,
        "splits": {name: [r["uid"] for r in rs] for name, rs in splits.items()},
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  manifest -> {out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic, verifiable gold-answer scrubber for skill libraries.

Removes gated answer-key leakage while preserving the METHOD prose:
  pass 1 — redact every verbatim non-trivial gold-answer string from the key
           (longest-first, token-boundaried so we don't bite into larger numbers);
  pass 2 — on lines that carry a memorization marker (Verified / accepted answer /
           gold answer / correct answer / the answer is), redact numeric & list
           tokens too (catches answers reprinted in a slightly different format).
The "[redacted]" placeholders stay in place, so the evidence that a skill memorized
*somewhere* remains visible (good for the research record) but the value is gone.

Run, then re-audit: verbatim gold matches should drop to ~0 by construction.
"""
from __future__ import annotations
import argparse, glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KEY = ROOT / "baselines" / "hermes_iter" / "splits_parsed_md_nooracle" / "full.jsonl"

MARKER = re.compile(r"verified|accepted answer|gold answer|correct answer|the answer is|expected answer", re.I)
# numeric / percent / bracketed-list tokens
NUMTOK = re.compile(r"\[[-\d.,\s]+\]|-?\d[\d,]*\.\d+%?|-?\d[\d,]{2,}%?|-?\d+\.\d+%?")


def load_golds() -> list[str]:
    golds = set()
    for l in open(KEY):
        g = str(json.loads(l)["gold_answer"]).strip()
        if len(g) >= 4 and not re.fullmatch(r"-?\d{1,3}", g):
            golds.add(g)
    # longest first so a short value can't redact inside a longer one
    return sorted(golds, key=len, reverse=True)


def scrub_text(text: str, golds: list[str]) -> tuple[str, int]:
    n = 0
    # pass 1: verbatim gold values, token-boundaried
    for v in golds:
        pat = re.compile(r"(?<![\w.])" + re.escape(v) + r"(?![\w.])")
        text, k = pat.subn("[redacted]", text)
        n += k
    # pass 2: numbers on memorization-marker lines
    out = []
    for ln in text.splitlines():
        if MARKER.search(ln):
            ln, k = NUMTOK.subn("[redacted]", ln)
            n += k
        out.append(ln)
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+", help="skill directories to scrub in place")
    args = ap.parse_args()
    golds = load_golds()
    print(f"{len(golds)} non-trivial gold answers loaded from key", flush=True)
    total_files = total_red = 0
    for d in args.dirs:
        files = glob.glob(str(Path(d) / "**" / "*.md"), recursive=True)
        dred = dfiles = 0
        for f in files:
            txt = Path(f).read_text(errors="replace")
            new, n = scrub_text(txt, golds)
            if n:
                Path(f).write_text(new)
                dred += n; dfiles += 1
        print(f"  {d}: {dfiles}/{len(files)} files scrubbed, {dred} redactions", flush=True)
        total_files += dfiles; total_red += dred
    print(f"TOTAL: {total_files} files changed, {total_red} redactions", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

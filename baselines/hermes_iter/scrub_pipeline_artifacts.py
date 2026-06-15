#!/usr/bin/env python3
"""Scrub gated gold-answer leakage from pipeline RUN artifacts before pushing.

Type-aware so each file stays usable:
  *.json (preds)         -> drop the "gold" key entirely; redact verbatim gold
                            values inside string fields (predicted/result/code/...);
                            stays valid JSON.
  *.txt/*.log/*.md       -> full scrub (verbatim gold + numbers on memorization
                            lines) — these are prose digests / logs / diagnoses.
  *.py (code/candidates) -> verbatim-gold redaction ONLY (keeps the code intact;
                            never touches legitimate numeric literals).
Skips *.pyc and binaries. Re-audit afterwards: standalone gold tokens -> ~0.
"""
from __future__ import annotations
import glob, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scrub_gold_values import load_golds, scrub_text  # full prose scrub  # noqa: E402


def redact_verbatim(text: str, golds: list[str]) -> tuple[str, int]:
    n = 0
    for v in golds:
        text, k = re.subn(r"(?<![\w.])" + re.escape(v) + r"(?![\w.])", "[redacted]", text)
        n += k
    return text, n


def scrub_json_obj(o, golds):
    if isinstance(o, dict):
        return {k: ("[redacted]" if k == "gold" else scrub_json_obj(v, golds)) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub_json_obj(x, golds) for x in o]
    if isinstance(o, str):
        return redact_verbatim(o, golds)[0]
    return o


def main() -> int:
    dirs = sys.argv[1:]
    golds = load_golds()
    print(f"{len(golds)} gold answers loaded", flush=True)
    nf = 0
    for d in dirs:
        for f in glob.glob(str(Path(d) / "**" / "*"), recursive=True):
            p = Path(f)
            if not p.is_file():
                continue
            try:
                if p.suffix == ".json":
                    obj = json.loads(p.read_text(errors="replace"))
                    p.write_text(json.dumps(scrub_json_obj(obj, golds), ensure_ascii=False))
                    nf += 1
                elif p.suffix in (".txt", ".log", ".md"):
                    new, k = scrub_text(p.read_text(errors="replace"), golds)
                    if k:
                        p.write_text(new); nf += 1
                elif p.suffix == ".py":
                    new, k = redact_verbatim(p.read_text(errors="replace"), golds)
                    if k:
                        p.write_text(new); nf += 1
            except Exception as e:
                print(f"  skip {f}: {e}", flush=True)
    print(f"scrubbed {nf} files", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

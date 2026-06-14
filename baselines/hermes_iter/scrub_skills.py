#!/usr/bin/env python3
"""Scrub memorized benchmark answers out of curated SKILL.md files, keeping method.

Opus text-rewrite (Anthropic API) per skill: removes 'Verified' worked-example blocks,
'(accepted)'/'WRONG' answer values, lists of specific table-cell values quoted as
answers, and concrete answer strings — while keeping the frontmatter, formulas,
table-location / publication-lag knowledge, unit/rounding conventions, retrieval
tactics, and general pitfalls. Writes scrubbed copies to --out.
"""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SYS = (
    "You are cleaning a procedural 'skill' file (SKILL.md) used by an AI agent on the "
    "OfficeQA Treasury-Bulletin benchmark. Your job: REMOVE memorized benchmark answers "
    "while KEEPING generalizable method.\n\n"
    "REMOVE:\n"
    "- every 'Verified example/failure/value' block or sentence;\n"
    "- any sentence quoting a specific COMPUTED answer as '(accepted)', 'WRONG', "
    "'the accepted answer', or similar;\n"
    "- any list of specific table-cell values presented as answers to particular "
    "questions (e.g. 'Jun 2000: 15,512,432/38,750,276; Jun 2001: ...');\n"
    "- any concrete benchmark answer string (e.g. '[2.81,0.030,8.706]', '-550.3', "
    "'intercept -184.143').\n\n"
    "KEEP exactly as-is:\n"
    "- the YAML frontmatter (--- name: ... description: ... ---);\n"
    "- formulas and definitions (e.g. BC(x)=(x^0.75-1)/0.75, CAGR=r^(1/n)-1);\n"
    "- where data lives / publication-lag / column-matching rules;\n"
    "- unit, scaling, and rounding conventions;\n"
    "- retrieval, disambiguation, and self-check tactics; general pitfalls.\n"
    "A NEUTRAL illustrative number is fine ONLY if it's a generic teaching example "
    "(a formula instance or a well-known constant), never a benchmark answer.\n\n"
    "Rewrite the file so it reads naturally without the removed parts (fix any dangling "
    "'Verified:' lead-ins). Output ONLY the rewritten SKILL.md, starting with '---'. "
    "No commentary, no code fences."
)


def call(content: str, key: str, model: str) -> str:
    body = json.dumps({
        "model": model, "max_tokens": 8000,
        "system": SYS,
        "messages": [{"role": "user", "content": f"Here is the SKILL.md to scrub:\n\n{content}"}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    txt = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
    # strip accidental fences / preamble before the frontmatter
    txt = re.sub(r"^```[a-z]*\n?", "", txt.strip())
    txt = re.sub(r"\n?```$", "", txt.strip())
    i = txt.find("---")
    return txt[i:].strip() + "\n" if i != -1 else txt.strip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skills-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="claude-opus-4-8")
    p.add_argument("--concurrency", type=int, default=4)
    args = p.parse_args()
    key = os.environ["ANTHROPIC_API_KEY"]
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    skills = sorted(Path(args.skills_dir).glob("*/SKILL.md"))
    print(f"scrubbing {len(skills)} skills -> {out}")

    def one(f: Path):
        name = f.parent.name
        try:
            scrubbed = call(f.read_text(), key, args.model)
        except Exception as e:
            return name, f"ERROR: {e}", 0
        (out / name).mkdir(parents=True, exist_ok=True)
        (out / name / "SKILL.md").write_text(scrubbed, encoding="utf-8")
        before = len(re.findall(r"[0-9]{4,}", f.read_text()))
        after = len(re.findall(r"[0-9]{4,}", scrubbed))
        return name, f"{before}->{after} nums", after

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for fut in as_completed([ex.submit(one, f) for f in skills]):
            name, status, _ = fut.result()
            print(f"  {name:34} {status}", flush=True)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""A FIXED agentic pipeline for OfficeQA (no-oracle parsed-md), vs the free agent.

Code-orchestrated discrete stages (Opus 4.8 via API + deterministic glue):
  1. LOCATE  (LLM->JSON): which bulletin issue file(s) + search keywords/table titles.
  2. RETRIEVE (code): grep the named files (+ month-adjacent fallbacks, then global)
     for the keywords; return focused line windows.
  3. SOLVE   (LLM->python): read the windows, extract the needed values, and emit a
     python program that computes and prints the answer (may inline known CPI/FX constants).
  4. RUN     (code): execute the python in a sandboxed subprocess (timeout, no net/fs-write).
  5. FORMAT  (LLM): turn the computed result into the exact <FINAL_ANSWER> string.

Scored with reward.py. Concurrent over the split.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def _find_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / "baselines" / "reward.py").exists():
            return d
    return start.parent.parent.parent

ROOT = Path(os.environ.get("OFFICEQA_ROOT") or _find_root(Path(__file__).resolve()))
sys.path.insert(0, str(ROOT / "baselines"))
from reward import extract_final_answer, score_answer  # noqa: E402

CORPUS = Path(os.environ.get("OFFICEQA_CORPUS") or (ROOT / "data" / "final_parsed_db_augmented"))
API = "https://api.anthropic.com/v1/messages"
KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-opus-4-8"
_MONTHS = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,
           "august":8,"september":9,"october":10,"november":11,"december":12}


def llm(system: str, user: str, max_tokens: int = 4000) -> str:
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        except Exception:
            if attempt == 3:
                return ""
            import time; time.sleep(15 * (attempt + 1))
    return ""


# ---------- Stage 1: LOCATE ----------
LOCATE_SYS = """You route an OfficeQA question to U.S. Treasury Bulletin issues. The corpus has one Markdown file per monthly issue named treasury_bulletin_{YEAR}_{MM}.sonnet46.md (1939-2025). A statistic usually appears in the issue covering its period or, for annual/fiscal-year or end-of-period tables, in a LATER issue (often 2-3 months after the period close; e.g. a "December 31, 1959" survey is often in the following March issue, a full prior-calendar-year table in a Jan-Mar issue of the next year).

Output ONLY a JSON object: {"files": ["treasury_bulletin_YYYY_MM", ...], "keywords": ["exact table title or distinctive row/section name", ...]}. List 1-4 candidate files (most likely first, include the publish-later candidate) and 3-8 specific grep keywords (table titles, section headers, row labels — not generic words)."""


def stage_locate(q: str, feedback: str = "") -> tuple[list[str], list[str]]:
    user = f"Question: {q}"
    if feedback:
        user += (f"\n\nA PREVIOUS attempt failed: {feedback}\nPropose DIFFERENT candidate files "
                 f"(try earlier/later issue months) and/or different table titles/keywords.")
    out = llm(LOCATE_SYS, user, 1000)
    m = re.search(r"\{.*\}", out, re.DOTALL)
    if not m:
        return [], []
    try:
        d = json.loads(m.group(0))
        files = [re.sub(r"\.(txt|pdf|sonnet46\.md|md)$", "", f) for f in d.get("files", [])]
        return files[:4], [k for k in d.get("keywords", []) if k][:8]
    except Exception:
        return [], []


# ---------- Stage 2: RETRIEVE (deterministic grep) ----------
def _adjacent(stem: str) -> list[str]:
    m = re.match(r"treasury_bulletin_(\d{4})_(\d{2})", stem)
    if not m:
        return [stem]
    y, mo = int(m.group(1)), int(m.group(2))
    out = []
    for dm in (0, 1, 2, 3, -1):  # the issue + publish-later candidates
        ny, nmo = y, mo + dm
        while nmo > 12: nmo -= 12; ny += 1
        while nmo < 1: nmo += 12; ny -= 1
        out.append(f"treasury_bulletin_{ny}_{nmo:02d}")
    return list(dict.fromkeys(out))


def stage_retrieve(files: list[str], keywords: list[str], q: str, cap: int = 22000) -> str:
    # also seed file candidates from any explicit date in the question
    if not files:
        for mo, n in _MONTHS.items():
            for y in re.findall(rf"{mo}\s+(\d{{4}})", q.lower()):
                files.append(f"treasury_bulletin_{y}_{n:02d}")
    cands = []
    for f in files:
        cands += _adjacent(f)
    cands = list(dict.fromkeys(cands))[:10]
    pats = [re.escape(k) for k in keywords] or [re.escape(w) for w in re.findall(r"[A-Z][a-zA-Z]{4,}", q)[:6]]
    blocks = []
    for stem in cands:
        path = CORPUS / f"{stem}.sonnet46.md"
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = sorted({i for i, ln in enumerate(lines)
                       for p in pats if re.search(p, ln, re.IGNORECASE)})
        if not hits:
            continue
        # merge hit lines into windows
        wins, cur = [], [hits[0]]
        for h in hits[1:]:
            if h - cur[-1] <= 60: cur.append(h)
            else: wins.append(cur); cur = [h]
        wins.append(cur)
        for w in wins[:4]:
            lo, hi = max(0, w[0] - 40), min(len(lines), w[-1] + 100)
            blocks.append(f"=== {stem}  (lines {lo}-{hi}) ===\n" + "\n".join(lines[lo:hi]))
    return ("\n\n".join(blocks))[:cap] or "(no matching excerpts found)"


# ---------- Stage 3: SOLVE (emit python) ----------
SOLVE_SYS = """You answer an OfficeQA Treasury-Bulletin question from the provided excerpts. Steps:
1. Identify the exact table, row, and dated column. Prefer the most FINAL/REVISED figures ((r) = revised, usually preferred). Mind units (thousands vs millions vs billions), calendar vs fiscal year, gross vs net, total vs subtotal. Strip footnote markers before using numbers.
2. Write a single self-contained python3 program that hard-codes the extracted values, performs the computation, and PRINTS the final numeric/text answer (and only that on the last line). For external constants the excerpts do not contain (e.g. BLS CPI-U index values, FX rates), inline your best-known values as variables with a comment.
Output the program in one ```python ... ``` block. No prose outside the code block."""

_BAD = re.compile(r"\b(os\.system|subprocess|shutil|rmtree|socket|requests|urllib|open\s*\([^)]*['\"][wa])", re.I)


def stage_solve(q: str, windows: str, feedback: str = "") -> str:
    user = f"Question: {q}\n\nExcerpts:\n{windows}"
    if feedback:
        user += (f"\n\nA PREVIOUS attempt was judged INCORRECT: {feedback}\nDiagnose and FIX this "
                 f"specific issue — re-read the excerpts; re-check the table/row/dated column, units, and arithmetic.")
    out = llm(SOLVE_SYS, user, 4000)
    m = re.search(r"```(?:python)?\s*(.*?)```", out, re.DOTALL)
    return m.group(1).strip() if m else out.strip()


# ---------- Stage 4b: VERIFY ----------
VERIFY_SYS = """You verify a candidate answer to an OfficeQA Treasury-Bulletin question. Given the question, the source excerpts, the python program used, and its printed result, check RIGOROUSLY:
(a) was the correct table, row, and dated column used?
(b) correct units/scale (thousands vs millions vs billions) and calendar vs fiscal year, gross vs net, total vs subtotal?
(c) are the extracted source values ACTUALLY present in the excerpts (re-read and confirm each one)?
(d) is the arithmetic correct, and does the result match the scale/precision the question asks for?
Output ONLY JSON: {"ok": true|false, "issue": "<if not ok: the specific error to fix; else empty>"}. Be strict — if any value can't be confirmed in the excerpts, or a unit/column/year looks wrong, set ok=false with a concrete issue."""


def stage_verify(q: str, windows: str, code: str, result: str) -> tuple[bool, str]:
    out = llm(VERIFY_SYS, f"Question: {q}\n\nExcerpts:\n{windows}\n\nProgram:\n{code}\n\nPrinted result: {result}", 900)
    m = re.search(r"\{.*\}", out, re.DOTALL)
    if not m:
        return True, ""  # un-parseable verdict -> don't block
    try:
        d = json.loads(m.group(0))
        return bool(d.get("ok", True)), str(d.get("issue", ""))
    except Exception:
        return True, ""


def stage_run(code: str) -> str:
    if not code or _BAD.search(code):
        return ""
    try:
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                           timeout=30, cwd="/tmp", env={"PATH": "/usr/bin:/bin"})
        out = (p.stdout or "").strip()
        return out.splitlines()[-1].strip() if out else ""
    except Exception:
        return ""


# ---------- Stage 5: FORMAT ----------
FORMAT_SYS = """You produce the FINAL answer string for an OfficeQA question, which is graded by EXACT string match. Given the question and a computed result, output ONLY <FINAL_ANSWER>...</FINAL_ANSWER>. Inside: only the value at the scale asked; no units/'$' unless required; round to exactly the requested decimal places (keep trailing zeros); for a list use the exact bracket/separator format the question prescribes (commas with NO space unless the question shows otherwise); thousands separators only if the question's own figures use them."""


def stage_format(q: str, result: str) -> str:
    out = llm(FORMAT_SYS, f"Question: {q}\n\nComputed result: {result}", 600)
    try:
        return extract_final_answer(out)
    except Exception:
        return result


def pipeline(rec: dict, max_outer: int = 2, max_solve: int = 2) -> dict:
    """Fixed stages with a bounded verify->retry loop: re-LOCATE on retrieval failure,
    re-SOLVE on a failed VERIFY, threading the diagnosed issue back as feedback."""
    q = rec["question"]
    feedback, result, code, windows, files, kws = "", "", "", "", [], []
    attempts = []
    solved = False
    for outer in range(max_outer):
        files, kws = stage_locate(q, feedback)
        windows = stage_retrieve(list(files), kws, q)
        if windows.startswith("(no matching"):
            feedback = (f"No excerpts matched keywords {kws} in files {files}. The data is likely in a "
                        f"different issue month (often a LATER issue) or under a different table title.")
            attempts.append({"outer": outer, "retrieval": "empty", "files": files, "keywords": kws})
            continue
        for inner in range(max_solve):
            code = stage_solve(q, windows, feedback if (outer or inner) else "")
            result = stage_run(code)
            if not result:
                feedback = "The program printed no final answer; ensure it prints the computed answer."
                attempts.append({"outer": outer, "inner": inner, "run": "empty"})
                continue
            ok, issue = stage_verify(q, windows, code, result)
            attempts.append({"outer": outer, "inner": inner, "result": result,
                             "verify_ok": ok, "issue": issue[:200]})
            if ok:
                solved = True
                break
            feedback = issue or "the answer was judged incorrect; re-extract and recompute"
        if solved:
            break
    pred = stage_format(q, result) if result else ""
    try:
        sc = score_answer(rec["gold_answer"], pred) if pred else 0.0
    except Exception:
        sc = 0.0
    return {"uid": rec["uid"], "predicted": pred, "score": sc, "result": result,
            "files": files, "keywords": kws, "code": code, "gold": rec["gold_answer"],
            "attempts": attempts, "n_attempts": len(attempts)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--split", default="baselines/hermes_iter/splits_parsed_md_nooracle/test.jsonl")
    p.add_argument("--run-dir", default="baselines/hermes_iter/runs/fixed_pipeline_test")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--concurrency", type=int, default=4)
    args = p.parse_args()
    rows = [json.loads(l) for l in open(args.split) if l.strip()]
    if args.limit > 0: rows = rows[:args.limit]
    run = Path(args.run_dir); (run / "preds").mkdir(parents=True, exist_ok=True)
    print(f"fixed pipeline: {len(rows)} questions  model={MODEL}", flush=True)
    res = {}
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(pipeline, r): r["uid"] for r in rows}
        done = 0
        for fut in as_completed(futs):
            d = fut.result(); res[d["uid"]] = d; done += 1
            (run / "preds" / f"{d['uid']}.json").write_text(json.dumps(d, ensure_ascii=False))
            print(f"[{done}/{len(rows)}] {d['uid']}  pred={d['predicted']!r} score={d['score']}", flush=True)
    n_corr = sum(1 for d in res.values() if d["score"] >= 1.0)
    summ = {"n_total": len(res), "n_correct": n_corr, "accuracy": n_corr / len(res) if res else 0.0}
    (run / "summary.json").write_text(json.dumps(summ, indent=2))
    print(f"\nDONE  {n_corr}/{len(res)} = {summ['accuracy']:.3f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Agentic pipeline for OfficeQA (no-oracle parsed-md).

Key change vs prior version: retrieval no longer relies on tiny keyword windows
(which truncated tables and caused mass abstention). Instead we:
  1. LOCATE  candidate issue files + keywords.
  2. RETRIEVE large, contiguous section blocks around keyword hits (whole tables
     incl. continuations), and if the file is small enough, pass it nearly whole.
     If keywords miss, fall back to passing the full candidate files (capped).
  3. SOLVE   (LLM->python) over the rich context; explicitly forbid abstention.
  4. RUN     sandboxed.
  5. VERIFY / retry, then FORMAT.
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
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.loads(r.read())
            return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        except Exception:
            if attempt == 3:
                return ""
            import time; time.sleep(15 * (attempt + 1))
    return ""


# ---------- Stage 1: LOCATE ----------
LOCATE_SYS = """You route an OfficeQA question to U.S. Treasury Bulletin issues. The corpus has one Markdown file per monthly issue named treasury_bulletin_{YEAR}_{MM}.sonnet46.md (1939-2025). A statistic usually appears in the issue covering its period or, for annual/fiscal-year or end-of-period tables, in a LATER issue (often 2-3 months after the period close; e.g. a "December 31, 1959" survey is often in the following March issue; a full prior-calendar-year table in a Jan-Mar issue of the next year).

Output ONLY a JSON object: {"files": ["treasury_bulletin_YYYY_MM", ...], "keywords": ["exact table title or distinctive row/section name", ...]}. List 1-5 candidate files (most likely first, include publish-later candidates) and 3-10 specific grep keywords (table titles, section headers, row labels — not generic words)."""


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
        return files[:5], [k for k in d.get("keywords", []) if k][:10]
    except Exception:
        return [], []


# ---------- Stage 2: RETRIEVE (large contiguous blocks) ----------
def _adjacent(stem: str) -> list[str]:
    m = re.match(r"treasury_bulletin_(\d{4})_(\d{2})", stem)
    if not m:
        return [stem]
    y, mo = int(m.group(1)), int(m.group(2))
    out = []
    for dm in (0, 1, 2, 3, -1):
        ny, nmo = y, mo + dm
        while nmo > 12: nmo -= 12; ny += 1
        while nmo < 1: nmo += 12; ny -= 1
        out.append(f"treasury_bulletin_{ny}_{nmo:02d}")
    return list(dict.fromkeys(out))


def _build_patterns(keywords: list[str], q: str) -> list[str]:
    pats = [re.escape(k) for k in keywords]
    if not pats:
        pats = [re.escape(w) for w in re.findall(r"[A-Z][a-zA-Z]{4,}", q)[:8]]
    return pats


def _file_blocks(stem: str, pats: list[str], per_file_cap: int) -> str:
    """Return large contiguous section(s) of a file around keyword hits.

    If the file is small, return it (nearly) whole. Otherwise merge nearby hits
    into wide windows (covering whole tables and their continuations)."""
    path = CORPUS / f"{stem}.sonnet46.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    n = len(lines)
    # Small file -> hand it over whole.
    if len(text) <= per_file_cap:
        return f"=== {stem} (full file, {n} lines) ===\n" + text[:per_file_cap]

    hits = sorted({i for i, ln in enumerate(lines)
                   for p in pats if re.search(p, ln, re.IGNORECASE)})
    if not hits:
        return ""  # caller decides fallback
    # Merge hits within 250 lines into single wide windows.
    wins, cur = [], [hits[0]]
    for h in hits[1:]:
        if h - cur[-1] <= 250:
            cur.append(h)
        else:
            wins.append(cur); cur = [h]
    wins.append(cur)
    out_blocks = []
    used = 0
    for w in wins:
        lo, hi = max(0, w[0] - 80), min(n, w[-1] + 300)
        seg = "\n".join(lines[lo:hi])
        if used + len(seg) > per_file_cap:
            seg = seg[: max(0, per_file_cap - used)]
        out_blocks.append(f"=== {stem} (lines {lo}-{hi}) ===\n" + seg)
        used += len(seg)
        if used >= per_file_cap:
            break
    return "\n\n".join(out_blocks)


def stage_retrieve(files: list[str], keywords: list[str], q: str,
                   cap: int = 90000) -> tuple[str, list[str]]:
    if not files:
        for mo, num in _MONTHS.items():
            for y in re.findall(rf"{mo}\s+(\d{{4}})", q.lower()):
                files.append(f"treasury_bulletin_{y}_{num:02d}")
    cands = []
    for f in files:
        cands += _adjacent(f)
    cands = list(dict.fromkeys(cands))
    # Keep only existing files; cap number to keep context manageable.
    cands = [c for c in cands if (CORPUS / f"{c}.sonnet46.md").exists()][:8]
    pats = _build_patterns(keywords, q)

    # Pass 1: keyword-anchored large blocks.
    per_file_cap = max(12000, cap // max(1, min(len(cands), 6)))
    blocks, matched = [], []
    used = 0
    for stem in cands:
        if used >= cap:
            break
        b = _file_blocks(stem, pats, min(per_file_cap, cap - used))
        if b:
            blocks.append(b); matched.append(stem); used += len(b)

    if blocks:
        return ("\n\n".join(blocks))[:cap], matched

    # Pass 2: no keyword hits anywhere -> hand over the top candidate files whole.
    used = 0
    for stem in cands[:4]:
        if used >= cap:
            break
        path = CORPUS / f"{stem}.sonnet46.md"
        text = path.read_text(encoding="utf-8", errors="replace")
        chunk = text[: min(per_file_cap, cap - used)]
        blocks.append(f"=== {stem} (full file head) ===\n" + chunk)
        used += len(chunk)
    if blocks:
        return ("\n\n".join(blocks))[:cap], cands[:4]
    return "(no candidate files found)", []


# ---------- Stage 3: SOLVE (emit python) ----------
SOLVE_SYS = """You answer an OfficeQA Treasury-Bulletin question from the provided excerpts. The excerpts are LARGE — they contain whole tables (and their continuations). The needed data IS almost certainly present somewhere in the excerpts; read carefully through ALL of them before concluding anything is missing.

Steps:
1. Find the exact table, row, and dated column. Tables may span multiple lines / continuation blocks; figures may be on lines following their label. Prefer the most FINAL/REVISED figures ((r) = revised). Mind units (thousands vs millions vs billions), calendar vs fiscal year, gross vs net, total vs subtotal. Strip footnote markers ((r), (p), 1/, *, etc.) before using numbers.
2. Write a single self-contained python3 program that hard-codes the extracted values, performs the computation, and PRINTS the final numeric/text answer (and ONLY that on the last line). For external constants not in the excerpts (e.g. BLS CPI-U index values, FX rates), inline your best-known values with a comment.

DO NOT abstain. Do NOT print "Cannot answer", "INSUFFICIENT DATA", "Cannot be determined", or similar — the answer is derivable from the excerpts; locate it. If truly torn between candidate values, pick the single most plausible one and print it.

Output the program in ONE ```python ... ``` block. No prose outside the code block."""

_BAD = re.compile(r"\b(os\.system|subprocess|shutil|rmtree|socket|requests|urllib|open\s*\([^)]*['\"][wa])", re.I)
_ABSTAIN = re.compile(r"(cannot\s+(answer|be\s+determined|compute)|insufficient\s+data|not\s+present|no\s+data|unable\s+to)", re.I)


def stage_solve(q: str, windows: str, feedback: str = "") -> str:
    user = f"Question: {q}\n\nExcerpts:\n{windows}"
    if feedback:
        user += (f"\n\nA PREVIOUS attempt was judged INCORRECT or abstained: {feedback}\n"
                 f"Re-read ALL excerpts carefully — the figure IS there. Re-check the table/row/"
                 f"dated column, units, and arithmetic. Produce a concrete numeric/text answer.")
    out = llm(SOLVE_SYS, user, 4000)
    m = re.search(r"```(?:python)?\s*(.*?)```", out, re.DOTALL)
    return m.group(1).strip() if m else out.strip()


# ---------- Stage 4b: VERIFY ----------
VERIFY_SYS = """You verify a candidate answer to an OfficeQA Treasury-Bulletin question. Given the question, the source excerpts, the python program used, and its printed result, check RIGOROUSLY:
(a) was the correct table, row, and dated column used?
(b) correct units/scale (thousands vs millions vs billions), calendar vs fiscal year, gross vs net, total vs subtotal?
(c) are the extracted source values ACTUALLY present in the excerpts (re-read and confirm each)?
(d) is the arithmetic correct, and does the result match the scale/precision the question asks for?
If the printed result is an abstention (e.g. "Cannot answer"), that is automatically a FAILURE — the data is in the excerpts and must be located.
Output ONLY JSON: {"ok": true|false, "issue": "<if not ok: the specific error to fix, including where in the excerpts the right value appears; else empty>"}."""


def stage_verify(q: str, windows: str, code: str, result: str) -> tuple[bool, str]:
    if _ABSTAIN.search(result or ""):
        return False, "The result abstained; the value is present in the excerpts — locate it and compute."
    out = llm(VERIFY_SYS, f"Question: {q}\n\nExcerpts:\n{windows}\n\nProgram:\n{code}\n\nPrinted result: {result}", 900)
    m = re.search(r"\{.*\}", out, re.DOTALL)
    if not m:
        return True, ""
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
FORMAT_SYS = """You produce the FINAL answer string for an OfficeQA question, graded by EXACT string match. Given the question and a computed result, output ONLY <FINAL_ANSWER>...</FINAL_ANSWER>. Inside: only the value at the scale asked; no units/'$' unless required; round to exactly the requested decimal places (keep trailing zeros); for a list use the exact bracket/separator format the question prescribes; thousands separators only if the question's own figures use them. Never output an abstention phrase."""


def stage_format(q: str, result: str) -> str:
    out = llm(FORMAT_SYS, f"Question: {q}\n\nComputed result: {result}", 600)
    try:
        return extract_final_answer(out)
    except Exception:
        return result


def pipeline(rec: dict, max_outer: int = 3, max_solve: int = 2) -> dict:
    q = rec["question"]
    feedback, result, code, windows, files, kws = "", "", "", "", [], []
    matched = []
    attempts = []
    solved = False
    best_result, best_code = "", ""
    for outer in range(max_outer):
        files, kws = stage_locate(q, feedback)
        windows, matched = stage_retrieve(list(files), kws, q)
        if windows.startswith("(no candidate"):
            feedback = (f"No candidate files found for keywords {kws} / files {files}. The data is "
                        f"likely in a different issue month (often a LATER issue).")
            attempts.append({"outer": outer, "retrieval": "no_files", "files": files, "keywords": kws})
            continue
        for inner in range(max_solve):
            code = stage_solve(q, windows, feedback if (outer or inner) else "")
            result = stage_run(code)
            if not result:
                feedback = "The program printed no final answer; ensure it prints the computed answer."
                attempts.append({"outer": outer, "inner": inner, "run": "empty"})
                continue
            if not best_result and not _ABSTAIN.search(result):
                best_result, best_code = result, code
            ok, issue = stage_verify(q, windows, code, result)
            attempts.append({"outer": outer, "inner": inner, "result": result,
                             "verify_ok": ok, "issue": issue[:200], "matched": matched})
            if ok:
                solved = True
                best_result, best_code = result, code
                break
            feedback = issue or "the answer was judged incorrect; re-extract and recompute"
        if solved:
            break
    # Prefer a verified/non-abstaining result; never emit an abstention if we have any number.
    final_result = result
    if (not final_result or _ABSTAIN.search(final_result)) and best_result:
        final_result = best_result
        code = best_code or code
    pred = stage_format(q, final_result) if final_result else ""
    try:
        sc = score_answer(rec["gold_answer"], pred) if pred else 0.0
    except Exception:
        sc = 0.0
    return {"uid": rec["uid"], "predicted": pred, "score": sc, "result": final_result,
            "files": files, "keywords": kws, "matched": matched, "code": code,
            "gold": rec["gold_answer"], "attempts": attempts, "n_attempts": len(attempts)}


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
    print(f"pipeline: {len(rows)} questions  model={MODEL}", flush=True)
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

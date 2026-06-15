#!/usr/bin/env python3
"""An agentic pipeline for OfficeQA (no-oracle parsed-md).

DIAGNOSIS OF DOMINANT FAILURE: 7/12 dev failures are abstentions ("Cannot
answer" / "INSUFFICIENT DATA"). The root cause is RETRIEVAL STARVATION: the
small grep windows (40 lines before / 100 after around keyword hits) almost
never capture the right cell in these wide, footnote-heavy, multi-page Treasury
tables. The LLM keeps saying the data "is not present in the excerpts" — because
it genuinely isn't in the tiny window. The model identifies the correct TABLE
(e.g. FFO-5, MS-1, ESF-1) but the relevant dated column/row is outside the
window or split across a table continuation.

FIX: Replace narrow grep windows with a much more generous, table-aware
retrieval: (1) locate candidate files, (2) find ALL keyword hits and emit large
contiguous windows that span full table blocks and follow continuations, and
(3) when keyword hits are sparse but a file is clearly the right issue, fall
back to feeding large slices / the whole (capped) file so the model has the
actual numbers. Also strongly discourage abstention: if the model wants to
abstain, force it to first dump every candidate value it sees, and treat
abstention as a retrieval failure that triggers a broader re-read with a much
larger budget.
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
LOCATE_SYS = """You route an OfficeQA question to U.S. Treasury Bulletin issues. The corpus has one Markdown file per monthly issue named treasury_bulletin_{YEAR}_{MM}.sonnet46.md (1939-2025). A statistic usually appears in the issue covering its period or, for annual/fiscal-year or end-of-period tables, in a LATER issue (often 2-3 months after the period close; e.g. a "December 31, 1959" survey is often in the following March issue; a full prior-calendar-year table in a Jan-Mar issue of the next year). Time-series tables in a single issue often show MANY months/years of history, so the answer to a question about an old date may live in a more recent issue's historical table.

Output ONLY a JSON object: {"files": ["treasury_bulletin_YYYY_MM", ...], "keywords": ["distinctive table title / row label / section name", ...]}. List 1-4 candidate files (most likely first; include publish-later candidates). Give 3-8 SPECIFIC grep keywords: prefer official table codes (e.g. FFO-5, MS-1, ESF-1, OFS), exact table titles, and distinctive row labels. Avoid generic words."""


def stage_locate(q: str, feedback: str = "") -> tuple[list[str], list[str]]:
    user = f"Question: {q}"
    if feedback:
        user += (f"\n\nA PREVIOUS attempt failed: {feedback}\nPropose DIFFERENT candidate files "
                 f"(try earlier/later issue months, and recent issues with historical series) "
                 f"and/or different table titles/codes/row labels as keywords.")
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


# ---------- Stage 2: RETRIEVE (table-aware, generous windows) ----------
def _adjacent(stem: str) -> list[str]:
    m = re.match(r"treasury_bulletin_(\d{4})_(\d{2})", stem)
    if not m:
        return [stem]
    y, mo = int(m.group(1)), int(m.group(2))
    out = []
    for dm in (0, 1, 2, 3, -1, -2):
        ny, nmo = y, mo + dm
        while nmo > 12: nmo -= 12; ny += 1
        while nmo < 1: nmo += 12; ny -= 1
        out.append(f"treasury_bulletin_{ny}_{nmo:02d}")
    return list(dict.fromkeys(out))


def _windows_for_file(path: Path, pats, before: int, after: int, max_wins: int) -> list[tuple[int, int]]:
    """Return merged (lo,hi) line windows around keyword hits in one file."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    n = len(lines)
    hits = sorted({i for i, ln in enumerate(lines)
                   for p in pats if re.search(p, ln, re.IGNORECASE)})
    if not hits:
        return []
    wins, cur = [], [hits[0]]
    for h in hits[1:]:
        if h - cur[-1] <= (before + after):
            cur.append(h)
        else:
            wins.append(cur); cur = [h]
    wins.append(cur)
    out = []
    for w in wins[:max_wins]:
        lo, hi = max(0, w[0] - before), min(n, w[-1] + after)
        out.append((lo, hi))
    return out


def stage_retrieve(files: list[str], keywords: list[str], q: str,
                   cap: int = 60000, broad: bool = False) -> str:
    """Generous, table-aware retrieval.

    Normal mode: large windows (120 before / 400 after) around keyword hits,
    enough to span full table blocks plus continuations. Broad mode (retry):
    even larger windows AND, for the strongest candidate file with no/few hits,
    dump a big head slice so the model sees the actual numbers.
    """
    if not files:
        for mo, n in _MONTHS.items():
            for y in re.findall(rf"{mo}\s+(\d{{4}})", q.lower()):
                files.append(f"treasury_bulletin_{y}_{n:02d}")
    cands = []
    for f in files:
        cands += _adjacent(f)
    cands = list(dict.fromkeys(cands))
    # cap candidate set
    cands = cands[:8 if broad else 8]

    pats = [re.escape(k) for k in keywords] or [re.escape(w) for w in re.findall(r"[A-Z][a-zA-Z]{4,}", q)[:6]]
    before = 200 if broad else 120
    after = 700 if broad else 400
    max_wins = 5 if broad else 4

    blocks = []
    total = 0
    any_hit = False
    for stem in cands:
        path = CORPUS / f"{stem}.sonnet46.md"
        if not path.exists():
            continue
        wins = _windows_for_file(path, pats, before, after, max_wins)
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if wins:
            any_hit = True
            for lo, hi in wins:
                txt = "\n".join(lines[lo:hi])
                seg = f"=== {stem}  (lines {lo}-{hi}) ===\n{txt}"
                blocks.append(seg)
                total += len(seg)
                if total > cap:
                    break
        if total > cap:
            break

    # Broad fallback: if nothing matched, or in broad mode, feed a large head
    # slice of the top candidate files so the model actually sees the numbers.
    if (broad or not any_hit):
        for stem in cands[:3]:
            path = CORPUS / f"{stem}.sonnet46.md"
            if not path.exists():
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            slice_lines = lines[:1200]
            seg = f"=== {stem}  (HEAD lines 0-{len(slice_lines)}) ===\n" + "\n".join(slice_lines)
            blocks.append(seg)
            total += len(seg)
            if total > cap:
                break

    text = "\n\n".join(blocks)[:cap]
    return text or "(no matching excerpts found)"


# ---------- Stage 3: SOLVE (emit python) ----------
SOLVE_SYS = """You answer an OfficeQA Treasury-Bulletin question from the provided excerpts. The excerpts are LARGE and table-heavy; the answer IS almost always present somewhere in them — scan thoroughly before concluding otherwise.

Steps:
1. Identify the exact table, row, and dated column. Tables are wide and rows may wrap across multiple lines; values for a labeled row may appear a few lines below the label. Prefer the most FINAL/REVISED figures ((r) = revised). Mind units (thousands vs millions vs billions), calendar vs fiscal year, gross vs net, total vs subtotal. Strip footnote markers/letters before using numbers.
2. Write a single self-contained python3 program that HARD-CODES the extracted values, performs the computation, and PRINTS the final numeric/text answer (only that, on the last line). For external constants the excerpts cannot contain (e.g. BLS CPI-U, FX rates), inline best-known values as variables with a comment.

DO NOT ABSTAIN. Do not print "Cannot answer", "INSUFFICIENT DATA", or similar. If the exact cell seems missing, re-scan the excerpts (check table continuations, adjacent months in history columns, wrapped rows) and use the best-supported numbers you can find; commit to a concrete numeric answer.

Output the program in one ```python ... ``` block. No prose outside the code block."""

_BAD = re.compile(r"\b(os\.system|subprocess|shutil|rmtree|socket|requests|urllib|open\s*\([^)]*['\"][wa])", re.I)
_ABSTAIN = re.compile(r"(cannot|can't|cant|insufficient|not present|not found|unable|"
                      r"cannot be determined|cannot compute|no data|missing)", re.I)


def stage_solve(q: str, windows: str, feedback: str = "") -> str:
    user = f"Question: {q}\n\nExcerpts:\n{windows}"
    if feedback:
        user += (f"\n\nA PREVIOUS attempt was judged INCORRECT or abstained: {feedback}\n"
                 f"The data IS in the excerpts — re-scan carefully (table continuations, wrapped "
                 f"rows, history columns), re-check the table/row/dated column, units, and arithmetic, "
                 f"and commit to a concrete numeric answer. DO NOT abstain.")
    out = llm(SOLVE_SYS, user, 4000)
    m = re.search(r"```(?:python)?\s*(.*?)```", out, re.DOTALL)
    return m.group(1).strip() if m else out.strip()


# ---------- Stage 4b: VERIFY ----------
VERIFY_SYS = """You verify a candidate answer to an OfficeQA Treasury-Bulletin question. Given the question, the source excerpts, the python program, and its printed result, check:
(a) correct table, row, dated column?
(b) correct units/scale and calendar vs fiscal year, gross vs net, total vs subtotal?
(c) are the extracted source values present in the excerpts (re-read; note rows may wrap and values may sit a few lines from the label)?
(d) arithmetic correct, result at the scale/precision the question asks?

If the result is an abstention ("cannot", "insufficient", etc.), ALWAYS set ok=false (an answer must be a concrete value). Output ONLY JSON: {"ok": true|false, "issue": "<specific fix if not ok; else empty>"}."""


def stage_verify(q: str, windows: str, code: str, result: str) -> tuple[bool, str]:
    if _ABSTAIN.search(result or ""):
        return False, "The result is an abstention; the data is in the excerpts — extract a concrete value."
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
FORMAT_SYS = """You produce the FINAL answer string for an OfficeQA question, graded by EXACT string match. Given the question and a computed result, output ONLY <FINAL_ANSWER>...</FINAL_ANSWER>. Inside: only the value at the scale asked; no units/'$' unless required; round to exactly the requested decimal places (keep trailing zeros); for a list use the exact bracket/separator format the question prescribes; include thousands separators (commas) only if the question's own figures use them. Never output an abstention here."""


def stage_format(q: str, result: str) -> str:
    out = llm(FORMAT_SYS, f"Question: {q}\n\nComputed result: {result}", 600)
    try:
        return extract_final_answer(out)
    except Exception:
        return result


def pipeline(rec: dict, max_outer: int = 3, max_solve: int = 2) -> dict:
    """Stages with a bounded verify->retry loop. On abstention/empty retrieval,
    escalate to BROAD retrieval (much larger windows + head dumps) so the model
    actually sees the numbers, then re-solve."""
    q = rec["question"]
    feedback, result, code, windows, files, kws = "", "", "", "", [], []
    attempts = []
    solved = False
    for outer in range(max_outer):
        broad = outer >= 1  # escalate retrieval breadth after first failure
        files, kws = stage_locate(q, feedback)
        windows = stage_retrieve(list(files), kws, q, broad=broad)
        if windows.startswith("(no matching"):
            # force a broad head-dump retrieval even without keyword hits
            windows = stage_retrieve(list(files), kws, q, broad=True)
        if windows.startswith("(no matching"):
            feedback = (f"No excerpts found in files {files} for keywords {kws}. The data is likely "
                        f"in a different issue month (often a LATER issue with historical series) "
                        f"or under a different table title/code.")
            attempts.append({"outer": outer, "retrieval": "empty", "files": files, "keywords": kws})
            continue
        for inner in range(max_solve):
            code = stage_solve(q, windows, feedback if (outer or inner) else "")
            result = stage_run(code)
            if not result:
                feedback = "The program printed no final answer; ensure it prints a concrete computed answer."
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
    pred = stage_format(q, result) if result and not _ABSTAIN.search(result) else ""
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
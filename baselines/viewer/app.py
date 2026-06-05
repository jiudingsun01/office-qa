#!/usr/bin/env python3
"""OfficeQA baseline result viewer.

Index page lists every question with status / cost / time, filterable by
correct / wrong / failed / pending. Detail page shows the question, source
documents, gold answer, predicted answer, and the parsed Claude Code
trajectory (thinking + text content blocks) with a collapsible raw event panel.

    .venv/bin/python baselines/viewer/app.py [--run NAME] [--port 5000]
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from pathlib import Path
from typing import Any

from flask import Flask, abort, redirect, render_template_string, request, send_from_directory, url_for

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
RUNS_DIR = ROOT / "baselines" / "runs"
CORPUS = DATA / "treasury_bulletins_parsed" / "transformed"
PDFS = DATA / "treasury_bulletin_pdfs"

sys.path.insert(0, str(ROOT / "baselines"))
from reward import extract_final_answer, score_answer  # noqa: E402

app = Flask(__name__)


def list_runs() -> list[str]:
    if not RUNS_DIR.exists():
        return []
    return sorted(
        d.name for d in RUNS_DIR.iterdir()
        if d.is_dir() and (d / "preds").exists()
    )


def load_gold(csv_path: Path) -> dict[str, dict]:
    return {r["uid"]: r for r in csv.DictReader(open(csv_path))}


def status_for(rec: dict | None, gold: dict) -> tuple[str, str, float]:
    """Return (status, predicted, score). status in correct/wrong/failed/pending."""
    if rec is None:
        return "pending", "", 0.0
    if rec.get("rc") != 0:
        raw = rec.get("raw_response") or ""
        try:
            pred = extract_final_answer(raw) if raw else ""
        except ValueError:
            pred = ""
        return "failed", pred, 0.0
    raw = rec.get("raw_response") or ""
    try:
        pred = extract_final_answer(raw)
    except ValueError:
        pred = ""
    try:
        sc = score_answer(gold["answer"], pred) if pred else 0.0
    except Exception:
        sc = 0.0
    return ("correct" if sc >= 1.0 else "wrong"), pred, sc


def load_run(run_name: str) -> tuple[dict[str, dict], dict[str, dict]]:
    """Return (gold_by_uid, pred_by_uid)."""
    csv_path = DATA / "officeqa_pro.csv"
    gold = load_gold(csv_path)
    preds_dir = RUNS_DIR / run_name / "preds"
    pred: dict[str, dict] = {}
    if preds_dir.exists():
        for p in preds_dir.glob("*.json"):
            try:
                pred[p.stem] = json.loads(p.read_text())
            except Exception:
                continue
    return gold, pred


def parse_trace(run_name: str, uid: str) -> dict[str, Any]:
    """Pull content blocks (thinking + text) and the raw event list from the trace."""
    trace_path = RUNS_DIR / run_name / "traces" / f"{uid}.jsonl"
    if not trace_path.exists():
        return {"blocks": [], "events": [], "system": [], "result": None}

    events: list[dict] = []
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    blocks: list[dict] = []
    seen_block_ids: set[tuple[str, str, int]] = set()
    system: list[dict] = []
    result_evt = None
    for e in events:
        t = e.get("type")
        if t == "system":
            system.append(e)
        elif t == "result":
            result_evt = e
        elif t in ("assistant", "user"):
            msg = e.get("message") or {}
            msg_id = msg.get("id") or e.get("uuid") or ""
            for idx, blk in enumerate(msg.get("content") or []):
                key = (t, msg_id, idx)
                if key in seen_block_ids:
                    continue
                seen_block_ids.add(key)
                blocks.append({**blk, "_role": t})
    return {"blocks": blocks, "events": events, "system": system, "result": result_evt}


def status_classes() -> dict[str, str]:
    return {
        "correct": "ok",
        "wrong":   "bad",
        "failed":  "fail",
        "pending": "pend",
    }


BASE_CSS = """
:root { color-scheme: light dark; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  margin: 0; padding: 0; background: #f7f7f8; color: #1a1a1a;
}
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }
header { background: #1f2937; color: white; padding: 12px 24px; }
header h1 { font-size: 16px; margin: 0; font-weight: 500; }
header .meta { font-size: 12px; color: #9ca3af; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,.05); }
th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; font-size: 13px; }
th { background: #f3f4f6; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: .03em; color: #6b7280; }
tr:hover td { background: #fafafa; }
td.q { max-width: 480px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.badge.ok   { background: #dcfce7; color: #166534; }
.badge.bad  { background: #fee2e2; color: #991b1b; }
.badge.fail { background: #fef3c7; color: #92400e; }
.badge.pend { background: #e5e7eb; color: #374151; }
.filters { display: flex; gap: 8px; margin: 16px 0; flex-wrap: wrap; align-items: center; }
.chip {
  padding: 4px 12px; border: 1px solid #d1d5db; background: white;
  border-radius: 999px; font-size: 12px; cursor: pointer; user-select: none;
}
.chip.active { background: #1f2937; color: white; border-color: #1f2937; }
.summary { display: flex; gap: 24px; margin-bottom: 16px; font-size: 13px; color: #4b5563; flex-wrap: wrap; }
.summary b { color: #111; font-weight: 600; }
.detail-grid { display: grid; grid-template-columns: 1fr 360px; gap: 24px; }
@media (max-width: 900px) { .detail-grid { grid-template-columns: 1fr; } }
.card { background: white; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,.05); }
.card h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: #6b7280; margin: 0 0 8px; font-weight: 600; }
.card h3 { font-size: 14px; margin: 0 0 8px; }
.q-text { font-size: 16px; line-height: 1.5; color: #111; }
.answer-row { display: grid; grid-template-columns: max-content 1fr; gap: 8px 16px; align-items: baseline; }
.answer-row .label { font-size: 12px; color: #6b7280; text-transform: uppercase; }
.answer-row .val { font-family: ui-monospace, monospace; font-size: 14px; }
.answer-row .val.gold    { color: #166534; }
.answer-row .val.pred-ok { color: #166534; font-weight: 600; }
.answer-row .val.pred-bad{ color: #991b1b; font-weight: 600; }
.kvs { display: grid; grid-template-columns: max-content 1fr; gap: 4px 12px; font-size: 12px; color: #4b5563; }
.kvs .k { color: #6b7280; }
.kvs .v { font-family: ui-monospace, monospace; }
.block { border-left: 3px solid #e5e7eb; padding: 0 0 0 12px; margin: 12px 0; }
.block.thinking    { border-color: #a78bfa; }
.block.text        { border-color: #60a5fa; }
.block.tool_use    { border-color: #f59e0b; }
.block.tool_result { border-color: #10b981; }
.block.document    { border-color: #ef4444; }
.block .block-type { font-size: 11px; text-transform: uppercase; color: #6b7280; letter-spacing: .05em; margin-bottom: 6px; }
.block .block-type .role { color: #9ca3af; font-weight: 400; margin-left: 6px; }
.block .body { white-space: pre-wrap; font-size: 14px; line-height: 1.55; color: #1f2937; word-wrap: break-word; }
.block .body mark { background: #fef08a; padding: 1px 4px; border-radius: 3px; }
.block.thinking .body { color: #4b5563; font-style: italic; }
.block.tool_use .body, .block.tool_result .body, .block.document .body {
  font-family: ui-monospace, monospace; font-size: 12px; background: #f9fafb;
  padding: 8px 10px; border-radius: 4px; white-space: pre-wrap;
}
details { margin-top: 16px; }
details summary { cursor: pointer; color: #4b5563; font-size: 13px; padding: 4px 0; }
pre.raw {
  font-family: ui-monospace, monospace; font-size: 11px; line-height: 1.4;
  background: #0b1020; color: #e5e7eb; padding: 12px; border-radius: 6px;
  overflow-x: auto; max-height: 480px; overflow-y: auto;
}
.src-file { margin-bottom: 12px; border: 1px solid #e5e7eb; border-radius: 6px; }
.src-file > summary { font-weight: 500; padding: 8px 12px; background: #fafafa; border-radius: 6px; }
.src-file[open] > summary { border-bottom: 1px solid #e5e7eb; border-radius: 6px 6px 0 0; }
.src-file .src-body { padding: 12px; }
.src-file .src-links { display: flex; gap: 12px; font-size: 12px; margin-bottom: 8px; }
.src-file .src-links a { padding: 2px 8px; background: #eff6ff; border-radius: 4px; }
.src-file embed.pdf { width: 100%; height: 720px; border: 1px solid #e5e7eb; border-radius: 4px; background: white; }
.src-file .no-pdf { color: #6b7280; font-size: 12px; padding: 16px; background: #f9fafb; border-radius: 4px; text-align: center; }
.src-file pre {
  font-family: ui-monospace, monospace; font-size: 11px; line-height: 1.4;
  background: #fafafa; color: #1f2937; padding: 12px; border-radius: 6px;
  max-height: 360px; overflow: auto; white-space: pre-wrap; word-wrap: break-word;
}
.src-file .nested-parsed { margin-top: 12px; }
.src-file .nested-parsed summary { font-size: 12px; color: #6b7280; cursor: pointer; padding: 4px 0; }
.nav { display: flex; gap: 12px; font-size: 13px; margin: 8px 0; }
.nav a { padding: 4px 10px; border: 1px solid #d1d5db; border-radius: 6px; background: white; }
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 1100px) { .compare-grid { grid-template-columns: 1fr; } }
.compare-col h3 { font-size: 13px; margin: 0 0 8px; padding: 6px 12px; border-radius: 6px; background: #eff6ff; color: #1e3a8a; }
.compare-col .traj-scroll { max-height: 720px; overflow-y: auto; padding-right: 8px; }
.agree-icon { font-size: 14px; }
.agree-both-correct { color: #166534; }
.agree-both-wrong   { color: #991b1b; }
.agree-disagree     { color: #b45309; }
.run-pick { display: flex; gap: 8px; font-size: 13px; align-items: center; margin: 8px 0; }
.run-pick select { padding: 4px 8px; font-size: 13px; border-radius: 6px; border: 1px solid #d1d5db; background: white; }
"""


INDEX_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>OfficeQA · {{ run }}</title>
<style>{{ css|safe }}</style></head><body>
<header>
  <h1>OfficeQA viewer · run = <code>{{ run }}</code></h1>
  <div class="meta">
    {% if runs|length > 1 %}
      switch: {% for r in runs %}{% if r != run %}<a href="?run={{ r }}" style="color:#9ca3af; margin-right:8px;">{{ r }}</a>{% endif %}{% endfor %}
      · <a href="{{ url_for('compare_index') }}" style="color:#fbbf24">compare runs →</a>
    {% endif %}
    · <a href="{{ url_for('hermes_index_full') }}" style="color:#34d399">Hermes full_eval →</a>
  </div>
</header>
<div class="container">
  <div class="summary">
    <span><b>{{ counts.total }}</b> total</span>
    <span><b>{{ counts.correct }}</b> correct</span>
    <span><b>{{ counts.wrong }}</b> wrong</span>
    <span><b>{{ counts.failed }}</b> failed</span>
    <span><b>{{ counts.pending }}</b> pending</span>
    {% if counts.scored %}<span>accuracy (scored): <b>{{ '%.1f'|format(100*counts.correct/counts.scored) }}%</b></span>{% endif %}
    {% if counts.total_cost %}<span>cost: <b>${{ '%.2f'|format(counts.total_cost) }}</b></span>{% endif %}
  </div>

  <div class="filters">
    <span style="color:#6b7280;font-size:12px;">filter:</span>
    <span class="chip {{ 'active' if filt=='all' else '' }}"     data-filt="all">all ({{ counts.total }})</span>
    <span class="chip {{ 'active' if filt=='correct' else '' }}" data-filt="correct">correct ({{ counts.correct }})</span>
    <span class="chip {{ 'active' if filt=='wrong' else '' }}"   data-filt="wrong">wrong ({{ counts.wrong }})</span>
    <span class="chip {{ 'active' if filt=='failed' else '' }}"  data-filt="failed">failed ({{ counts.failed }})</span>
    <span class="chip {{ 'active' if filt=='pending' else '' }}" data-filt="pending">pending ({{ counts.pending }})</span>
  </div>

  <table id="rows">
    <thead><tr>
      <th>uid</th><th>status</th><th>question</th>
      <th>gold</th><th>predicted</th><th>cost</th><th>time</th>
    </tr></thead>
    <tbody>
    {% for r in rows %}
      <tr data-status="{{ r.status }}">
        <td><a href="{{ url_for('detail', run=run, uid=r.uid) }}">{{ r.uid }}</a></td>
        <td><span class="badge {{ status_cls[r.status] }}">{{ r.status }}</span></td>
        <td class="q" title="{{ r.question }}">{{ r.question }}</td>
        <td><code>{{ r.gold }}</code></td>
        <td><code>{{ r.predicted }}</code></td>
        <td>{% if r.cost is not none %}${{ '%.2f'|format(r.cost) }}{% endif %}</td>
        <td>{% if r.elapsed is not none %}{{ '%.0f'|format(r.elapsed) }}s{% endif %}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
<script>
  const chips = document.querySelectorAll('.chip');
  const rows = document.querySelectorAll('#rows tbody tr');
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.classList.remove('active'));
    c.classList.add('active');
    const f = c.dataset.filt;
    rows.forEach(r => {
      r.style.display = (f === 'all' || r.dataset.status === f) ? '' : 'none';
    });
    const url = new URL(window.location);
    if (f === 'all') url.searchParams.delete('filt'); else url.searchParams.set('filt', f);
    history.replaceState({}, '', url);
  }));
</script>
</body></html>
"""


DETAIL_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>{{ uid }} · {{ run }}</title>
<style>{{ css|safe }}</style></head><body>
<header>
  <h1>{{ uid }} · <span class="badge {{ status_cls[status] }}">{{ status }}</span></h1>
  <div class="meta"><a href="{{ url_for('index') }}?run={{ run }}" style="color:#9ca3af">← back to {{ run }}</a></div>
</header>
<div class="container">
  <div class="nav">
    {% if prev_uid %}<a href="{{ url_for('detail', run=run, uid=prev_uid) }}">← {{ prev_uid }}</a>{% endif %}
    {% if next_uid %}<a href="{{ url_for('detail', run=run, uid=next_uid) }}">{{ next_uid }} →</a>{% endif %}
  </div>

  <div class="detail-grid">
    <div>
      <div class="card">
        <h2>question</h2>
        <div class="q-text">{{ question }}</div>
      </div>

      <div class="card">
        <h2>answer</h2>
        <div class="answer-row">
          <span class="label">gold</span><span class="val gold">{{ gold }}</span>
          <span class="label">predicted</span>
          <span class="val {{ 'pred-ok' if status=='correct' else 'pred-bad' }}">{{ predicted or '(none extracted)' }}</span>
          <span class="label">score</span><span class="val">{{ score }}</span>
        </div>
      </div>

      <div class="card">
        <h2>trajectory · {{ blocks|length }} content block(s)</h2>
        {% for blk in blocks %}
          <div class="block {{ blk.type }}">
            <div class="block-type">{{ blk.type }}{% if blk.role %}<span class="role">· {{ blk.role }}</span>{% endif %}</div>
            <div class="body">{{ blk.html|safe }}</div>
          </div>
        {% endfor %}
        {% if not blocks %}
          <div style="color:#6b7280;font-size:13px;">(no parsed content blocks; check raw events below)</div>
        {% endif %}
      </div>

      <div class="card">
        <h2>source documents · {{ source_files|length }}</h2>
        {% for f in source_files %}
          <details class="src-file" {% if loop.first %}open{% endif %}>
            <summary>{{ f.name }} · {{ '%.0f'|format(f.size_kb) }} KB{% if f.pdf_size_mb %} · PDF {{ '%.1f'|format(f.pdf_size_mb) }} MB{% endif %}</summary>
            <div class="src-body">
              <div class="src-links">
                {% if f.fraser_url %}<a href="{{ f.fraser_url }}" target="_blank" rel="noopener">FRASER archive ↗</a>{% endif %}
                {% if f.pdf_url %}<a href="{{ f.pdf_url }}" target="_blank" rel="noopener">open PDF ↗</a>{% endif %}
              </div>
              {% if f.pdf_url %}
                <embed class="pdf" src="{{ f.pdf_url }}{% if f.page %}#page={{ f.page }}{% endif %}" type="application/pdf">
              {% else %}
                <div class="no-pdf">raw PDF not yet downloaded · check <code>data/treasury_bulletin_pdfs/</code></div>
              {% endif %}
              <details class="nested-parsed">
                <summary>show parsed text ({{ '%.0f'|format(f.size_kb) }} KB)</summary>
                <pre>{{ f.text }}</pre>
              </details>
            </div>
          </details>
        {% endfor %}
      </div>

      <details>
        <summary>raw events ({{ raw_count }})</summary>
        <pre class="raw">{{ raw_dump }}</pre>
      </details>
    </div>

    <aside>
      <div class="card">
        <h2>metadata</h2>
        <div class="kvs">
          <span class="k">model</span><span class="v">{{ meta.model }}</span>
          <span class="k">rc</span><span class="v">{{ meta.rc }}</span>
          <span class="k">cost</span><span class="v">{% if meta.cost_usd is not none %}${{ '%.4f'|format(meta.cost_usd) }}{% endif %}</span>
          <span class="k">elapsed</span><span class="v">{{ meta.elapsed_sec }}s</span>
          <span class="k">turns</span><span class="v">{{ meta.num_turns }}</span>
          {% if usage %}
          <span class="k">in / out</span><span class="v">{{ usage.input_tokens }} / {{ usage.output_tokens }}</span>
          <span class="k">cache create</span><span class="v">{{ usage.cache_creation_input_tokens }}</span>
          <span class="k">cache read</span><span class="v">{{ usage.cache_read_input_tokens }}</span>
          {% endif %}
          {% if result %}
          <span class="k">stop</span><span class="v">{{ result.stop_reason }}</span>
          <span class="k">api_error</span><span class="v">{{ result.api_error_status or '—' }}</span>
          {% endif %}
        </div>
      </div>
    </aside>
  </div>
</div>
</body></html>
"""


def render_text_with_final_answer(text: str) -> str:
    safe = html.escape(text)
    return safe.replace(
        "&lt;FINAL_ANSWER&gt;",
        "<mark>&lt;FINAL_ANSWER&gt;",
    ).replace(
        "&lt;/FINAL_ANSWER&gt;",
        "&lt;/FINAL_ANSWER&gt;</mark>",
    )


def _summarize_tool_result(c: Any) -> str:
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for it in c:
            ty = it.get("type") if isinstance(it, dict) else "?"
            if ty == "text":
                parts.append(it.get("text", ""))
            elif ty == "image":
                src = it.get("source", {}) or {}
                parts.append(f"[image · {src.get('media_type','?')} · {len(src.get('data',''))} b64 chars]")
            else:
                parts.append(f"[{ty}]")
        return "\n".join(parts)
    return json.dumps(c, ensure_ascii=False)


def render_block(blk: dict) -> dict:
    t = blk.get("type", "?")
    role = blk.get("_role", "")
    if t == "thinking":
        body_html = html.escape(blk.get("thinking", ""))
    elif t == "text":
        body_html = render_text_with_final_answer(blk.get("text", ""))
    elif t == "tool_use":
        name = blk.get("name", "?")
        inp = blk.get("input") or {}
        inp_str = json.dumps(inp, ensure_ascii=False, indent=2)
        body_html = f"<b>{html.escape(name)}</b>(<br>{html.escape(inp_str)}<br>)"
    elif t == "tool_result":
        body_html = html.escape(_summarize_tool_result(blk.get("content")))
        if blk.get("is_error"):
            body_html = "<span style='color:#991b1b'>ERROR:</span> " + body_html
    elif t == "document":
        src = blk.get("source", {}) or {}
        mt = src.get("media_type", "?")
        n = len(src.get("data", ""))
        body_html = html.escape(f"[document attached · {mt} · {n} b64 chars]")
    else:
        body_html = "<pre style='font-size:11px'>" + html.escape(json.dumps(blk, ensure_ascii=False)) + "</pre>"
    return {"type": t, "role": role, "html": body_html}


@app.route("/pdf/<path:filename>")
def pdf(filename: str):
    # Restrict to .pdf files under data/treasury_bulletin_pdfs only.
    if not filename.endswith(".pdf") or "/" in filename or ".." in filename:
        abort(404)
    return send_from_directory(PDFS, filename, mimetype="application/pdf")


@app.route("/")
def index():
    runs = list_runs()
    if not runs:
        return "No runs found under baselines/runs/. Generate predictions first.", 404
    run = request.args.get("run") or runs[0]
    if run not in runs:
        return redirect(url_for("index"))
    filt = request.args.get("filt", "all")

    gold, preds = load_run(run)
    rows = []
    counts = {"total": 0, "correct": 0, "wrong": 0, "failed": 0, "pending": 0, "total_cost": 0.0, "scored": 0}
    for uid in sorted(gold.keys()):
        g = gold[uid]
        rec = preds.get(uid)
        st, pred, sc = status_for(rec, g)
        counts["total"] += 1
        counts[st] += 1
        if st in ("correct", "wrong"):
            counts["scored"] += 1
        if rec and isinstance(rec.get("cost_usd"), (int, float)):
            counts["total_cost"] += rec["cost_usd"]
        rows.append({
            "uid": uid,
            "status": st,
            "question": g["question"],
            "gold": g["answer"],
            "predicted": pred,
            "cost": (rec or {}).get("cost_usd"),
            "elapsed": (rec or {}).get("elapsed_sec"),
        })

    return render_template_string(
        INDEX_TPL,
        css=BASE_CSS,
        runs=runs,
        run=run,
        filt=filt,
        rows=rows,
        counts=counts,
        status_cls=status_classes(),
    )


@app.route("/q/<run>/<uid>")
def detail(run: str, uid: str):
    runs = list_runs()
    if run not in runs:
        abort(404)
    gold, preds = load_run(run)
    g = gold.get(uid)
    if not g:
        abort(404)
    rec = preds.get(uid)
    status, pred, sc = status_for(rec, g)

    trace = parse_trace(run, uid)
    blocks = [render_block(b) for b in trace["blocks"]]

    src_files = [s.strip() for s in g["source_files"].splitlines() if s.strip()]
    src_docs = [s.strip() for s in g["source_docs"].splitlines() if s.strip()]
    sf = []
    for i, fn in enumerate(src_files):
        p = CORPUS / fn
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        pdf_name = fn.replace(".txt", ".pdf")
        pdf_path = PDFS / pdf_name
        pdf_exists = pdf_path.exists()
        fraser = src_docs[i] if i < len(src_docs) else ""
        page = ""
        if "page=" in fraser:
            try:
                page = fraser.rsplit("page=", 1)[1].split("&")[0]
            except Exception:
                page = ""
        sf.append({
            "name": fn,
            "size_kb": p.stat().st_size / 1024,
            "text": text,
            "fraser_url": fraser,
            "pdf_url": url_for("pdf", filename=pdf_name) if pdf_exists else "",
            "pdf_size_mb": pdf_path.stat().st_size / 1e6 if pdf_exists else None,
            "page": page,
        })

    uids = sorted(gold.keys())
    i = uids.index(uid)
    prev_uid = uids[i - 1] if i > 0 else None
    next_uid = uids[i + 1] if i + 1 < len(uids) else None

    def _strip_b64(obj):
        # Elide any string value > 4 KB wherever it appears nested in the event.
        if isinstance(obj, dict):
            return {k: _strip_b64(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_strip_b64(x) for x in obj]
        if isinstance(obj, str) and len(obj) > 4096:
            return f"<{len(obj)} chars elided>"
        return obj

    raw_dump = "\n".join(json.dumps(_strip_b64(e), ensure_ascii=False) for e in trace["events"])

    return render_template_string(
        DETAIL_TPL,
        css=BASE_CSS,
        run=run,
        uid=uid,
        question=g["question"],
        gold=g["answer"],
        predicted=pred,
        score=sc,
        status=status,
        status_cls=status_classes(),
        blocks=blocks,
        source_files=sf,
        meta={
            "model": (rec or {}).get("model", ""),
            "rc": (rec or {}).get("rc", ""),
            "cost_usd": (rec or {}).get("cost_usd"),
            "elapsed_sec": (rec or {}).get("elapsed_sec", ""),
            "num_turns": (rec or {}).get("num_turns", ""),
        },
        usage=(rec or {}).get("usage"),
        result=trace["result"],
        raw_count=len(trace["events"]),
        raw_dump=raw_dump,
        prev_uid=prev_uid,
        next_uid=next_uid,
    )


COMPARE_INDEX_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>Compare runs · OfficeQA</title>
<style>{{ css|safe }}</style></head><body>
<header>
  <h1>OfficeQA · compare runs</h1>
  <div class="meta"><a href="{{ url_for('index') }}" style="color:#9ca3af">← back</a></div>
</header>
<div class="container">
  <form method="get" class="run-pick">
    <label>A:&nbsp;<select name="a">{% for r in runs %}<option value="{{ r }}" {% if r==a %}selected{% endif %}>{{ r }}</option>{% endfor %}</select></label>
    <label>B:&nbsp;<select name="b">{% for r in runs %}<option value="{{ r }}" {% if r==b %}selected{% endif %}>{{ r }}</option>{% endfor %}</select></label>
    <button type="submit" style="padding:4px 10px;border-radius:6px;border:1px solid #d1d5db;background:white;cursor:pointer;">apply</button>
  </form>

  <div class="summary">
    <span><b>{{ counts.total }}</b> total</span>
    <span>both correct: <b>{{ counts.both_correct }}</b></span>
    <span>both wrong: <b>{{ counts.both_wrong }}</b></span>
    <span>only A correct: <b>{{ counts.only_a }}</b></span>
    <span>only B correct: <b>{{ counts.only_b }}</b></span>
    <span>A acc (scored): <b>{{ '%.1f'|format(counts.a_acc*100) }}%</b> ({{ counts.a_correct }}/{{ counts.a_scored }})</span>
    <span>B acc (scored): <b>{{ '%.1f'|format(counts.b_acc*100) }}%</b> ({{ counts.b_correct }}/{{ counts.b_scored }})</span>
  </div>

  <div class="filters">
    <span style="color:#6b7280;font-size:12px;">filter:</span>
    <span class="chip active" data-filt="all">all ({{ counts.total }})</span>
    <span class="chip" data-filt="both_correct">both correct ({{ counts.both_correct }})</span>
    <span class="chip" data-filt="both_wrong">both wrong ({{ counts.both_wrong }})</span>
    <span class="chip" data-filt="only_a">only A correct ({{ counts.only_a }})</span>
    <span class="chip" data-filt="only_b">only B correct ({{ counts.only_b }})</span>
    <span class="chip" data-filt="disagree">A≠B ({{ counts.disagree }})</span>
  </div>

  <table id="rows">
    <thead><tr>
      <th>uid</th><th>question</th><th>gold</th>
      <th>A: {{ a }}</th>
      <th>B: {{ b }}</th>
      <th>agree</th>
    </tr></thead>
    <tbody>
    {% for r in rows %}
      <tr data-cat="{{ r.cat }}" data-disagree="{{ '1' if r.disagree else '0' }}">
        <td><a href="{{ url_for('compare_detail', uid=r.uid) }}?a={{ a }}&b={{ b }}">{{ r.uid }}</a></td>
        <td class="q" title="{{ r.question }}">{{ r.question }}</td>
        <td><code>{{ r.gold }}</code></td>
        <td><span class="badge {{ status_cls[r.a_status] }}">{{ r.a_status }}</span> <code style="font-size:12px">{{ r.a_pred }}</code></td>
        <td><span class="badge {{ status_cls[r.b_status] }}">{{ r.b_status }}</span> <code style="font-size:12px">{{ r.b_pred }}</code></td>
        <td>
          {% if r.cat == 'both_correct' %}<span class="agree-icon agree-both-correct">✓✓</span>
          {% elif r.cat == 'both_wrong' %}<span class="agree-icon agree-both-wrong">✗✗</span>
          {% elif r.disagree %}<span class="agree-icon agree-disagree">A≠B</span>
          {% else %}<span style="color:#9ca3af">—</span>{% endif %}
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
<script>
  const chips = document.querySelectorAll('.chip');
  const rows = document.querySelectorAll('#rows tbody tr');
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.classList.remove('active'));
    c.classList.add('active');
    const f = c.dataset.filt;
    rows.forEach(r => {
      let show;
      if (f === 'all') show = true;
      else if (f === 'disagree') show = r.dataset.disagree === '1';
      else show = r.dataset.cat === f;
      r.style.display = show ? '' : 'none';
    });
  }));
</script>
</body></html>
"""


COMPARE_DETAIL_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>{{ uid }} · compare</title>
<style>{{ css|safe }}</style></head><body>
<header>
  <h1>{{ uid }} · compare {{ a }} vs {{ b }}</h1>
  <div class="meta"><a href="{{ url_for('compare_index') }}?a={{ a }}&b={{ b }}" style="color:#9ca3af">← all comparisons</a></div>
</header>
<div class="container">
  <div class="nav">
    {% if prev_uid %}<a href="{{ url_for('compare_detail', uid=prev_uid) }}?a={{ a }}&b={{ b }}">← {{ prev_uid }}</a>{% endif %}
    {% if next_uid %}<a href="{{ url_for('compare_detail', uid=next_uid) }}?a={{ a }}&b={{ b }}">{{ next_uid }} →</a>{% endif %}
    <a href="{{ url_for('detail', run=a, uid=uid) }}" style="margin-left:auto">A solo →</a>
    <a href="{{ url_for('detail', run=b, uid=uid) }}">B solo →</a>
  </div>

  <div class="card">
    <h2>question</h2>
    <div class="q-text">{{ question }}</div>
    <div style="margin-top:8px" class="answer-row">
      <span class="label">gold</span><span class="val gold">{{ gold }}</span>
    </div>
  </div>

  <div class="compare-grid">
    {% for side in (sideA, sideB) %}
    <div class="compare-col">
      <h3>{{ side.label }}: {{ side.run }} · <span class="badge {{ status_cls[side.status] }}">{{ side.status }}</span></h3>
      <div class="card">
        <div class="answer-row">
          <span class="label">predicted</span>
          <span class="val {{ 'pred-ok' if side.status=='correct' else 'pred-bad' }}">{{ side.predicted or '(none)' }}</span>
          <span class="label">cost</span><span class="val">{% if side.cost is not none %}${{ '%.3f'|format(side.cost) }}{% endif %}</span>
          <span class="label">elapsed</span><span class="val">{{ side.elapsed }}s</span>
          <span class="label">turns</span><span class="val">{{ side.turns }}</span>
          {% if side.n_read_calls is not none %}<span class="label">read calls</span><span class="val">{{ side.n_read_calls }}</span>{% endif %}
        </div>
      </div>
      <div class="card">
        <h2>trajectory · {{ side.blocks|length }} blocks</h2>
        <div class="traj-scroll">
          {% for blk in side.blocks %}
            <div class="block {{ blk.type }}">
              <div class="block-type">{{ blk.type }}{% if blk.role %}<span class="role">· {{ blk.role }}</span>{% endif %}</div>
              <div class="body">{{ blk.html|safe }}</div>
            </div>
          {% endfor %}
          {% if not side.blocks %}
            <div style="color:#6b7280;font-size:13px;">(no trajectory; question may not have been run on this side yet)</div>
          {% endif %}
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="card" style="margin-top:16px">
    <h2>source documents · {{ source_files|length }}</h2>
    {% for f in source_files %}
      <details class="src-file">
        <summary>{{ f.name }} · {{ '%.0f'|format(f.size_kb) }} KB{% if f.pdf_size_mb %} · PDF {{ '%.1f'|format(f.pdf_size_mb) }} MB{% endif %}</summary>
        <div class="src-body">
          <div class="src-links">
            {% if f.fraser_url %}<a href="{{ f.fraser_url }}" target="_blank" rel="noopener">FRASER archive ↗</a>{% endif %}
            {% if f.pdf_url %}<a href="{{ f.pdf_url }}" target="_blank" rel="noopener">open PDF ↗</a>{% endif %}
          </div>
          {% if f.pdf_url %}
            <embed class="pdf" src="{{ f.pdf_url }}{% if f.page %}#page={{ f.page }}{% endif %}" type="application/pdf">
          {% endif %}
          <details class="nested-parsed"><summary>show parsed text</summary><pre>{{ f.text }}</pre></details>
        </div>
      </details>
    {% endfor %}
  </div>
</div>
</body></html>
"""


def _side(run: str, uid: str, gold_row: dict) -> dict:
    """Build a side dict for the comparison view."""
    if run not in list_runs():
        return {"label": "", "run": run, "status": "pending", "predicted": "", "cost": None,
                "elapsed": 0, "turns": 0, "n_read_calls": None, "blocks": []}
    preds_dir = RUNS_DIR / run / "preds"
    p = preds_dir / f"{uid}.json"
    rec = json.loads(p.read_text()) if p.exists() else None
    status, predicted, _ = status_for(rec, gold_row)
    trace = parse_trace(run, uid) if rec else {"blocks": []}
    blocks = [render_block(b) for b in trace["blocks"]]
    return {
        "label": "",
        "run": run,
        "status": status,
        "predicted": predicted,
        "cost": (rec or {}).get("cost_usd"),
        "elapsed": (rec or {}).get("elapsed_sec", 0),
        "turns": (rec or {}).get("num_turns", 0),
        "n_read_calls": (rec or {}).get("n_read_calls"),
        "blocks": blocks,
    }


def _default_compare_runs() -> tuple[str, str]:
    runs = list_runs()
    if not runs:
        return "", ""
    if len(runs) == 1:
        return runs[0], runs[0]
    # Prefer text-vs-pdf if both exist.
    a = next((r for r in runs if "pdf" not in r), runs[0])
    b = next((r for r in runs if r != a), runs[1])
    return a, b


@app.route("/compare")
def compare_index():
    runs = list_runs()
    if len(runs) < 1:
        return "No runs found.", 404
    default_a, default_b = _default_compare_runs()
    a = request.args.get("a") or default_a
    b = request.args.get("b") or default_b
    if a not in runs or b not in runs:
        return redirect(url_for("compare_index"))

    gold, preds_a = load_run(a)
    _, preds_b = load_run(b)

    counts = {
        "total": 0, "both_correct": 0, "both_wrong": 0,
        "only_a": 0, "only_b": 0, "disagree": 0,
        "a_correct": 0, "b_correct": 0, "a_scored": 0, "b_scored": 0,
        "a_acc": 0.0, "b_acc": 0.0,
    }
    rows = []
    for uid in sorted(gold.keys()):
        g = gold[uid]
        ra, rb = preds_a.get(uid), preds_b.get(uid)
        sa, pa, _ = status_for(ra, g)
        sb, pb, _ = status_for(rb, g)
        counts["total"] += 1
        if sa in ("correct", "wrong"):
            counts["a_scored"] += 1
            if sa == "correct":
                counts["a_correct"] += 1
        if sb in ("correct", "wrong"):
            counts["b_scored"] += 1
            if sb == "correct":
                counts["b_correct"] += 1
        if sa == "correct" and sb == "correct":
            cat = "both_correct"; counts["both_correct"] += 1
        elif sa == "correct" and sb != "correct":
            cat = "only_a"; counts["only_a"] += 1
        elif sb == "correct" and sa != "correct":
            cat = "only_b"; counts["only_b"] += 1
        elif sa == "wrong" and sb == "wrong":
            cat = "both_wrong"; counts["both_wrong"] += 1
        else:
            cat = "pending"
        disagree = (sa != sb) and (sa in ("correct","wrong") and sb in ("correct","wrong"))
        if disagree:
            counts["disagree"] += 1
        rows.append({
            "uid": uid, "question": g["question"], "gold": g["answer"],
            "a_status": sa, "a_pred": pa, "b_status": sb, "b_pred": pb,
            "cat": cat, "disagree": disagree,
        })
    counts["a_acc"] = counts["a_correct"] / counts["a_scored"] if counts["a_scored"] else 0.0
    counts["b_acc"] = counts["b_correct"] / counts["b_scored"] if counts["b_scored"] else 0.0

    return render_template_string(
        COMPARE_INDEX_TPL,
        css=BASE_CSS, runs=runs, a=a, b=b,
        rows=rows, counts=counts, status_cls=status_classes(),
    )


@app.route("/compare/<uid>")
def compare_detail(uid: str):
    runs = list_runs()
    default_a, default_b = _default_compare_runs()
    a = request.args.get("a") or default_a
    b = request.args.get("b") or default_b
    if a not in runs or b not in runs:
        return redirect(url_for("compare_index"))

    gold, _ = load_run(a)
    g = gold.get(uid)
    if not g:
        abort(404)

    side_a = _side(a, uid, g); side_a["label"] = "A"
    side_b = _side(b, uid, g); side_b["label"] = "B"

    src_files = [s.strip() for s in g["source_files"].splitlines() if s.strip()]
    src_docs = [s.strip() for s in g["source_docs"].splitlines() if s.strip()]
    sf = []
    for i, fn in enumerate(src_files):
        p = CORPUS / fn
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        pdf_name = fn.replace(".txt", ".pdf")
        pdf_path = PDFS / pdf_name
        pdf_exists = pdf_path.exists()
        fraser = src_docs[i] if i < len(src_docs) else ""
        page = ""
        if "page=" in fraser:
            try:
                page = fraser.rsplit("page=", 1)[1].split("&")[0]
            except Exception:
                page = ""
        sf.append({
            "name": fn, "size_kb": p.stat().st_size / 1024, "text": text,
            "fraser_url": fraser,
            "pdf_url": url_for("pdf", filename=pdf_name) if pdf_exists else "",
            "pdf_size_mb": pdf_path.stat().st_size / 1e6 if pdf_exists else None,
            "page": page,
        })

    uids = sorted(gold.keys())
    i = uids.index(uid)
    prev_uid = uids[i - 1] if i > 0 else None
    next_uid = uids[i + 1] if i + 1 < len(uids) else None

    return render_template_string(
        COMPARE_DETAIL_TPL,
        css=BASE_CSS, uid=uid, a=a, b=b,
        question=g["question"], gold=g["answer"],
        sideA=side_a, sideB=side_b,
        source_files=sf, status_cls=status_classes(),
        prev_uid=prev_uid, next_uid=next_uid,
    )


# ---------------------------------------------------------------------------
# Hermes trajectory viewer
# ---------------------------------------------------------------------------
HERMES_PROFILE = Path.home() / ".hermes" / "profiles" / "officeqa-iter-v2"
HERMES_SESSIONS = HERMES_PROFILE / "sessions"
FULL_EVAL_RUN_DIR = ROOT / "baselines" / "hermes_iter" / "runs" / "full_eval"
FULL_SPLIT_PATH = ROOT / "baselines" / "hermes_iter" / "splits" / "full.jsonl"

_hermes_index_cache: dict | None = None


def _build_hermes_index() -> dict[str, Path]:
    """Map uid -> most-recent matching Hermes session path.

    Matches by searching for the question text inside the first user message.
    Picks the session with the latest start time.
    """
    global _hermes_index_cache
    if _hermes_index_cache is not None:
        return _hermes_index_cache

    # 1) load uid -> question text
    if not FULL_SPLIT_PATH.exists():
        _hermes_index_cache = {}
        return _hermes_index_cache
    rows = [json.loads(l) for l in FULL_SPLIT_PATH.read_text().splitlines() if l.strip()]
    q_by_uid = {r["uid"]: r["question"] for r in rows}

    # 2) walk sessions, collect (uid -> [(started_at, path), ...])
    candidates: dict[str, list[tuple[float, Path]]] = {uid: [] for uid in q_by_uid}
    for p in HERMES_SESSIONS.glob("*.json"):
        try:
            s = json.load(open(p))
        except Exception:
            continue
        started = s.get("session_start") or s.get("started_at") or 0
        if isinstance(started, str):
            try:
                from datetime import datetime
                started = datetime.fromisoformat(started.rstrip("Z")).timestamp()
            except Exception:
                started = 0
        # Search first user message for any uid's question
        for m in (s.get("messages") or [])[:5]:
            if not isinstance(m, dict) or m.get("role") != "user":
                continue
            c = m.get("content")
            if not isinstance(c, str):
                continue
            for uid, q in q_by_uid.items():
                # Match first 80 chars of question
                if q and q[:80] in c:
                    candidates[uid].append((started, p))
            break  # first user msg only

    idx = {uid: max(lst)[1] for uid, lst in candidates.items() if lst}
    _hermes_index_cache = idx
    return idx


def _load_full_eval_pred(uid: str) -> dict | None:
    p = FULL_EVAL_RUN_DIR / "preds" / f"{uid}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _load_full_split() -> dict[str, dict]:
    if not FULL_SPLIT_PATH.exists():
        return {}
    return {r["uid"]: r for r in (json.loads(l) for l in FULL_SPLIT_PATH.read_text().splitlines() if l.strip())}


def _hermes_message_blocks(session: dict) -> list[dict]:
    """Flatten Hermes messages into render-ready blocks."""
    out = []
    for i, m in enumerate(session.get("messages") or []):
        if not isinstance(m, dict):
            continue
        role = m.get("role", "?")
        content = m.get("content")
        tool_calls = m.get("tool_calls") or []
        tool_name = m.get("tool_name") or ""

        # User / assistant text content
        if isinstance(content, str) and content.strip() and role != "tool":
            out.append({"kind": "text", "role": role, "text": content, "tool_name": tool_name})

        # Assistant tool calls
        for tc in tool_calls:
            fn = (tc.get("function") or {})
            name = fn.get("name", "?")
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except Exception:
                args = fn.get("arguments")
            out.append({"kind": "tool_call", "role": role, "name": name, "args": args, "id": tc.get("id", "")})

        # Tool results (role == 'tool')
        if role == "tool":
            txt = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
            out.append({"kind": "tool_result", "name": tool_name, "text": txt})
    return out


HERMES_CSS = """
.h-block { border-left: 3px solid #e5e7eb; padding: 8px 0 8px 12px; margin: 12px 0; }
.h-block.user        { border-color: #6366f1; background: #eef2ff; padding: 12px; border-radius: 0 6px 6px 0; }
.h-block.assistant   { border-color: #60a5fa; }
.h-block.tool_call   { border-color: #f59e0b; }
.h-block.tool_result { border-color: #10b981; }
.h-block .role-tag { font-size: 11px; text-transform: uppercase; color: #6b7280; letter-spacing: .05em; margin-bottom: 6px; }
.h-block .body { white-space: pre-wrap; font-size: 13px; line-height: 1.5; color: #1f2937; word-wrap: break-word; }
.h-block.user .body { font-weight: 500; color: #111; }
.h-block .body mark { background: #fef08a; padding: 1px 4px; border-radius: 3px; }
.tool-name { font-family: ui-monospace, monospace; font-size: 12px; background: #fef3c7; padding: 2px 6px; border-radius: 4px; color: #92400e; font-weight: 600; }
.tool-args { font-family: ui-monospace, monospace; font-size: 11px; background: #fafafa; padding: 8px; border-radius: 4px; margin-top: 4px; max-height: 200px; overflow: auto; white-space: pre-wrap; }
.tool-result-body { font-family: ui-monospace, monospace; font-size: 11px; background: #ecfdf5; padding: 8px; border-radius: 4px; max-height: 400px; overflow: auto; white-space: pre-wrap; word-break: break-all; }
.tool-result-head { font-size: 11px; color: #047857; font-weight: 600; margin-bottom: 4px; }
.error-list { display: grid; grid-template-columns: max-content 1fr max-content 1fr; gap: 4px 12px; font-size: 13px; }
.error-list code { font-family: ui-monospace, monospace; padding: 1px 6px; background: #fef2f2; color: #991b1b; border-radius: 3px; }
.error-list code.gold { background: #f0fdf4; color: #166534; }
"""


HERMES_INDEX_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>Hermes trajectories — Pro wrong</title>
<style>{{ css|safe }}{{ hcss|safe }}</style></head><body>
<header>
  <h1>Hermes trajectories — Pro split, wrong instances ({{ rows|length }})</h1>
  <div class="meta">profile: officeqa-iter-v2 · run: full_eval · <a href="{{ url_for('hermes_index_full') }}" style="color:#34d399">all 246 →</a> · <a href="{{ url_for('index') }}" style="color:#9ca3af">Claude Code runs →</a></div>
</header>
<div class="container">
  <div class="filters">
    <span style="color:#6b7280;font-size:12px;">filter:</span>
    <span class="chip active" data-filt="all">all ({{ rows|length }})</span>
    <span class="chip" data-filt="tiny">tiny drift &lt;1% ({{ cats.tiny }})</span>
    <span class="chip" data-filt="mod">moderate 1-10% ({{ cats.mod }})</span>
    <span class="chip" data-filt="large">large &gt;10% ({{ cats.large }})</span>
    <span class="chip" data-filt="list">list ({{ cats.list }})</span>
    <span class="chip" data-filt="test">cohort=test ({{ cats.test }})</span>
    <span class="chip" data-filt="seen">cohort=seen ({{ cats.seen }})</span>
  </div>

  <table id="rows">
    <thead><tr>
      <th>uid</th><th>cohort</th><th>category</th><th>gold</th><th>predicted</th><th>n_src</th><th>elapsed</th><th>n_msgs</th><th>tool_calls</th>
    </tr></thead>
    <tbody>
    {% for r in rows %}
      <tr data-cat="{{ r.cat }}" data-cohort="{{ r.cohort }}">
        <td><a href="{{ url_for('hermes_detail', uid=r.uid) }}">{{ r.uid }}</a></td>
        <td>{{ r.cohort }}</td>
        <td>{{ r.cat }}</td>
        <td><code style="background:#f0fdf4;color:#166534;padding:1px 4px;border-radius:3px;">{{ r.gold }}</code></td>
        <td><code style="background:#fef2f2;color:#991b1b;padding:1px 4px;border-radius:3px;">{{ r.pred }}</code></td>
        <td>{{ r.n_src }}</td>
        <td>{{ '%.0f'|format(r.elapsed) }}s</td>
        <td>{{ r.n_msgs }}</td>
        <td style="font-size:12px;">{{ r.tools }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
<script>
  const chips=document.querySelectorAll('.chip'); const rows=document.querySelectorAll('#rows tbody tr');
  chips.forEach(c=>c.addEventListener('click',()=>{
    chips.forEach(x=>x.classList.remove('active')); c.classList.add('active');
    const f=c.dataset.filt;
    rows.forEach(r=>{
      let show;
      if (f==='all') show=true;
      else if (f==='test'||f==='seen') show = r.dataset.cohort===f;
      else show = r.dataset.cat===f;
      r.style.display = show?'':'none';
    });
  }));
</script>
</body></html>
"""


HERMES_DETAIL_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>{{ uid }} — Hermes trajectory</title>
<style>{{ css|safe }}{{ hcss|safe }}</style></head><body>
<header>
  <h1>{{ uid }} — Hermes trajectory ({% if correct %}<span class="badge ok">CORRECT</span>{% else %}<span class="badge bad">WRONG</span>{% endif %})</h1>
  <div class="meta">
    <a href="{{ url_for('hermes_index_full') }}" style="color:#9ca3af">← all 246</a>
    · <a href="{{ url_for('hermes_index_pro_wrong') }}" style="color:#9ca3af">Pro-wrong</a>
    · session: <code>{{ session_id }}</code>
    · {{ n_messages }} messages · {{ n_tool_calls }} tool calls · {{ '%.0f'|format(elapsed) }}s
  </div>
</header>
<div class="container">
  <div class="card">
    <h2>question</h2>
    <div class="q-text">{{ question }}</div>
    <div style="margin-top:12px" class="error-list">
      <span class="label">gold</span><span><code class="gold">{{ gold }}</code></span>
      <span class="label">predicted</span><span><code>{{ predicted or '(none)' }}</code></span>
      <span class="label">cohort</span><span>{{ cohort }}</span>
      <span class="label">tool-calls</span><span>{{ tool_usage }}</span>
    </div>
  </div>

  <div class="card">
    <h2>trajectory · {{ blocks|length }} blocks</h2>
    {% for b in blocks %}
      {% if b.kind == 'text' %}
        <div class="h-block {{ b.role }}">
          <div class="role-tag">{{ b.role }}</div>
          <div class="body">{{ b.body|safe }}</div>
        </div>
      {% elif b.kind == 'tool_call' %}
        <div class="h-block tool_call">
          <div class="role-tag">tool_call <span class="tool-name">{{ b.name }}</span></div>
          <div class="tool-args">{{ b.args_json }}</div>
        </div>
      {% elif b.kind == 'tool_result' %}
        <div class="h-block tool_result">
          <div class="tool-result-head">{{ b.name or 'tool' }} result · {{ b.size }} chars</div>
          <div class="tool-result-body">{{ b.text }}</div>
        </div>
      {% endif %}
    {% endfor %}
  </div>
</div>
</body></html>
"""


def _render_text_with_highlight(text: str) -> str:
    safe = html.escape(text)
    return safe.replace(
        "&lt;FINAL_ANSWER&gt;",
        "<mark>&lt;FINAL_ANSWER&gt;",
    ).replace(
        "&lt;/FINAL_ANSWER&gt;",
        "&lt;/FINAL_ANSWER&gt;</mark>",
    )


def _classify_error(gold: str, pred: str) -> str:
    g, p = (gold or "").strip(), (pred or "").strip()
    if g.startswith("[") or p.startswith("["):
        return "list"
    def to_f(s):
        s = s.strip().strip("%").replace(",", "")
        try: return float(s)
        except: return None
    gf, pf = to_f(g), to_f(p)
    if gf is None or pf is None:
        return "other"
    if gf == 0:
        return "tiny" if abs(pf - gf) < 0.01 else "large"
    rel = abs(pf - gf) / abs(gf) * 100
    if rel < 1: return "tiny"
    if rel < 10: return "mod"
    return "large"


HERMES_FULL_TPL = """
<!doctype html><html><head>
<meta charset="utf-8"><title>Hermes — full eval (all 246)</title>
<style>{{ css|safe }}{{ hcss|safe }}</style></head><body>
<header>
  <h1>Hermes — full_eval · all 246 questions
    <span class="badge ok">{{ counts.correct }} correct</span>
    <span class="badge bad">{{ counts.wrong }} wrong</span>
  </h1>
  <div class="meta">
    profile: officeqa-iter-v2 · overall {{ '%.1f'|format(100*counts.correct/counts.total) }}% ·
    <a href="{{ url_for('hermes_index_pro_wrong') }}" style="color:#fbbf24">Pro wrong only →</a> ·
    <a href="{{ url_for('index') }}" style="color:#9ca3af">Claude Code runs →</a>
  </div>
</header>
<div class="container">
  <div class="summary">
    <span>Pro / hard: <b>{{ counts.hard_correct }}/{{ counts.hard_total }} = {{ '%.1f'|format(100*counts.hard_correct/counts.hard_total) }}%</b></span>
    <span>Easy: <b>{{ counts.easy_correct }}/{{ counts.easy_total }} = {{ '%.1f'|format(100*counts.easy_correct/counts.easy_total) }}%</b></span>
    <span>test cohort: <b>{{ counts.test_correct }}/{{ counts.test_total }}</b></span>
    <span>easy cohort: <b>{{ counts.easycoh_correct }}/{{ counts.easycoh_total }}</b></span>
    <span>seen cohort: <b>{{ counts.seen_correct }}/{{ counts.seen_total }}</b></span>
  </div>

  <div class="filters">
    <span style="color:#6b7280;font-size:12px;">outcome:</span>
    <span class="chip active" data-out="all">all ({{ counts.total }})</span>
    <span class="chip" data-out="correct">correct ({{ counts.correct }})</span>
    <span class="chip" data-out="wrong">wrong ({{ counts.wrong }})</span>
    <span style="color:#6b7280;font-size:12px;margin-left:16px;">cohort:</span>
    <span class="chip active" data-coh="all">all</span>
    <span class="chip" data-coh="test">test ({{ counts.test_total }})</span>
    <span class="chip" data-coh="seen">seen ({{ counts.seen_total }})</span>
    <span class="chip" data-coh="easy">easy ({{ counts.easycoh_total }})</span>
    <span style="color:#6b7280;font-size:12px;margin-left:16px;">difficulty:</span>
    <span class="chip active" data-diff="all">all</span>
    <span class="chip" data-diff="hard">hard / Pro ({{ counts.hard_total }})</span>
    <span class="chip" data-diff="easy">easy ({{ counts.easy_total }})</span>
  </div>

  <table id="rows">
    <thead><tr>
      <th>uid</th><th>outcome</th><th>diff</th><th>cohort</th><th>question</th>
      <th>gold</th><th>predicted</th><th>elapsed</th>
    </tr></thead>
    <tbody>
    {% for r in rows %}
      <tr data-out="{{ 'correct' if r.correct else 'wrong' }}" data-coh="{{ r.cohort }}" data-diff="{{ r.difficulty }}">
        <td><a href="{{ url_for('hermes_detail', uid=r.uid) }}">{{ r.uid }}</a></td>
        <td><span class="badge {{ 'ok' if r.correct else 'bad' }}">{{ 'OK' if r.correct else 'X' }}</span></td>
        <td>{{ r.difficulty }}</td>
        <td>{{ r.cohort }}</td>
        <td class="q" title="{{ r.question }}">{{ r.question }}</td>
        <td><code style="background:#f0fdf4;color:#166534;padding:1px 4px;border-radius:3px;font-size:12px">{{ r.gold }}</code></td>
        <td><code style="background:{{ '#f0fdf4' if r.correct else '#fef2f2' }};color:{{ '#166534' if r.correct else '#991b1b' }};padding:1px 4px;border-radius:3px;font-size:12px">{{ r.pred or '(none)' }}</code></td>
        <td>{{ '%.0f'|format(r.elapsed) }}s</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
<script>
  function applyFilters() {
    const out = document.querySelector('[data-out].active').dataset.out;
    const coh = document.querySelector('[data-coh].active').dataset.coh;
    const diff= document.querySelector('[data-diff].active').dataset.diff;
    document.querySelectorAll('#rows tbody tr').forEach(r=>{
      const okOut  = out==='all'  || r.dataset.out===out;
      const okCoh  = coh==='all'  || r.dataset.coh===coh;
      const okDiff = diff==='all' || r.dataset.diff===diff;
      r.style.display = (okOut && okCoh && okDiff) ? '' : 'none';
    });
  }
  ['out','coh','diff'].forEach(group=>{
    document.querySelectorAll(`[data-${group}]`).forEach(c=>c.addEventListener('click',()=>{
      document.querySelectorAll(`[data-${group}]`).forEach(x=>x.classList.remove('active'));
      c.classList.add('active');
      applyFilters();
    }));
  });
</script>
</body></html>
"""


@app.route("/hermes/full")
def hermes_index_full():
    """Index of all 246 full_eval questions for the evolved Hermes agent."""
    sys.path.insert(0, str(ROOT / "baselines"))
    from reward import extract_final_answer, score_answer  # noqa: E402

    split = _load_full_split()
    rows = []
    counts = {
        "total": 0, "correct": 0, "wrong": 0,
        "hard_total": 0, "hard_correct": 0,
        "easy_total": 0, "easy_correct": 0,
        "test_total": 0, "test_correct": 0,
        "seen_total": 0, "seen_correct": 0,
        "easycoh_total": 0, "easycoh_correct": 0,
    }
    for uid, meta in sorted(split.items()):
        rec = _load_full_eval_pred(uid)
        if not rec:
            continue
        raw = rec.get("raw_response") or ""
        try: ext = extract_final_answer(raw)
        except Exception: ext = ""
        try: sc = score_answer(meta["gold_answer"], ext) if ext else 0.0
        except Exception: sc = 0.0
        correct = sc >= 1.0
        counts["total"] += 1
        counts["correct" if correct else "wrong"] += 1
        diff = meta.get("difficulty", "")
        coh = meta.get("cohort", "")
        if diff == "hard":
            counts["hard_total"] += 1
            if correct: counts["hard_correct"] += 1
        elif diff == "easy":
            counts["easy_total"] += 1
            if correct: counts["easy_correct"] += 1
        if coh == "test":
            counts["test_total"] += 1
            if correct: counts["test_correct"] += 1
        elif coh == "seen":
            counts["seen_total"] += 1
            if correct: counts["seen_correct"] += 1
        elif coh == "easy":
            counts["easycoh_total"] += 1
            if correct: counts["easycoh_correct"] += 1
        rows.append({
            "uid": uid,
            "correct": correct,
            "difficulty": diff,
            "cohort": coh,
            "question": meta["question"],
            "gold": meta["gold_answer"],
            "pred": ext,
            "elapsed": rec.get("elapsed_sec", 0),
        })

    return render_template_string(
        HERMES_FULL_TPL,
        css=BASE_CSS, hcss=HERMES_CSS,
        rows=rows, counts=counts,
    )


@app.route("/hermes/")
def hermes_index_pro_wrong():
    """Index of Pro-split wrong instances from the full_eval run."""
    sys.path.insert(0, str(ROOT / "baselines"))
    from reward import extract_final_answer, score_answer  # noqa: E402

    split = _load_full_split()
    idx_sess = _build_hermes_index()
    rows = []
    cats = {"tiny": 0, "mod": 0, "large": 0, "list": 0, "test": 0, "seen": 0}

    for uid, meta in sorted(split.items()):
        if meta.get("difficulty") != "hard":
            continue
        rec = _load_full_eval_pred(uid)
        if not rec:
            continue
        raw = rec.get("raw_response") or ""
        try: ext = extract_final_answer(raw)
        except Exception: ext = ""
        try: sc = score_answer(meta["gold_answer"], ext) if ext else 0.0
        except Exception: sc = 0.0
        if sc >= 1.0:
            continue  # only wrong

        cat = _classify_error(meta["gold_answer"], ext)
        cats[cat] = cats.get(cat, 0) + 1
        cats[meta["cohort"]] = cats.get(meta["cohort"], 0) + 1

        sess_path = idx_sess.get(uid)
        n_msgs = 0
        tools = ""
        if sess_path and sess_path.exists():
            try:
                s = json.load(open(sess_path))
                msgs = s.get("messages") or []
                n_msgs = len(msgs)
                from collections import Counter
                tc = Counter()
                for m in msgs:
                    for t in (m.get("tool_calls") or []):
                        tc[(t.get("function") or {}).get("name", "?")] += 1
                tools = ", ".join(f"{k}={v}" for k, v in tc.most_common())
            except Exception:
                pass
        rows.append({
            "uid": uid,
            "cohort": meta["cohort"],
            "gold": meta["gold_answer"],
            "pred": ext or "(none)",
            "n_src": len(meta["source_files"]),
            "elapsed": rec.get("elapsed_sec", 0),
            "n_msgs": n_msgs,
            "tools": tools,
            "cat": cat,
        })

    return render_template_string(
        HERMES_INDEX_TPL,
        css=BASE_CSS, hcss=HERMES_CSS,
        rows=rows, cats=cats,
    )


@app.route("/hermes/<uid>")
def hermes_detail(uid: str):
    sys.path.insert(0, str(ROOT / "baselines"))
    from reward import extract_final_answer, score_answer  # noqa: E402

    split = _load_full_split()
    if uid not in split:
        abort(404)
    meta = split[uid]
    rec = _load_full_eval_pred(uid) or {}
    raw = rec.get("raw_response") or ""
    try: predicted = extract_final_answer(raw)
    except Exception: predicted = ""
    try: sc = score_answer(meta["gold_answer"], predicted) if predicted else 0.0
    except Exception: sc = 0.0

    idx_sess = _build_hermes_index()
    sess_path = idx_sess.get(uid)
    blocks_rendered = []
    session_id = ""
    n_messages = 0
    n_tool_calls = 0
    tool_usage = ""
    if sess_path and sess_path.exists():
        s = json.load(open(sess_path))
        session_id = s.get("session_id", "")
        msgs = s.get("messages") or []
        n_messages = len(msgs)
        from collections import Counter
        tc = Counter()
        for m in msgs:
            for t in (m.get("tool_calls") or []):
                tc[(t.get("function") or {}).get("name", "?")] += 1
        n_tool_calls = sum(tc.values())
        tool_usage = ", ".join(f"{k}={v}" for k, v in tc.most_common())

        for b in _hermes_message_blocks(s):
            if b["kind"] == "text":
                text = b["text"]
                if len(text) > 12000:
                    text = text[:6000] + f"\n\n... [truncated {len(text)-12000} chars] ...\n\n" + text[-3000:]
                blocks_rendered.append({
                    "kind": "text",
                    "role": b["role"],
                    "body": _render_text_with_highlight(text),
                })
            elif b["kind"] == "tool_call":
                args = b["args"]
                args_json = json.dumps(args, ensure_ascii=False, indent=2) if isinstance(args, (dict, list)) else str(args)
                if len(args_json) > 4000:
                    args_json = args_json[:4000] + f"\n... [{len(args_json)-4000} chars elided] ..."
                blocks_rendered.append({
                    "kind": "tool_call",
                    "name": b["name"],
                    "args_json": args_json,
                })
            elif b["kind"] == "tool_result":
                text = b["text"] or ""
                size = len(text)
                if size > 8000:
                    text = text[:4000] + f"\n\n... [truncated {size-8000} chars] ...\n\n" + text[-2000:]
                blocks_rendered.append({
                    "kind": "tool_result",
                    "name": b["name"],
                    "text": text,
                    "size": size,
                })

    return render_template_string(
        HERMES_DETAIL_TPL,
        css=BASE_CSS, hcss=HERMES_CSS,
        uid=uid,
        question=meta["question"],
        gold=meta["gold_answer"],
        predicted=predicted,
        cohort=meta["cohort"],
        elapsed=rec.get("elapsed_sec", 0),
        correct=sc >= 1.0,
        session_id=session_id,
        n_messages=n_messages,
        n_tool_calls=n_tool_calls,
        tool_usage=tool_usage,
        blocks=blocks_rendered,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5000)
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()
    print(f"Open http://{args.host}:{args.port}/  (SSH tunnel: ssh -L {args.port}:127.0.0.1:{args.port} <vm>)")
    print(f"Hermes full_eval (all 246):   http://{args.host}:{args.port}/hermes/full")
    print(f"Pro-wrong subset only:        http://{args.host}:{args.port}/hermes/")
    app.run(host=args.host, port=args.port, debug=args.debug)

#!/usr/bin/env bash
# Auto-resuming launcher for the full Claude+Fable skill-curation loop.
# iterate_claude.py is resumable (cached answers + per-question reflect markers +
# curate markers), so each relaunch continues where the last died — handy when
# the Claude Code subscription hits a rate limit mid-run.
set -u
cd /home/azureuser/office-qa
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d= -f2)
STATE=baselines/hermes_iter/runs/fable_claude_loop_full
for attempt in $(seq 1 30); do
  echo "=== launch attempt $attempt ($(date -u +%H:%M:%S)) ==="
  .venv/bin/python baselines/hermes_iter/iterate_claude.py \
    --state-dir "$STATE" \
    --train-split baselines/hermes_iter/splits_parsed_md_nooracle/train.jsonl \
    --eval-split  baselines/hermes_iter/splits_parsed_md_nooracle/eval.jsonl \
    --max-iters 5 --patience 3 \
    --answer-concurrency 4 \
    && { echo "=== completed cleanly (attempt $attempt) ==="; break; }
  echo "=== attempt $attempt exited non-zero; resuming in 240s ==="
  sleep 240
done

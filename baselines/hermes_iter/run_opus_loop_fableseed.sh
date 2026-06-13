#!/usr/bin/env bash
# Auto-resuming launcher: Claude Code skill-curation loop with claude-opus-4-8,
# SEEDED from the 28 skills Fable 5 wrote before it was pulled. Resumable
# (cached answers + reflect/curate markers + one-time seed marker).
set -u
cd /home/azureuser/office-qa
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d= -f2)
STATE=baselines/hermes_iter/runs/opus48_claude_loop_fableseed
SEED=baselines/hermes_iter/runs/fable_claude_loop_full/project/.claude/skills
for attempt in $(seq 1 30); do
  echo "=== launch attempt $attempt ($(date -u +%H:%M:%S)) ==="
  .venv/bin/python baselines/hermes_iter/iterate_claude.py \
    --state-dir "$STATE" \
    --train-split baselines/hermes_iter/splits_parsed_md_nooracle/train.jsonl \
    --eval-split  baselines/hermes_iter/splits_parsed_md_nooracle/eval.jsonl \
    --model-args "--model claude-opus-4-8" \
    --seed-skills "$SEED" \
    --max-iters 5 --patience 3 \
    --answer-concurrency 4 \
    && { echo "=== completed cleanly (attempt $attempt) ==="; break; }
  echo "=== attempt $attempt exited non-zero; resuming in 240s ==="
  sleep 240
done

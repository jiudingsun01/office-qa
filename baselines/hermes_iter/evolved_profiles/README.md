# Evolved profiles (meta-optimization output)

The actual learned artifacts produced by `iterate.py --reflect` — i.e. the
"trained model" for each backend. Each subdir holds only the **evolved**
OfficeQA/Treasury-Bulletin pieces, not the ~87 generic base Hermes skills:

```
<profile>/
  MEMORY.md        # durable cross-session facts the agent wrote
  skills/<name>/   # procedural SKILL.md files the agent authored (officeqa/treasury-tagged)
```

| profile | backend | evolved skills | memory entries | final test |
|---|---|---|---|---|
| `officeqa-iter-v2` | gpt-5.5 | 36 | 21 | 24/28 = 0.857 (PDF corpus, run `iter02`) |
| `officeqa-iter-opus48` | claude-opus-4-8 | 48 | 8 | 18/28 = 0.643 (parsed-md+pdf, run `opus48_full_metaopt`) |

> **Gating note.** Some SKILL.md files contain worked examples with concrete
> Treasury-Bulletin values. Like the per-question trajectories, treat these as
> derived from the gated OfficeQA corpus (see `../EXPERIMENTS.md` §9).

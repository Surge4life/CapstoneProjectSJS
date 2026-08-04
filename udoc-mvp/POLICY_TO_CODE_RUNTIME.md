# Policy-to-Code → EVA runtime matrix

**Updated:** 2026-08-04 · Core commit includes `9311201a`

## Pipeline

```
Upload legislation (PDF/DOCX/TXT)
        ↓
extract_rules()  — transparent heuristics → candidate PolicyRule rows
        ↓
Human review / PATCH rules (enable, severity, threshold)
        ↓
Activate pack  (or COB submit → approve)
        ↓
pe.invalidate()  — hot-reload epoch
        ↓
EVA decision time: evaluate(Evidence) + policy_engine.apply(active rules)
        ↓
Adjusted decision + fired findings (non-bypassable path)
```

## Live endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/policy/upload` | Compile draft rules from file |
| GET | `/policy/packs` | List packs |
| GET | `/policy/packs/{id}` | Pack + rules |
| PATCH | `/policy/rules/{id}` | Edit enable/severity/threshold |
| POST | `/policy/packs/{id}/activate` | Enforce on next EVA |
| GET | `/policy/active` | **Fixed** — active packs + rule list + by_kind |
| POST | `/policy/test` | Single scenario dry-run (EVA+policy) |
| POST | `/policy/runtime-matrix` | **New** — fair/biased/high/sov dry-run matrix |
| POST | `/decisions/batch` | Persist matrix (writes Decision rows) |
| POST | `/policy/hot-reload` | Clear rule cache |

## Runtime matrix body

```json
{ "model_id": "model-001", "options": ["fair", "biased", "high", "sov"] }
```

Returns `results[]` with `decision`, `fired`, `policy_enforced`, plus smoke `gate`.

## Demo seed

Pack **UDOC Demo · POPIA + Fairness** (5 rules) seeds at Core startup. `/udoc/demo/ready` auto-heals model-001 if suspended.

## Honesty

Heuristic compile is transparent, not a legal LLM. Human primacy on activation. Neon-light file size cap on upload.

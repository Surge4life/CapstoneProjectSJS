# Chapter 15 — Model Lifecycle

## AI Models in G.O.D.S Intelligence

G.O.D.S Intelligence uses two types of AI model:

1. **Embedding models** — convert text to vector representations for retrieval
2. **Synthesis models** — generate natural language responses from retrieved evidence

Both have a defined lifecycle within the governance framework.

---

## Embedding Model Lifecycle

### Selection

The embedding model is selected at deployment time. Selection criteria:
- Semantic accuracy on the corpus domain (evaluated against a test query set)
- Latency (must not exceed the intelligence query budget)
- Licence (must be compatible with institutional use)
- Air-gap capability (must be runnable locally for air-gap deployments)

**Approved embedding models:**

| Model | Dimensions | Use Case | Air-Gap? |
|-------|-----------|---------|---------|
| OpenAI `text-embedding-ada-002` | 1536 | Cloud deployments | No |
| `all-MiniLM-L6-v2` (Sentence Transformers) | 384 | Air-gap and cloud | Yes |
| `e5-large-v2` (Microsoft) | 1024 | Higher accuracy, air-gap | Yes |

### Deployment

The embedding model is configured in `platform-core/app/core/config.py`:
```python
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS: int = 384
```

### Migration

Changing the embedding model requires re-embedding the entire corpus. This is because vectors from different models are not comparable.

```bash
# Migration procedure
gods-cli corpus re-embed \
  --from-model "all-MiniLM-L6-v2" \
  --to-model "e5-large-v2" \
  --verify   # Verify a sample of results before committing
```

Re-embedding is an audited operation. The audit record includes which model was used before and after, and the migration timestamp.

---

## Synthesis Model Lifecycle

### Selection

The synthesis model produces the natural language response from retrieved evidence. Selection criteria:
- Instruction-following quality (does it stay within the evidence bounds?)
- Constitutional compliance (does it refuse appropriately?)
- Latency and cost
- Licence and data governance
- Air-gap capability

**Approved synthesis models:**

| Model | Use Case | Air-Gap? |
|-------|---------|---------|
| GPT-4o-mini (OpenAI) | Cloud deployments, cost-effective | No |
| GPT-4o (OpenAI) | High-stakes queries requiring precision | No |
| Llama 3 70B (Meta, quantised) | Air-gap deployments | Yes |
| Mistral 7B Instruct | Air-gap, lightweight | Yes |

### Governance Evaluation

Before deploying a new synthesis model, it must pass governance evaluation:

1. **Constitutional compliance test:** A test set of 50 queries that should trigger each of the 10 constitutional limits. The model must refuse all 50 appropriately.
2. **Attribution accuracy test:** A test set of 30 queries where the correct sources are known. The model must cite the correct sources in ≥ 90% of responses.
3. **Evidence boundary test:** A test set of 20 queries where the evidence does not support a complete answer. The model must declare `INSUFFICIENT` or LOW confidence in all 20.

A model that fails any of these evaluations is not used in production.

### Deprecation

When a synthesis model is deprecated (e.g., the API is discontinued):
1. A replacement model is selected and evaluated
2. A migration is planned with a cut-over date
3. Post-cut-over, old model responses are still in the audit record (they are permanent)
4. Future queries use the new model
5. The model change is recorded in the platform configuration audit trail

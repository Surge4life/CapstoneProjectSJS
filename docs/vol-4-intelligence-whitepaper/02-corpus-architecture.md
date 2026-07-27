# Chapter 02 — Internal Corpus Architecture

## The Corpus as Infrastructure

The G.O.D.S Intelligence corpus is not a folder of documents. It is a governed, versioned, access-controlled knowledge infrastructure. Every document that enters the corpus is tracked, tiered, audited, and made retrievable in a structured way.

---

## Corpus Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Corpus Interface                      │
│         (upload, query, manage via API)                  │
├─────────────────────────────────────────────────────────┤
│                  Governance Layer                        │
│   Tier enforcement · Access control · Upload audit       │
├──────────────────────────┬──────────────────────────────┤
│   Metadata Store         │    Vector + Text Index        │
│   (PostgreSQL)           │    (OpenSearch)               │
│   KnowledgeDoc table     │    k-NN + BM25               │
│   Tier, dates, owner     │    Embeddings + full text     │
├──────────────────────────┴──────────────────────────────┤
│                   Object Storage                         │
│   (S3-compatible) — original files stored immutably      │
└─────────────────────────────────────────────────────────┘
```

---

## Document Storage Model

Every document in the corpus has three representations:

1. **Original file** — stored immutably in object storage (S3-compatible). Never modified after upload.
2. **Metadata record** — `KnowledgeDoc` row in PostgreSQL. Tracks tier, owner, version, access counts.
3. **Chunks + embeddings** — one or more chunk records in OpenSearch. These are the retrievable units.

If a document is updated, a new version is created (new file, new chunks, new metadata record). The old version is retained and marked as `superseded_by: new_doc_id`.

---

## Corpus Namespaces

The corpus is divided into namespaces:

| Namespace | Access | Contents |
|-----------|--------|----------|
| `platform` | Internal (all authenticated users) | G.O.D.S operational knowledge, policy documents, governance guidance |
| `client_{tenant_id}` | Tenant-specific | Client's own knowledge base |
| `shared_{pack_id}` | Licensed tenants | Shared knowledge packs (licensed from platform corpus) |

Retrieval is always namespace-scoped. A query against `client_abc` cannot retrieve documents from `client_xyz` or `platform` (unless the tenant has licensed platform corpus access).

---

## Index Architecture

The OpenSearch index for each corpus namespace:

```json
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 512
    }
  },
  "mappings": {
    "properties": {
      "chunk_id": { "type": "keyword" },
      "doc_id": { "type": "keyword" },
      "doc_title": { "type": "text" },
      "doc_tier": { "type": "integer" },
      "text": { "type": "text", "analyzer": "english" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
          "name": "hnsw",
          "space_type": "cosine",
          "engine": "nmslib"
        }
      },
      "chunk_index": { "type": "integer" },
      "created_at": { "type": "date" }
    }
  }
}
```

---

## Corpus Health Metrics

The corpus health dashboard (in the Intelligence section of `platform-web`) shows:

| Metric | Description | Alert Threshold |
|--------|-------------|----------------|
| Total documents | Count by tier | — |
| Indexing lag | Time from upload to searchable | > 5 minutes |
| Average tier | Weighted average tier of corpus | < 2.0 (too much low-tier content) |
| Coverage gaps | Query categories with < 3 relevant results | Any gap |
| Outdated documents | Documents where a newer version exists | > 10% of corpus |
| Query hit rate | % of queries with confidence > 0.60 | < 70% |

Low query hit rate means the corpus doesn't contain enough relevant content. The recommended action is to audit recent queries with `INSUFFICIENT_EVIDENCE` outcomes and identify what content is missing.

---

## Corpus Backup

The corpus is backed up as part of the standard database backup:

- PostgreSQL `KnowledgeDoc` table: included in daily PostgreSQL backup
- OpenSearch chunks/embeddings: daily OpenSearch snapshot to object storage
- Original files: object storage versioning enabled (every version retained)

Restoration: restore PostgreSQL metadata → restore OpenSearch snapshot → re-embed any documents uploaded between the backup and the incident (using the original files from object storage).

# Chapter 08 — Client Corpora & Multi-Tenancy

## The Multi-Tenant Intelligence Architecture

Every SaaS client of the G.O.D.S ecosystem has access to their own private corpus. This corpus is:
- Completely isolated from other clients' corpora
- Completely isolated from the platform corpus (unless explicitly licensed)
- Governed by the same constitutional boundaries as the platform corpus
- Owned by the client

---

## Tenant Isolation Architecture

Isolation is enforced at three layers:

### Layer 1: Database Isolation (PostgreSQL)

Every `KnowledgeDoc` record has a `tenant_id` column. Row-Level Security (RLS) policies ensure queries from one tenant's context cannot return another tenant's documents:

```sql
CREATE POLICY tenant_isolation ON platform.knowledge_docs
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

The application sets `app.current_tenant_id` at the start of each request. All subsequent queries are automatically filtered.

### Layer 2: Search Index Isolation (OpenSearch)

Each tenant has its own OpenSearch index:
```
gods_corpus_platform       — Platform corpus (shared, licensed)
gods_corpus_{tenant_id}    — Client-specific corpus
```

The retrieval service always passes the tenant's specific index (or a combination of tenant + licensed platform index) — never the full collection of all indices.

### Layer 3: API Isolation (platform-core)

The `client_knowledge` router enforces tenant scope at the API level:

```python
@router.post("/corpus/query")
async def query_corpus(
    request: CorpusQueryRequest,
    current_user: User = Depends(get_current_user)
):
    # Always scope to the user's tenant — no override possible
    results = await client_knowledge.query(
        query=request.query,
        tenant_id=current_user.tenant_id,  # From JWT — cannot be spoofed
        include_platform=request.include_platform and tenant.has_platform_license
    )
    return results
```

There is no parameter or header that can override the tenant scope. It is derived from the authenticated user's JWT, which is signed and cannot be modified by the client.

---

## Shared Platform Knowledge

Some knowledge is valuable to all tenants. The platform corpus (owned by G.O.D.S) can be licensed to tenants:

| Knowledge Pack | Contents | Access |
|---------------|---------|--------|
| `regulatory_za` | South African legislation, regulations, case summaries | Licensed |
| `nqf_framework` | NQF level descriptions, SAQA framework | Licensed |
| `governance_standards` | G.O.D.S governance guidance, PolicyPack explanations | Included in all plans |
| `engineering_canon` | This document | Internal only |

Licensing is managed via the `tenants` router in `platform-core`. When a tenant licenses a knowledge pack:
1. A `TenantKnowledgeLicense` record is created
2. The retrieval service adds the licensed packs to the tenant's index list
3. Licensing is audited

---

## Tenant Corpus Limits

Each tenant's corpus has configurable limits:

| Limit | Default | Maximum |
|-------|---------|---------|
| Documents | 1,000 | Unlimited (enterprise) |
| Storage | 10 GB | Configurable |
| Queries per day | 10,000 | Unlimited (enterprise) |
| Embedding model | Platform default | Custom (enterprise) |
| Max file size | 50 MB | 200 MB (enterprise) |

Limits are tracked and enforced by the `client_knowledge` service. When a limit is approached (90% of quota), the tenant admin receives a notification.

---

## Data Portability

A tenant can export their entire corpus at any time:

```
POST /client-knowledge/corpus/export
→ Returns a download URL for a ZIP file containing:
  - All document metadata (JSON)
  - All original files (in their original format)
  - All chunk texts (JSON)
  - Embeddings (if the tenant wants them — large file)
```

The export is designed for portability. A tenant who leaves the G.O.D.S platform can take their corpus with them. This is both a contractual commitment and a technical guarantee.

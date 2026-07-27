# Chapter 11 — External Consultation (Optional, User-Initiated)

## What External Consultation Is

External consultation is the mechanism by which G.O.D.S Intelligence can optionally reach outside the institutional corpus to consult an external AI service. It is:

- **Optional** — off by default in every deployment
- **User-initiated** — the user must explicitly request it for each query
- **Bounded** — the external response is treated as low-confidence evidence only
- **Sanitised** — no PII or sensitive data leaves the institutional boundary
- **Audited** — every external consultation is permanently recorded

---

## When to Enable External Consultation

External consultation is appropriate when:
- The institutional corpus is intentionally narrow (focused on operational knowledge)
- Users regularly need to access general regulatory or technical information
- The institution has assessed and accepted the data governance implications

External consultation is NOT appropriate when:
- The deployment is air-gapped (by definition — no external connectivity)
- The corpus contains highly sensitive data that employees might inadvertently include in queries
- The regulatory context requires that all processing happen within the institutional boundary

---

## Configuration

External consultation is enabled per deployment in the platform configuration:

```python
class IntelligenceConfig(BaseSettings):
    external_consultation_enabled: bool = False
    external_consultation_service: str = "openai"  # openai | azure_openai | anthropic
    external_consultation_model: str = "gpt-4o-mini"
    external_consultation_max_tokens: int = 1024
    external_consultation_requires_user_confirmation: bool = True  # Cannot be False
    external_consultation_sanitise_pii: bool = True  # Cannot be False
```

The `requires_user_confirmation` and `sanitise_pii` settings cannot be disabled. These are constitutional requirements.

---

## The Sanitisation Pipeline

Before any query reaches an external service, it goes through the sanitisation pipeline:

```python
async def sanitise_query(query: str, user_id: UUID) -> tuple[str, SanitisationReport]:
    """
    Remove PII and sensitive identifiers from a query before external transmission.
    Returns the sanitised query and a report of what was removed.
    """
    report = SanitisationReport()

    # 1. Named entity recognition — remove names, places, organisations
    query = ner_anonymise(query, report)

    # 2. Pattern matching — remove ID numbers, phone numbers, emails
    query = pattern_redact(query, report)

    # 3. Institution-specific terms — remove internal system IDs, case references
    query = internal_term_redact(query, report)

    # 4. Verify — ensure no PII remains (secondary scan)
    residual_pii = scan_for_pii(query)
    if residual_pii:
        raise SanitisationFailureError(residual_pii)

    return query, report
```

The sanitisation report is stored in the audit record. If sanitisation fails, the external consultation is blocked.

---

## External Response Handling

The external response is treated as a Tier 5 source (Secondary/Contextual):
- Confidence contribution capped at 0.40
- Clearly labelled as `EXTERNAL_SOURCE` in the response
- Never presented as institutional knowledge
- Subject to the same constitutional post-check as internal sources

**User-facing presentation:**
```
[External Source — consulted on your request from GPT-4o Mini]
"According to publicly available information..."
Note: External sources are not verified by the institutional governance system 
and are provided for general context only.
```

---

## Audit Record for External Consultation

```json
{
  "query_id": "uuid",
  "external_consultation": {
    "service": "openai",
    "model": "gpt-4o-mini",
    "sanitised_query": "What are the general requirements for AI governance disclosure in South Africa?",
    "original_query_hash": "sha256:...",
    "pii_items_removed": 0,
    "response_received": true,
    "response_confidence_assigned": 0.35,
    "consultation_timestamp": "2025-01-15T10:30:00Z"
  }
}
```

The original query (before sanitisation) is never stored in the external consultation record — only its hash. This ensures that if the record were somehow accessed by a third party, the original query content (which might contain sensitive terms) is not exposed.

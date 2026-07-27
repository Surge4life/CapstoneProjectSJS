# Chapter 03 — Knowledge Ownership

## The Ownership Principle

Every document in the G.O.D.S corpus has an owner. Ownership determines who can modify, supersede, or remove the document. Ownership is non-transferable without an audit record of the transfer.

This is not a technical nicety. It is a governance requirement. When an institution's intelligence system answers a question, the institution must be able to say: "This answer came from document X, which was uploaded by person Y on date Z, who had the authority to add it to our corpus."

Without documented ownership, the corpus becomes an unaccountable accumulation of content. With documented ownership, every claim is traceable to a responsible party.

---

## Ownership Layers

### Platform Ownership (G.O.D.S)

Documents in the `platform` namespace are owned by G.O.D.S Holdings (Pty) Ltd (proposed). These are:
- The Engineering Canon itself (referenced as corpus documents)
- Regulatory summaries
- Governance guidance documents
- Standard policy templates

Platform documents can only be uploaded by users with `corpus_admin` role. They are available to all tenants who have licensed platform corpus access.

### Tenant Ownership

Documents in a `client_{tenant_id}` namespace are owned by the tenant organisation. They are uploaded by tenant users with appropriate corpus permissions (`corpus_manager`, `corpus_editor`, `corpus_contributor` depending on tier).

The tenant owns this content. G.O.D.S has no right to use it for any purpose other than serving intelligence queries for that tenant. This is a contractual obligation and a technical guarantee (namespace isolation).

### Individual Contributor Attribution

Within tenant ownership, individual contribution is tracked:
- `uploaded_by: uuid` — who uploaded the document
- `approved_by: uuid` — who approved Tier 1/2 documents
- `updated_by: uuid` — who last updated the document

This attribution is permanent. Even if the individual's account is deleted, the attribution record remains (the user record is soft-deleted; the document attribution references the user UUID which still exists in the database).

---

## What Ownership Means in Practice

### Right to Update

The document owner (by role) can upload a new version. The previous version is marked `superseded` but never deleted.

### Right to Supersede

A higher-tier document can supersede a lower-tier document on the same topic. This is not automatic — a compliance officer must explicitly mark the relationship. This prevents accidental supersession and maintains the evidence hierarchy.

### Right to Archive

Tenant document owners can archive a document (mark it as `archived: true`). Archived documents are excluded from retrieval but retained in the corpus. Archiving is audited. Permanent deletion is not available — this is the immutability commitment applied to corpus content.

---

## Copyright and Intellectual Property

Every document in the corpus must have a declared copyright status:

| Status | Meaning |
|--------|---------|
| `institution_owned` | Created by the institution, full rights |
| `licensed` | Licensed from a third party, usage terms on file |
| `public_domain` | Public domain (Creative Commons Zero or equivalent) |
| `fair_use` | Used under fair use / fair dealing, legal basis documented |
| `government_publication` | Government publications (often public but jurisdiction-specific) |

Documents with `licensed` status must have the licence reference on file. The system does not prevent uploading licensed material — but it records the declared status, making the institution responsible for accuracy.

A document with incorrect copyright status is an institutional liability, not a G.O.D.S liability. The system records what the uploader declared; it cannot verify copyright independently.

---

## Copyright Strategy for Intelligence Outputs

When G.O.D.S Intelligence synthesises a response from corpus documents, the copyright of the response depends on:

1. **Verbatim quotation:** Copyright belongs to the original source. Always cite and attribute.
2. **Paraphrase:** Copyright is more complex — G.O.D.S Intelligence always cites the source it paraphrased, shifting the copyright analysis to the institution.
3. **Original synthesis:** If the response is a genuinely novel synthesis of multiple sources, the institution may have a copyright claim.

The G.O.D.S Intelligence system does not make copyright determinations. It cites sources. The institution's legal team determines copyright for their specific use of outputs.

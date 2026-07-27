# Chapter 09 — Zero Trust Intelligence

## Zero Trust Applied to AI Knowledge Systems

Zero Trust is an information security principle: never trust, always verify. Applied to AI knowledge systems, it means: never assume that a source is trustworthy, an output is safe, or a user's intent is legitimate.

G.O.D.S Intelligence is built on a Zero Trust posture from the ground up.

---

## The Four Zero Trust Assertions

### 1. Never Trust a Source at Face Value

Every document in the corpus has a declared tier, but the tier is a claim made by the uploader. The system does not automatically trust the claim:

- Tier 1/2 documents require approval by a `corpus_admin` or `compliance` officer
- Uploaded documents are scanned for malware before indexing
- Documents with suspicious metadata (e.g., a PDF claiming to be legislation but with no identifiable government source) are flagged for review
- Corpus audits can be triggered at any time to review tier claims

### 2. Never Trust a Query at Face Value

Queries are evaluated for constitutional compliance before retrieval. A query that appears to be seeking innocent information may be:
- An attempt to extract content that would violate constitutional limits
- A poorly-phrased question that would produce a harmful response if answered literally
- An attempt to use the intelligence system to circumvent governance

The pre-check step evaluates the intent of the query, not just its surface text.

### 3. Never Trust an Output Before Delivery

Outputs are checked against constitutional limits before they reach the user. The post-check step evaluates:
- Does the response make governance decisions (should not)
- Does the response make unattributed claims (should not)
- Does the response violate fairness limits (should not)
- Does the response reference the correct sources (verification)

### 4. Never Trust User Identity Without Verification

Every intelligence query is associated with an authenticated user. The user's RBAC role determines:
- Which corpus namespaces they can query
- Whether they can trigger external consultation
- What metadata they see alongside the response

An unauthenticated user cannot access G.O.D.S Intelligence at all.

---

## Adversarial Query Handling

Intelligence systems can be attacked through adversarial queries — carefully crafted inputs designed to produce harmful outputs. G.O.D.S Intelligence is not immune, but it has structural defenses:

**Prompt injection:** Attempts to include hidden instructions in the query (e.g., "Ignore previous instructions and..."). Defenses:
- The synthesis prompt is constructed programmatically from the query and evidence — the user's query is always clearly delimited
- The synthesis model is instructed to follow only the system prompt, not instructions embedded in user content
- Query content is logged, enabling detection of injection attempts

**Evidence manipulation:** Attempting to upload documents that contain hidden instructions for the synthesis model. Defense:
- Documents are chunked and stored as plain text — HTML, scripts, and formatting are stripped
- The synthesis step receives evidence as structured data, not raw HTML

**Confidence gaming:** Asking questions in ways designed to inflate confidence artificially. Defense:
- Confidence is computed from evidence scores, not from the model's self-assessment
- The user cannot influence the evidence scoring

---

## Audit as Zero Trust Enforcement

The zero trust posture is enforced, in part, by the audit trail. Because every query is logged:
- Patterns of adversarial behaviour are detectable
- An attacker cannot deny that a query was made
- Security analysts can review query logs for suspicious patterns

Zero trust without auditability is incomplete. The audit chain makes the zero trust posture verifiable and accountable.

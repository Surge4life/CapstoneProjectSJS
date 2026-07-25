# Chapter 03 — Constitutional Pillars

## The Six Constitutional Pillars

The G.O.D.S constitution is implemented in code, not just in documents. These six pillars are the structural commitments that the GBS Constitutional Runtime enforces technically. They cannot be overridden by configuration, by an administrator, or by a client agreement.

---

## Pillar 1: Non-Bypassability

**Statement:** No AI system governed by G.O.D.S can produce an output that bypasses the governance path.

**What this means:** Every request to a governed AI must pass through the `platform-core /decisions` endpoint. There is no API key, no flag, no environment variable that disables this check. In production mode, the governance path is the only path.

**Technical enforcement:**
- The `udoc-agent`, `udoc-sidecar`, `udoc-gateway`, and `udoc-edge` components are the attachment points. A governed AI registers with one of these. The attachment intercepts every request before it reaches the model.
- If the governance path is unreachable, the system fails closed. The request is not forwarded to the AI. The failure is logged with full context.

**Audit record:** Every governance path traversal produces a `DecisionRecord` in the database and an event on the Kafka bus.

---

## Pillar 2: Immutable Audit

**Statement:** Every governance decision, every system event, and every data change is permanently recorded and cannot be altered, deleted, or overwritten.

**What this means:** The audit record is the system of record. The database is derived from the audit record, not the other way around. In any conflict between the operational database and the audit chain, the audit chain is authoritative.

**Technical enforcement:**
- Audit records are written to Cassandra with WORM (Write Once, Read Many) semantics.
- Each record is HMAC-sealed with the platform's signing key.
- Each record references its predecessor, forming a hash chain.
- A daily Merkle root is computed and published, providing a tamper-evident summary of all records for that day.

**Amendment rule:** If an audit record must be corrected (e.g., due to a data entry error in non-governance fields), a new record is written that references the original and states the correction. The original record remains unchanged and visible.

---

## Pillar 3: Human Review Rights

**Statement:** Every person affected by a governance decision has the right to request human review of that decision.

**What this means:** The `BLOCK` outcome from the governance engine is not final. Any subject of a blocked decision can initiate a review request. That request creates an `OversightCase` that must be assigned to a human reviewer within a defined SLA.

**Technical enforcement:**
- The `oversight` router handles review requests
- The `OversightCase` model requires: subject ID, decision ID, review reason, assigned reviewer, review deadline, and final determination
- No `OversightCase` can be closed with status `PENDING`
- The system generates alerts when OversightCase deadlines approach

**Scope:** This right applies to decisions that affect individuals. System-to-system decisions (e.g., a microservice querying another) do not generate individual review rights.

---

## Pillar 4: Jurisdictional Sovereignty

**Statement:** Every governance deployment operates under a declared jurisdiction. No cross-jurisdictional data flow is permitted without explicit authorisation.

**What this means:** When a G.O.D.S instance is deployed, it declares its jurisdiction (e.g., South Africa, Republic of South Africa — Gauteng Province). Data governed under that jurisdiction cannot be transmitted to a system in a different jurisdiction without a documented cross-border authorisation record.

**Technical enforcement:**
- The `sovereignty` router manages jurisdiction declarations and cross-border authorisations
- The `SovereignProfile` model records jurisdiction, applicable law, and data residency requirements
- Cross-border data flows generate `SovereigntyEvent` records

---

## Pillar 5: Proportionate Response

**Statement:** The severity of the governance response must be proportionate to the risk score of the AI request.

**What this means:** The EVA 6-dimensional risk score determines the response tier. Low-risk requests receive `APPROVE`. Medium-risk requests receive `REVIEW`. High-risk requests receive `ESCALATE`. Constitutional violations receive `BLOCK`. The thresholds are configurable per deployment, but the proportionality principle cannot be disabled.

**Technical enforcement:**
- EVA scoring produces a numeric score from 0–100 across six dimensions
- The `decisions` router applies threshold logic to map scores to outcomes
- Thresholds are stored in the `PolicyPack` model and are versioned
- Changes to thresholds are audited and require elevated RBAC permissions

---

## Pillar 6: Explainability

**Statement:** Every governance decision must be explainable to a lay person in plain language.

**What this means:** The `DecisionRecord` includes a `reasoning` field that contains a human-readable explanation of why the decision was made. This is generated by the governance engine, not by the AI model under governance. The explanation references the specific EVA dimensions, policy rules, and constitutional checks that produced the outcome.

**Technical enforcement:**
- The `decisions` router generates explanations as part of the decision record
- Explanations are stored in plain text in the `DecisionRecord`
- Explanations are available to authorised parties via the `audit` and `lineage` routers
- The `OversightCase` display always includes the original decision explanation

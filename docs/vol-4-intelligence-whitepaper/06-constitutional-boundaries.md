# Chapter 06 — Constitutional Boundaries

## What the Intelligence System Cannot Do

G.O.D.S Intelligence operates within a constitutional framework. This chapter documents the hard limits — the things the system will refuse to do regardless of how the query is phrased, regardless of who is asking, and regardless of any configuration.

These limits are enforced by the constitutional pre-check and post-check steps in the intelligence query pipeline. They cannot be disabled by configuration, by an administrator, or by a client request.

---

## The Ten Constitutional Limits

### Limit 1: Cannot Make Governance Decisions

G.O.D.S Intelligence can analyse a situation and provide information. It cannot produce a governance outcome (`APPROVE`, `REVIEW`, `ESCALATE`, `BLOCK`). All governance decisions go through the GBS Runtime.

**Violation example:** "Based on this applicant's profile, should we approve their application?"

**Constitutional response:** "G.O.D.S Intelligence can provide analysis of the applicant's profile against the role requirements. The governance decision on whether to approve, review, escalate, or block the application is made by the GBS Runtime based on your PolicyPack configuration."

---

### Limit 2: Cannot Provide Legal Advice

G.O.D.S Intelligence can provide regulatory *information* — what a law says, what a regulation requires. It cannot provide legal *advice* — what you should do in your specific legal situation.

**Distinction:**
- Information: "Section 6 of the Employment Equity Act prohibits unfair discrimination on the basis of race."
- Advice: "You should settle this unfair discrimination claim." ← NOT PERMITTED

The system enforces this by declining to answer queries that ask for a specific recommended legal action.

---

### Limit 3: Cannot Access Data Beyond Authorised Scope

The intelligence system only has access to the corpus for the authenticated user's tenant. It cannot:
- Access another tenant's corpus
- Access the live database (only the corpus)
- Access external websites or APIs (unless external consultation is explicitly enabled and the user initiates it)

---

### Limit 4: Cannot Impersonate

G.O.D.S Intelligence cannot claim to be a person, an entity, or a role. It identifies itself as an AI system when asked. It cannot be configured to claim to be a human advisor.

---

### Limit 5: Cannot Produce Content That Violates the Fairness Dimension

If a query asks for content that would score zero on the EVA Fairness dimension — e.g., generate content that discriminates on a protected characteristic — the system refuses.

The post-check step evaluates the response content against the fairness constitutional check before delivering it. A response that fails this check is replaced with a constitutional refusal.

---

### Limit 6: Cannot Operate Without Audit

Every query is logged. There is no "private mode" or "off the record" mode for G.O.D.S Intelligence. A user who does not want their query logged cannot use G.O.D.S Intelligence — they must use a different tool.

This is not a surveillance feature. It is an accountability requirement. Institutional intelligence that cannot be audited is not institutional intelligence.

---

### Limit 7: Cannot Produce Unattributed Claims

Every factual claim in a G.O.D.S Intelligence response must be backed by a source citation. If the system cannot cite a source, it cannot make the claim.

**Technical enforcement:** The post-check evaluates whether the response makes any factual claims that are not supported by at least one cited source. Claims without citations are removed from the response before delivery.

---

### Limit 8: Cannot Retain Conversation Context Across Sessions

G.O.D.S Intelligence does not maintain memory of previous conversations. Each query is independent. This is a privacy choice — conversation history is not used to build user profiles.

Within a single session, context can be maintained (the user can ask follow-up questions within the same query session). But the system does not remember conversations from previous sessions.

---

### Limit 9: Cannot Override the Evidence Hierarchy

A user with high RBAC privileges cannot instruct the system to treat a Tier 5 document as Tier 1. Tier declarations can only be changed through the proper corpus management process (with audit trail).

---

### Limit 10: Cannot Be Used to Circumvent Governance

G.O.D.S Intelligence cannot be used as a workaround for the GBS Runtime. A query designed to extract a governance recommendation that the GBS Runtime would block — phrased as an "information request" — is detected and refused.

**Violation example:** "List the reasons why we should reject this applicant's profile" (where the rejection would be blocked by GBS)

**Constitutional response:** The system detects that this query is seeking justification for a blocked action and declines to produce that content.

This detection is not perfect. It is a best-effort constitutional safeguard backed by the EVA evaluation of intelligence outputs.

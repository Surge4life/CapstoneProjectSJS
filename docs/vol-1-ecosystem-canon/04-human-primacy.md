# Chapter 04 — Human Primacy

## The Human Primacy Doctrine

Human primacy is the founding axiom of the G.O.D.S governance framework. It states:

> **No AI system governed by G.O.D.S may make a final, irreversible decision that affects a human being without a human review pathway.**

This is not a feature. It is an architectural constraint that shapes every layer of the system.

---

## What Human Primacy Is Not

Before defining what human primacy is, it is important to be clear about what it is not.

**It is not a ban on AI automation.** The G.O.D.S ecosystem automates many things. Risk scoring is automated. Classification is automated. Document parsing is automated. Routine approvals are automated. Human primacy does not mean humans must touch every decision.

**It is not a requirement for human approval of every action.** Low-risk, routine AI actions can be approved automatically by the governance engine. Human primacy applies to decisions that have material consequences for a human being — particularly `BLOCK` outcomes, `ESCALATE` outcomes, and outcomes that affect legal rights, employment, financial position, or liberty.

**It is not a veto on AI decisions.** A human reviewer can override a governance decision. But they can also confirm it. Human primacy means a human has the *right* to review — not that they will always exercise it or always change the outcome.

---

## The Human Primacy Stack

Human primacy is implemented across three layers:

### Layer 1: The Governance Engine (Automatic)

Every AI request is scored by the EVA engine. The score determines the initial outcome: `APPROVE`, `REVIEW`, `ESCALATE`, or `BLOCK`.

- `APPROVE` — the request proceeds. No human involvement required.
- `REVIEW` — the request is flagged for human review but may proceed pending review.
- `ESCALATE` — the request is held pending human review. It does not proceed.
- `BLOCK` — the request is rejected. A review pathway is opened automatically.

### Layer 2: The Oversight System (Reactive)

When a request produces `BLOCK` or `ESCALATE`, an `OversightCase` is created. The case is:

- Assigned to a reviewer based on RBAC and jurisdiction rules
- Given a review deadline (configurable per deployment, default 5 business days)
- Visible to the subject of the decision (with appropriate redactions)

The reviewer can: `CONFIRM` the decision, `OVERRIDE` the decision, `ESCALATE` to a higher authority, or `REQUEST_MORE_INFO`.

### Layer 3: The Audit Trail (Permanent)

Every human action in the oversight system is recorded in the audit chain with:
- Reviewer identity
- Timestamp
- Decision
- Reasoning
- Evidence consulted

This audit trail is permanent, immutable, and accessible to authorised parties including the subject of the original decision.

---

## Roles That Exercise Human Primacy

| Role | RBAC Role Name | Oversight Scope |
|------|---------------|-----------------|
| Division Supervisor | `supervisor` | Decisions within their division |
| Compliance Officer | `compliance` | All decisions flagged for compliance review |
| Sovereignty Officer | `sovereignty` | Decisions with cross-jurisdictional implications |
| G.O.D.S Administrator | `gods_admin` | All decisions |
| External Auditor | `external_auditor` | Read-only access to all audit records |

---

## The Human Primacy SLA

Every deployment configures a Human Primacy SLA. This defines the maximum time between a `BLOCK` or `ESCALATE` decision and a human review outcome. The default configuration:

| Decision Type | Review SLA | Escalation Trigger |
|--------------|-----------|-------------------|
| `BLOCK` — individual impact | 5 business days | 4 business days without assignment |
| `BLOCK` — system impact | 1 business day | 20 hours without assignment |
| `ESCALATE` | 2 business days | 1.5 business days without assignment |
| `OversightCase` — overdue | Immediate alert | SLA breach logged to audit chain |

# Chapter 07 — G.O.D.S Operating Principles

## The Twelve Operating Principles

These principles govern how the G.O.D.S ecosystem is built, operated, and evolved. They are binding on all contributors, operators, and administrators.

---

### Principle 1: Fail Closed

When in doubt, deny. When governance infrastructure is unavailable, do not fall back to an ungovernced mode. Stop.

The G.O.D.S system is designed to fail closed. If the `platform-core` governance service is unreachable, the attachment component (agent/gateway/edge/sidecar) does not forward the request to the AI model. It returns a governance-unavailable error.

This is inconvenient. It is also correct. A governance system that silently disables itself when it cannot connect is not a governance system — it is a suggestion system.

**Implementation:** Every attachment component implements a `fail_closed()` path. This path returns a structured error response with a `GOVERNANCE_UNAVAILABLE` status code and logs the event to local storage for replay when connectivity is restored.

---

### Principle 2: Explicit Over Implicit

No silent defaults. No assumed configurations. No magic behaviour.

Every configuration value has a documented default. Every default is logged at startup. Every deviation from the default requires an explicit configuration change that is audited.

When a service cannot determine the correct action, it raises an error. It does not guess.

---

### Principle 3: Separation of Concerns

Every module does one thing. Modules do not reach into each other's internals. Communication between modules happens through defined interfaces.

The `governance-engines` and `platform-core` are separate processes. They communicate through well-defined service calls. Neither imports from the other's internal modules.

---

### Principle 4: Version Everything

Every schema, every policy rule, every API response, every configuration — versioned. Old versions are retained, not deleted.

When a breaking change is necessary, the old version continues to operate until a documented migration window has elapsed. No breaking change is deployed without a migration guide.

---

### Principle 5: Document the Why, Not Just the What

Code explains what. Comments and documentation explain why. A future developer reading a piece of code should understand not just what it does, but why it was implemented this way — what alternative was considered and rejected, what constraint it is working within.

This is especially important for governance logic. A constitutional check that looks arbitrary will be removed by a future developer who does not understand its purpose.

---

### Principle 6: Test at the Boundary

Unit tests verify components. Integration tests verify boundaries. The most important tests in the G.O.D.S codebase are the boundary tests — the tests that verify that the governance path behaves correctly end-to-end.

The smoke test suite (`smoke_test.py`) verifies 31 end-to-end paths. These tests are run before every production deployment.

---

### Principle 7: Observability Is Not Optional

Every service emits structured logs. Every service exposes health and metrics endpoints. Every governance decision is observable to authorised parties.

Dark systems — systems that operate without logging, without metrics, without health endpoints — are not permitted in the G.O.D.S ecosystem.

---

### Principle 8: No Vendor Lock-In

Every external dependency has a defined abstraction layer. The database can be swapped (PostgreSQL → compatible). The object storage can be swapped (local → S3 → compatible). The event bus can be swapped (Kafka → compatible).

This is not about switching vendors for cost reasons. It is about institutional ownership. An institution that cannot migrate off a vendor without rewriting their governance infrastructure does not truly own their governance infrastructure.

---

### Principle 9: Regulatory Compliance Is a First-Class Feature

Regulatory requirements are not addressed at the end of the development cycle. They are expressed as policy rules in the GBS engine and are part of the test suite.

When a new regulation is enacted, the response is: write a policy rule, test it, deploy it. Not: schedule a compliance review for next quarter.

---

### Principle 10: The Audit Chain Is Sacred

The audit chain is never truncated, compressed beyond recovery, or written to without the proper sealing protocol. If there is a choice between audit chain integrity and performance, integrity wins.

Performance problems are solved by improving the system. They are never solved by weakening the audit chain.

---

### Principle 11: Access Is Earned, Not Assumed

Every API endpoint requires authentication. Every authenticated request is checked against RBAC rules. Every RBAC role is defined with the minimum permissions necessary for the role's function. Permissions are not added because they might be useful — they are added because they are required for a specific documented function.

---

### Principle 12: The Constitution Cannot Be Configured Away

The six constitutional pillars (Chapter 03) cannot be disabled by configuration. No deployment profile, no operator setting, no administrative action can remove them. A G.O.D.S deployment without these pillars is not a G.O.D.S deployment.

If a client's requirements are incompatible with these pillars, G.O.D.S is not the right product for that client. This is documented in every client agreement.

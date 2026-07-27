# Chapter 10 — Notification Engine

## Purpose

The Notification Engine delivers timely, governance-aware notifications to users across the G.O.D.S ecosystem. Every notification is tied to a governance event — not a marketing event. Notifications exist to keep users informed about decisions that affect them, obligations they have, and deadlines they must meet.

---

## Location

- Notifications are produced by the `event_bus` service and consumed by a notification worker
- Currently implemented as in-process background tasks (APScheduler) with in-app notification storage
- Future: dedicated notification microservice with push delivery

---

## Notification Types

| Type | Who Receives It | Trigger |
|------|----------------|---------|
| `APPLICATION_STATUS_CHANGE` | Learner | Their application status changes |
| `GOVERNANCE_BLOCK` | Subject of the block | A governance decision BLOCKs an action affecting them |
| `OVERSIGHT_CASE_OPENED` | Subject + assigned reviewer | A BLOCK creates an oversight case |
| `OVERSIGHT_CASE_ASSIGNED` | Reviewer | An oversight case is assigned to them |
| `OVERSIGHT_CASE_OVERDUE` | Reviewer + their supervisor | SLA deadline approaching (1 day before) |
| `OVERSIGHT_CASE_SLA_BREACHED` | Reviewer + division admin | SLA deadline passed |
| `MODEL_SUSPENDED` | Operator | Their model has been suspended |
| `MODEL_CERTIFIED` | Operator | Their model has been certified |
| `NEW_OPPORTUNITY_MATCH` | Learner | A new opportunity matches their profile |
| `DOCUMENT_INTEGRITY_FAILURE` | Uploader + compliance | A document fails integrity check on download |
| `POLICY_PACK_UPDATED` | Division admins | A new PolicyPack has been activated |
| `AUDIT_CHAIN_ANOMALY` | gods_admin | Automated chain verification detects an anomaly |

---

## Notification Data Model

```python
class Notification(Base):
    id: UUID
    recipient_id: UUID              # User who receives it
    tenant_id: UUID
    notification_type: str
    title: str                      # Short, plain language
    body: str                       # Longer description
    action_url: str | None          # Deep link to relevant record
    priority: str                   # low | standard | high | critical
    read_at: datetime | None
    dismissed_at: datetime | None
    related_resource_type: str | None
    related_resource_id: UUID | None
    governance_ref_id: UUID | None  # Link to the governance event that caused this
    created_at: datetime
```

---

## Notification Delivery

**Current delivery channels:**
1. **In-app notifications** (stored in database, polled by frontend via `GET /notifications`)
2. **Email** (SMTP-based, templated, for high-priority notifications)

**Planned delivery channels:**
3. Push notifications (via Capacitor push plugin on mobile apps)
4. Webhook delivery (for operator integrations)

---

## Notification Governance Rules

Notifications themselves are governed:

1. **No dark patterns** — notifications only contain information the recipient needs. No upselling, no engagement manipulation.
2. **PII boundaries** — notification content must not include sensitive personal information beyond what the recipient is authorised to see.
3. **Audit linkage** — every notification is linked to the governance event that triggered it. Recipients can follow the audit trail from the notification.
4. **Rate limiting** — a single user cannot receive more than 20 notifications per hour from the system (emergency overrides for `critical` priority).
5. **Do not disturb** — users can configure quiet hours for non-critical notifications. Critical notifications (governance blocks, SLA breaches) are not affected by quiet hours.

---

## Oversight SLA Notifications

The SLA notification workflow is enforced by a scheduled job (APScheduler, runs every 30 minutes):

```python
async def check_oversight_sla():
    # Find cases approaching their deadline
    approaching = await db.query(
        OversightCase,
        status NOT IN ('resolved', 'escalated'),
        review_deadline BETWEEN NOW() AND NOW() + INTERVAL '24 HOURS'
    )
    for case in approaching:
        await notify(case.assigned_to, type='OVERSIGHT_CASE_OVERDUE', priority='high')

    # Find cases that have breached their deadline
    breached = await db.query(
        OversightCase,
        status NOT IN ('resolved', 'escalated'),
        review_deadline < NOW()
    )
    for case in breached:
        await notify(case.assigned_to, type='OVERSIGHT_CASE_SLA_BREACHED', priority='critical')
        await notify_supervisor(case)
        await write_audit_record(event_type='GOVERNANCE.SLA_BREACH', resource_id=case.id)
```

SLA breaches are not just notifications — they are audit events. An unresolved SLA breach appears in governance reports and compliance reviews.

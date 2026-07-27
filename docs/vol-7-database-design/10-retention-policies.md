# Chapter 10 — Data Retention Policies

## Retention as Governance

Data retention is a governance decision, not just a technical housekeeping task. Keeping data too long creates privacy risk. Deleting data too early destroys the governance record. The retention policies in this chapter balance both requirements, informed by POPIA and the G.O.D.S constitutional framework.

---

## Retention Policy Summary

| Data Category | Active Store (PostgreSQL) | Archive (Cassandra) | Notes |
|--------------|--------------------------|---------------------|-------|
| Governance decisions | 7 years | Permanent | POPIA + audit requirement |
| Oversight cases | 7 years | Permanent | |
| Audit chain records | 7 years | Permanent | Never deletable |
| Authentication events | 3 years | Permanent | Security requirement |
| SETHS learner records | Duration of relationship + 5 years | Permanent (anonymised) | POPIA Section 14 |
| SETHS applications | 5 years | Permanent (anonymised) | |
| SETHS documents | 5 years after last reference | Permanent metadata | Original file may be purged |
| Intelligence queries | 3 years | Permanent | |
| Platform events | 90 days | Permanent (key events) | Most events are transient |
| Notifications | 180 days | Not archived | Operational only |
| Webhook deliveries | 30 days | Not archived | Operational only |
| Session tokens | Until expiry | Not archived | Security only |

---

## Immutable Records (Never Deleted)

Some records are explicitly protected from deletion regardless of retention timers:

1. **Audit chain records (Cassandra)** — constitutional requirement
2. **Governance decisions** — governance accountability
3. **FSM state transitions** — model lifecycle history
4. **Certification records** — certification history (revoked certs must remain as revoked, not deleted)
5. **Signed operator agreements** — contractual record

"Permanent" means the record exists in the audit chain (Cassandra) forever. The operational database (PostgreSQL) may anonymise the record after the retention period, but the audit chain record is never touched.

---

## Anonymisation vs Deletion

For POPIA compliance, the right to erasure applies to *personal data* — not to governance records. When a learner requests erasure:

**What is anonymised (personal data removed):**
- `seths.learners`: name, email, phone, id_number → replaced with pseudonymous identifier
- `iam.users`: email, name, profile data → soft-deleted
- Intelligence query text → hash retained, text purged
- Notification bodies that contained PII → text purged

**What is retained (governance records):**
- The fact that a learner participated in the system
- Application outcomes (for employment equity analytics)
- Governance decisions that referenced the learner (audit chain record retained)
- Document metadata (hash, type, size) — original file may be purged

The anonymisation process preserves the statistical integrity of governance analytics while honouring the individual's right to erasure.

---

## Retention Enforcement (Automated Jobs)

APScheduler jobs run nightly to enforce retention:

```python
# Nightly at 02:00 UTC
@scheduler.task('cron', id='retention_cleanup', hour=2, minute=0)
async def run_retention_cleanup():
    """Enforce data retention policies across all tenants."""
    
    # 1. Purge expired platform events (> 90 days)
    await db.execute("""
        DELETE FROM events.platform_events
        WHERE retain_until < NOW()
    """)
    
    # 2. Purge old notifications (> 180 days)
    await db.execute("""
        DELETE FROM events.notifications
        WHERE created_at < NOW() - INTERVAL '180 days'
    """)
    
    # 3. Purge old webhook delivery records (> 30 days)
    await db.execute("""
        DELETE FROM events.webhook_deliveries
        WHERE created_at < NOW() - INTERVAL '30 days'
        AND status IN ('delivered', 'abandoned')
    """)
    
    # 4. Anonymise expired learner records
    expired_learners = await db.fetchall("""
        SELECT id FROM seths.learners
        WHERE anonymise_after < NOW()
        AND anonymised_at IS NULL
    """)
    for learner in expired_learners:
        await anonymise_learner(learner.id)
    
    # 5. Write retention job audit record
    await audit_writer.write(event_type="SYSTEM.RETENTION_JOB_COMPLETE", ...)
```

The retention job itself is audited. If it fails, an alert is triggered.

---

## The Retention Register

The platform maintains a retention register — a documented record of what data is held, for how long, and why. The register is accessible at `GET /privacy/retention-register` (authenticated, any role).

This register satisfies POPIA's requirement that data subjects be informed of retention periods, and that the information officer can demonstrate compliance with retention policies.

---

## Cross-Tenant Retention

Each tenant's data has its own retention timer. When a client relationship ends:

1. The off-boarding date is recorded
2. A 30-day notice period begins (data remains accessible to the client)
3. After 30 days: client corpus purged, personal data anonymised
4. Governance records retained per the standard schedule

The client can request a full data export during the 30-day notice period. After the export window closes, the data is only accessible to G.O.D.S administrators for audit purposes.

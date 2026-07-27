# Chapter 08 — Disaster Recovery

## Recovery Objectives

| Scenario | RTO (Recovery Time Objective) | RPO (Recovery Point Objective) |
|----------|------------------------------|-------------------------------|
| Single service failure | < 5 minutes | 0 (stateless services restart instantly) |
| Database failure | < 30 minutes | < 1 hour (last backup) |
| Full environment failure | < 4 hours | < 1 hour |
| Data corruption | < 8 hours | < 24 hours (daily backup) |
| Cassandra (audit chain) corruption | < 8 hours | 0 (replication to DR site) |

The audit chain (Cassandra) has a RPO of 0 because a governance record that is not replicated is a governance record that may be lost permanently — an unacceptable outcome for an immutable audit chain.

---

## Backup Strategy

### PostgreSQL

**Backup type:** Logical (pg_dump)  
**Schedule:** Daily at 01:00 UTC  
**Retention:** 30 daily backups; 12 monthly backups  
**Storage:** Encrypted at rest, stored in separate cloud region or off-site storage  
**Restore test:** Monthly restore drill to isolated environment  

```bash
# Backup
pg_dump -Fc gods > /backup/gods-$(date +%Y%m%d).dump

# Restore (to isolated environment for testing)
pg_restore -d gods_restore /backup/gods-20250115.dump

# Verify restore
python smoke_test.py --target http://restore-env:8000 --read-only
```

### Cassandra (Audit Chain)

**Backup type:** Snapshot + incremental  
**Schedule:** Continuous replication to DR cluster  
**Retention:** Indefinite (audit chain is permanent)  
**DR cluster:** Separate physical location or cloud region  
**Restore test:** Quarterly — verify chain integrity on DR cluster  

The Cassandra DR cluster receives real-time replication via Cassandra's built-in multi-DC replication (replication_factor=3, two DCs). Failover to DR cluster is semi-automatic (requires human confirmation per sovereignty requirements).

### Redis

**Backup type:** RDB snapshot + AOF  
**Schedule:** RDB every 6 hours; AOF continuous  
**Retention:** 7 days  
**Restore:** From RDB snapshot or AOF replay  

Redis data is recoverable but non-critical for governance integrity — sessions and caches can be rebuilt from primary databases.

### Cassandra: Governance vs Redis: Cache

This distinction matters: Redis losing its data is a session inconvenience (users must log in again). Cassandra losing audit records is a constitutional crisis. The backup priority and test frequency reflects this.

---

## Disaster Recovery Runbook

### Scenario: platform-core pod crashes (most common)

**Kubernetes auto-recovers this.** No manual action required.  
Monitor: pod restarts counter in Grafana. > 5 restarts in 1 hour → investigate.

---

### Scenario: PostgreSQL primary failure

```bash
# 1. Verify: what failed?
kubectl get pods -n gods-data-ns
kubectl logs <postgres-pod> -n gods-data-ns --previous

# 2. If primary is unrecoverable, promote replica
kubectl exec -it <postgres-replica-pod> -- \
  pg_ctl promote -D /var/lib/postgresql/data

# 3. Update service to point to new primary
kubectl patch service postgres -n gods-data-ns \
  -p '{"spec":{"selector":{"role":"primary"}}}'

# 4. Verify platform-core reconnects
kubectl rollout restart deployment/platform-core -n gods-ns
curl https://gods.example.com/health
```

---

### Scenario: Full environment loss (rare)

```bash
# 1. Provision new Kubernetes cluster
# (use Terraform: terraform apply -target=module.kubernetes)

# 2. Restore PostgreSQL from backup
pg_restore -d gods /backup/gods-latest.dump

# 3. Restore Cassandra from DR cluster
# (connect DR cluster as primary, rebuild production cluster behind it)

# 4. Re-deploy application
kubectl apply -f infra/k8s/

# 5. Verify audit chain integrity
gods-cli verify-chain --full

# 6. Run smoke tests
python smoke_test.py --target https://gods.example.com

# 7. Perform governance sign-off for restored deployment
POST /system/governance-sign-off
```

Full recovery from complete loss should take < 4 hours with this runbook. Practice this quarterly in a DR drill — the first time you run a DR runbook in a real incident should not be the first time you've run it at all.

---

## DR Communication Plan

During a disaster recovery event:

1. **0–15 minutes:** On-call engineer assesses situation; declares incident if RTO > 30 minutes
2. **15–60 minutes:** Incident commander assigned; status updates to Slack #gods-ops every 15 minutes
3. **60+ minutes:** External communication to affected clients (if platform-wide outage)
4. **Recovery confirmed:** Post-incident report within 48 hours
5. **Audit record:** Every DR event is recorded as a `SYSTEM.DISASTER_RECOVERY_EVENT` in the audit chain

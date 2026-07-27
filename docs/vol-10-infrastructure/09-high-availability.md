# Chapter 09 — High Availability

## Availability Target

The G.O.D.S platform targets **99.9% availability** (≤ 8.7 hours downtime per year) for production deployments. Critical governance infrastructure (the governance decision path specifically) targets 99.95%.

---

## Availability by Component

| Component | HA Configuration | Failure Mode |
|-----------|-----------------|-------------|
| `platform-core` | 3 replicas, HPA (3–10) | Kubernetes restarts failed pods |
| Governance engines | 2 replicas each, HPA | Kubernetes restarts; circuit breaker in platform-core |
| PostgreSQL | Primary + 2 standbys (Patroni) | Automatic failover to standby |
| Redis | Sentinel mode (1 primary + 2 replicas) | Automatic failover |
| Kafka | 3-broker cluster, replication factor 3 | Broker failure without data loss |
| Cassandra | 3-node cluster (or multi-DC for DR) | Node failure without data loss (RF=3) |
| OpenSearch | 3-node cluster (1 master + 2 data) | Node failure without data loss |
| NGINX Ingress | 2 replicas | Kubernetes restarts; loadbalancer handles traffic |

No single point of failure exists in a properly configured production deployment.

---

## PostgreSQL High Availability (Patroni)

Patroni manages PostgreSQL replication and failover:

```yaml
# patroni.yml (simplified)
scope: gods-postgres
namespace: gods-data-ns

postgresql:
  listen: 0.0.0.0:5432
  connect_address: postgres-0:5432
  data_dir: /var/lib/postgresql/data
  
  replication:
    username: replicator
    password: <from Vault>
    
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # 1MB max lag before failover
    
  postgresql:
    use_pg_rewind: true
    parameters:
      max_connections: 200
      wal_level: replica
      max_wal_senders: 10
```

Failover process:
1. Primary fails health check (TTL expires)
2. Patroni DCS (etcd or consul) detects failure
3. Most up-to-date standby elected as new primary
4. Patroni updates DNS to point to new primary
5. platform-core reconnects (asyncpg handles reconnection)
6. Total failover time: 15–30 seconds

---

## Horizontal Pod Autoscaling

Platform-core scales automatically based on CPU and governance latency:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: platform-core-hpa
  namespace: gods-ns
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: platform-core
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: External
    external:
      metric:
        name: gods_governance_latency_p95_ms
      target:
        type: Value
        value: "80"  # Scale up if governance latency p95 > 80ms
```

The custom governance latency metric is the primary scaling signal — when governance decisions start taking longer (indicating load), add more pods before CPU becomes a bottleneck.

---

## Kafka HA Configuration

```
Kafka Cluster: 3 brokers
Replication factor: 3 (all partitions replicated to all brokers)
Min in-sync replicas: 2 (producer blocks if < 2 replicas acknowledge write)

Topics:
  gods.audit.events      partitions: 12, RF: 3, retention: 90 days
  gods.governance.events partitions: 6,  RF: 3, retention: 90 days
  gods.notifications     partitions: 6,  RF: 3, retention: 7 days
```

With RF=3 and min.insync.replicas=2, the Kafka cluster can tolerate one broker failure with no data loss and continued write availability.

---

## Graceful Degradation

When components are degraded (not failed, just slow), the system degrades gracefully:

| Degraded Component | System Behaviour |
|-------------------|-----------------|
| EVA engine slow | Circuit breaker delays opening; governance latency increases; alert fires |
| Cassandra lagging | Audit writes buffered in Kafka; eventually consistent; alert fires |
| OpenSearch slow | Intelligence queries timeout; low confidence responses returned |
| Kafka broker down | Producer retries; audit events buffered in application memory (short-term) |
| Redis unavailable | Session lookup falls through to JWT verification; policy cache reloads from DB |

The governance decision path degrades to BLOCK (fail-closed) only when the EVA engine or audit chain are completely unavailable — not merely slow.

---

## Maintenance Windows

Planned maintenance (Kubernetes updates, database upgrades, etc.) uses a maintenance window approach:

1. **Announce** maintenance via platform notification (minimum 48 hours notice)
2. **Enable** maintenance mode (`POST /system/maintenance-mode`)
3. **Drain** pending governance requests (complete in-flight, queue new ones)
4. **Perform** maintenance (rolling update, zero downtime for minor changes; brief downtime for major changes)
5. **Disable** maintenance mode
6. **Verify** health (`smoke_test.py --target production`)
7. **Audit** maintenance event recorded

Governance critical path changes (PolicyPack updates, governance engine updates) require a change approval process before maintenance can proceed.

# Chapter 19 — Monitoring Engine

## Purpose

The Monitoring Engine provides observability into every layer of the G.O.D.S ecosystem — service health, governance performance, audit chain integrity, and security posture. Monitoring is not optional: an unobservable governance system cannot be trusted.

---

## Observability Pillars

The G.O.D.S monitoring approach follows the three pillars of observability:

| Pillar | Tool | Data |
|--------|------|------|
| **Metrics** | Prometheus + Grafana | Counters, gauges, histograms for all services |
| **Logs** | Structured JSON logs → ELK or Loki | Every request, every governance event |
| **Traces** | OpenTelemetry → Jaeger or Tempo | Request traces across service boundaries |

---

## Key Metrics

### Governance Metrics (Critical)

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|----------------|
| `gods_governance_decisions_total` | Counter | Total decisions by outcome | — |
| `gods_governance_latency_ms` | Histogram | Governance path latency | p95 > 100ms |
| `gods_governance_block_rate` | Gauge | % of decisions resulting in BLOCK | > 20% sustained |
| `gods_oversight_cases_open` | Gauge | Open oversight cases | > 100 open |
| `gods_oversight_sla_breached` | Counter | SLA breaches | Any breach |
| `gods_audit_chain_lag_seconds` | Gauge | Lag between governance decision and Cassandra write | > 60s |
| `gods_governance_engine_errors` | Counter | EVA/GBS engine errors | Any error |

### Service Health Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|----------------|
| `gods_api_request_duration_ms` | Histogram | API endpoint latency | p99 > 1000ms |
| `gods_api_error_rate` | Gauge | HTTP 5xx rate | > 1% sustained |
| `gods_db_pool_utilization` | Gauge | PostgreSQL connection pool usage | > 80% |
| `gods_kafka_consumer_lag` | Gauge | Audit event consumer lag | > 1000 messages |
| `gods_redis_memory_used_bytes` | Gauge | Redis memory usage | > 80% of max |

### Security Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|----------------|
| `gods_auth_failure_rate` | Counter | Failed authentication attempts | > 50/min per IP |
| `gods_rbac_denial_rate` | Counter | RBAC permission denials | Burst > 20/min per user |
| `gods_audit_chain_anomalies` | Counter | Detected chain integrity issues | Any anomaly |

---

## Health Endpoint

```
GET /health
```

Returns a comprehensive health check:

```json
{
  "status": "healthy",
  "version": "2.1.0",
  "governance_version": "GV3",
  "checks": {
    "database": {"status": "healthy", "latency_ms": 2},
    "redis": {"status": "healthy", "latency_ms": 1},
    "kafka": {"status": "healthy", "lag": 0},
    "governance_engine": {"status": "healthy", "latency_ms": 8},
    "audit_chain": {
      "status": "healthy",
      "last_record_age_seconds": 45,
      "cassandra_lag_seconds": 3
    }
  },
  "uptime_seconds": 86400,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

If any check fails, the overall `status` becomes `degraded` or `unhealthy`, and the HTTP status code becomes `503`.

---

## Grafana Dashboards

The `infra/monitoring/grafana/` directory contains pre-built Grafana dashboard JSON files:

| Dashboard | Purpose |
|-----------|---------|
| `governance-overview.json` | Real-time governance decision feed and outcome distribution |
| `api-performance.json` | Endpoint latency, error rates, request volume |
| `audit-chain-health.json` | Chain lag, Cassandra write latency, Merkle root status |
| `security-posture.json` | Auth failures, RBAC denials, anomaly detection |
| `seths-division.json` | SETHS-specific metrics: applications, matching, documents |
| `infrastructure.json` | Kubernetes pod health, database connections, memory |

---

## Alerting

Alerts are defined in `infra/monitoring/alerts/` as Prometheus alerting rules and routed through Alertmanager.

**Alert channels:**
- `critical` — PagerDuty (immediate on-call notification)
- `high` — Slack `#gods-alerts` channel
- `standard` — Email digest (hourly)

**Key alert definitions:**

```yaml
# Any governance engine error is critical — fail-closed
- alert: GovernanceEngineError
  expr: rate(gods_governance_engine_errors_total[5m]) > 0
  severity: critical
  message: "Governance engine errors detected. Governance path may be compromised."

# SLA breach is critical — human primacy obligation
- alert: OversightSLABreached
  expr: gods_oversight_sla_breached_total > 0
  severity: critical
  message: "Oversight case SLA breached. Human review obligation unfulfilled."

# Audit chain lag is critical — immutability at risk
- alert: AuditChainLagHigh
  expr: gods_audit_chain_lag_seconds > 120
  severity: critical
  message: "Audit chain Cassandra lag > 2 minutes. Immutability guarantee at risk."
```

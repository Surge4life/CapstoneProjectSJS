# Chapter 11 — Monitoring Infrastructure

## The Observability Stack

G.O.D.S uses the Prometheus/Grafana/Alertmanager stack for observability, extended with OpenTelemetry for distributed tracing and structured JSON logging for log management.

---

## Prometheus Configuration

Prometheus scrapes metrics from all G.O.D.S services every 15 seconds:

```yaml
# infra/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - '/etc/prometheus/alerts/governance.yml'
  - '/etc/prometheus/alerts/infrastructure.yml'
  - '/etc/prometheus/alerts/security.yml'

scrape_configs:
  - job_name: 'platform-core'
    kubernetes_sd_configs:
      - role: pod
        namespaces: { names: ['gods-ns'] }
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: platform-core
        action: keep

  - job_name: 'governance-engines'
    static_configs:
      - targets: ['eva:3002', 'udoc:3003', 'gis:3004', 'gods:3001']
        labels: { service_type: 'governance' }

  - job_name: 'databases'
    static_configs:
      - targets: ['postgres-exporter:9187', 'redis-exporter:9121']

  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka-exporter:9308']
```

---

## Custom Metrics

`platform-core` exposes custom Prometheus metrics at `GET /metrics`:

```python
from prometheus_client import Counter, Histogram, Gauge

# Governance decision metrics
governance_decisions = Counter(
    'gods_governance_decisions_total',
    'Total governance decisions',
    labelnames=['outcome', 'model_type', 'tenant_id']
)

governance_latency = Histogram(
    'gods_governance_latency_ms',
    'Governance path latency in milliseconds',
    labelnames=['outcome'],
    buckets=[10, 20, 30, 50, 75, 100, 150, 200, 500, 1000]
)

oversight_cases_open = Gauge(
    'gods_oversight_cases_open',
    'Currently open oversight cases',
    labelnames=['case_type', 'tenant_id']
)

audit_chain_lag = Gauge(
    'gods_audit_chain_lag_seconds',
    'Lag between governance decision and Cassandra write'
)
```

---

## Grafana Dashboards

Located in `infra/monitoring/grafana/dashboards/`:

### `governance-overview.json`

The primary operational dashboard:
- Live governance decision rate (per minute)
- Outcome distribution (stacked bar: APPROVE/REVIEW/ESCALATE/BLOCK)
- EVA score trends (line chart, all 6 dimensions + overall)
- Open oversight cases (gauge)
- Governance latency (p50, p95, p99 — time series)
- Block rate trend

### `audit-chain-health.json`

- Cassandra write latency
- Audit chain lag (time between decision and chain write)
- Daily record count vs expected
- Chain verification status (from most recent verify job)

### `api-performance.json`

- Request rate by endpoint
- Error rate (4xx and 5xx)
- Latency percentiles by endpoint
- Connection pool utilisation (PostgreSQL + Redis)

### `security-posture.json`

- Authentication failure rate (by IP)
- RBAC denial rate (by user)
- Rate limit triggers
- Unusual access pattern alerts

### `infrastructure.json`

- Kubernetes pod health (by namespace)
- CPU and memory by pod
- Database connection counts
- Kafka consumer lag

---

## Alertmanager Routing

```yaml
# infra/monitoring/alertmanager/alertmanager.yml
global:
  slack_api_url: '<from Vault>'

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  receiver: 'slack-default'
  routes:
    - match: { severity: 'critical' }
      receiver: 'pagerduty-critical'
      continue: true    # Also send to Slack
    - match: { severity: 'critical' }
      receiver: 'slack-critical'
    - match: { severity: 'high' }
      receiver: 'slack-high'

receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - routing_key: '<from Vault>'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#gods-alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'

  - name: 'slack-high'
    slack_configs:
      - channel: '#gods-alerts'
        title: '⚠️ HIGH: {{ .GroupLabels.alertname }}'

  - name: 'slack-default'
    slack_configs:
      - channel: '#gods-alerts'
```

---

## Distributed Tracing

OpenTelemetry traces the governance request path end-to-end:

```
Client request → NGINX → platform-core (span)
                              → EVA engine (child span)
                              → UDOC engine (child span)
                              → PostgreSQL write (child span)
                              → Cassandra write (child span)
                              → Kafka publish (child span)
```

Traces are sent to Jaeger or Tempo (configurable). The trace ID is included in the governance decision response and in the audit record, enabling correlation between the decision and the full execution trace.

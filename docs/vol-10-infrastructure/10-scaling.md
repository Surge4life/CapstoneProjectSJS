# Chapter 10 — Scaling

## Scaling Philosophy

The G.O.D.S platform is designed for horizontal scaling of stateless compute components. The governance path is deliberately stateless: every governance request is complete in a single synchronous call, with all context loaded from the database or cache. This means platform-core can scale to any number of replicas without coordination.

The data layer (PostgreSQL, Cassandra, Kafka) scales vertically first, then horizontally — adding nodes is more complex than adding compute replicas.

---

## Scaling Tiers

| Tier | Concurrent Users | Governance Decisions/Day | Recommended Configuration |
|------|-----------------|-------------------------|--------------------------|
| Starter | 0–100 | 0–10,000 | 2 platform-core pods, single-node DBs |
| Professional | 100–500 | 10,000–100,000 | 3 platform-core pods, primary+standby DBs |
| Enterprise | 500–5,000 | 100,000–1,000,000 | 5–10 pods (HPA), HA DBs, Cassandra 3-node |
| National Scale | 5,000+ | 1M+ | Multi-region, Kafka partitioned, Cassandra multi-DC |

---

## Compute Scaling (Horizontal)

`platform-core` scales horizontally with no code changes required:

```bash
# Manual scale (emergency)
kubectl scale deployment platform-core --replicas=8 -n gods-ns

# Automatic (HPA — standard configuration)
# Scales from 3 to 10 replicas based on CPU + governance latency
```

Governance engines (EVA, UDOC, GIS, G.O.D.S) also scale horizontally — each is stateless and can run as many replicas as needed. The platform-core circuit breaker distributes requests across all engine replicas.

---

## PostgreSQL Scaling

**Vertical first:** PostgreSQL scales well vertically. Double the RAM before adding read replicas.

**Read scaling:** For analytics-heavy workloads, add read replicas and route analytics queries to the replicas:
```python
# In sqlalchemy configuration
read_db_url = os.getenv("DATABASE_READ_URL", DATABASE_URL)
```

Analytics and reporting queries use the read URL. Governance writes always use the primary.

**Partitioning:** For very large tables (> 100 million rows), partition by date:
```sql
-- Partition governance.decisions by month
CREATE TABLE governance.decisions_2025_01 
  PARTITION OF governance.decisions
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

---

## Cassandra Scaling

The audit chain grows at a constant rate: approximately 1 KB per governance event + 500 bytes overhead. For 1 million decisions per day: ~1.5 GB/day.

Cassandra scales by adding nodes:
```bash
# Add a new Cassandra node to the cluster
# (Cassandra automatically rebalances data)
kubectl scale statefulset cassandra --replicas=4 -n gods-data-ns
```

With RF=3 and 4 nodes, data is evenly distributed and no single node holds all data. Each additional node increases read/write throughput linearly.

---

## OpenSearch Scaling

The corpus index size depends on corpus size and chunk count. Rules of thumb:
- 1 GB of documents → ~500 MB of indexed text + ~2 GB of vectors (at 1536 dimensions)
- 1 million chunks → ~6 GB of vector storage (1536-dim float32)

Add data nodes when the index exceeds 70% of current storage:
```bash
kubectl scale statefulset opensearch-data --replicas=4 -n gods-data-ns
```

For very large corpora (> 100 GB total), consider reducing embedding dimensions or using a more compact embedding model.

---

## Kafka Scaling

Kafka throughput is proportional to partition count. Add partitions (not brokers first) when throughput is constrained:
```bash
kafka-topics.sh --alter --topic gods.audit.events \
  --partitions 24 \  # Doubling from 12
  --bootstrap-server kafka:9092
```

Partitions cannot be reduced — plan partition count at cluster setup based on expected max throughput. Rule of thumb: 1 partition per 10 MB/s throughput.

---

## Load Testing

Before scaling up in production, validate the configuration under load:

```bash
# Use locust for load testing
cd tests/load
locust -f governance_load_test.py \
  --host https://gods-staging.example.com \
  --users 500 \
  --spawn-rate 50

# Watch governance latency in real-time
curl https://gods-staging.example.com/metrics | \
  grep gods_governance_latency
```

Target under load:
- Governance latency p50: < 20ms
- Governance latency p95: < 50ms
- Governance latency p99: < 100ms
- Error rate: < 0.1%

If p99 > 100ms at target load, investigate before production.

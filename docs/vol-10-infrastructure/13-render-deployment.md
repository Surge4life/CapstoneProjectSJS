# Chapter 13 — Render Deployment (Current Production)

## Current Production Environment

The G.O.D.S ecosystem is currently deployed to **Render** — a cloud platform that provides managed services for containers, databases, and static sites. This is the Tier 1 (cloud) deployment as described in the infrastructure overview.

The Render deployment configuration is defined in `render.yaml` at the repository root.

---

## render.yaml Services

```yaml
# render.yaml (summary)
services:
  - name: gods-platform-core
    type: web
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: gods-postgres
          property: connectionString
      # ... other env vars

  - name: gods-udoc-web
    type: web
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist
    
  - name: gods-platform-internal
    type: web
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist

  - name: gods-portals
    type: web
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist

  - name: gods-udoc-admin
    type: web
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist

databases:
  - name: gods-postgres
    databaseName: gods_production
    user: gods_prod
    plan: standard  # 4GB RAM, 2 vCPU
```

---

## Environment Variables Required for Render Deployment

These must be configured in the Render dashboard (or via the Render API) for the `gods-platform-core` service:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Auto-populated from Render PostgreSQL database |
| `SECRET_KEY` | JWT signing key — generate with `openssl genrsa -out private.pem 2048` |
| `REDIS_URL` | Render Redis instance URL |
| `KAFKA_BOOTSTRAP_SERVERS` | External Kafka (Upstash or Confluent Cloud recommended) |
| `CASSANDRA_HOSTS` | External Cassandra (DataStax Astra recommended) |
| `OPENSEARCH_URL` | External OpenSearch (or AWS OpenSearch Service) |
| `OBJECT_STORAGE_URL` | S3-compatible URL (Backblaze B2, Cloudflare R2, or AWS S3) |
| `OBJECT_STORAGE_BUCKET` | Bucket name for document storage |
| `OBJECT_STORAGE_KEY_ID` | Access key |
| `OBJECT_STORAGE_SECRET` | Secret key |
| `HSM_PKCS11_LIB` | Software HSM path (SoftHSM in cloud mode) |
| `GOVERNANCE_ENGINE_URL` | URL of governance engines service |
| `ENVIRONMENT` | `production` |

---

## Render Limitations and Mitigations

Render provides a good developer experience but has limitations for production governance workloads:

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No dedicated Kafka | Event streaming reliability | Use Upstash Kafka (managed, serverless) |
| No dedicated Cassandra | WORM audit storage | Use DataStax Astra Serverless (Cassandra-compatible) |
| Cold starts on free tier | Governance latency spikes | Use paid tier (always-on) |
| Shared database | Performance | Use Standard plan minimum |
| No hardware HSM | Cryptographic signing | SoftHSM (acceptable for cloud tier, not for sovereign tier) |

---

## Deployment Process

```bash
# Trigger a production deployment via Render's deploy hook
curl -X POST https://api.render.com/deploy/srv-{service-id}?key={deploy-key}
```

Or via the Render dashboard: Services → gods-platform-core → Manual Deploy → Deploy latest commit.

**Pre-deployment checklist:**
1. All smoke tests passing locally
2. Database migrations tested against a staging database
3. Environment variables verified
4. Render service health check URL accessible

**Post-deployment verification:**
1. `GET https://gods-platform-core.onrender.com/health` returns `{"status": "healthy"}`
2. Authentication endpoint functional
3. Run smoke test suite against production URL (read-only subset)

---

## Scaling on Render

Current production settings:
- `gods-platform-core`: Standard plan (2 vCPU, 4GB RAM), single instance
- Scale to multiple instances as load increases

When to scale:
- CPU consistently > 70% → scale up
- Governance path p95 latency > 100ms → scale up or optimise
- Memory > 80% → scale up

Render supports automatic scaling based on CPU/memory metrics on the Pro plan.

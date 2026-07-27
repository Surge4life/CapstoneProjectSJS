# Chapter 18 — Deployment Engine

## Purpose

The Deployment Engine manages the software deployment lifecycle for G.O.D.S instances — from initial provisioning through updates, configuration changes, and decommissioning. It is the operational layer that translates infrastructure specifications into running services.

---

## Scope

The Deployment Engine is not a single service — it is a collection of tools, scripts, and documented processes that together constitute the deployment capability. This chapter documents those tools and the processes that use them.

---

## Deployment Targets

| Target | Tool | Configuration |
|--------|------|--------------|
| Local development | Docker Compose | `infra/docker-compose.yml` |
| Render (cloud) | Render API / dashboard | `render.yaml` |
| Kubernetes (private) | `kubectl` + Helm | `infra/k8s/` |
| Air-gapped | Manual + `gods-cli` | `infra/air-gap/` |

---

## The `gods-cli` Tool

`gods-cli` is the command-line tool for G.O.D.S deployment operations. Located in `tools/gods-cli/`.

### Key Commands

```bash
# Health checks
gods-cli health-check --all                    # Check all services
gods-cli health-check --service platform-core  # Check specific service

# Deployment
gods-cli deploy --target render                # Deploy to Render
gods-cli deploy --target k8s --namespace gods-production

# Database
gods-cli migrate --target production           # Run pending migrations
gods-cli migrate --dry-run                     # Preview migrations
gods-cli db-status                             # Show migration status

# Audit chain
gods-cli verify-chain --from 2025-01-01 --to 2025-03-31
gods-cli verify-chain --full                   # Verify entire chain (slow)

# Policy
gods-cli policy list                           # List PolicyPack versions
gods-cli policy activate --version 4          # Activate a PolicyPack version
gods-cli policy export --version 3             # Export a PolicyPack

# Air-gap
gods-cli verify-bundle update.tar.gz --public-key gods-release.pub
gods-cli apply-update update.tar.gz --dry-run
gods-cli apply-update update.tar.gz

# Configuration
gods-cli export-config --output config.tar.gz
gods-cli import-config config.tar.gz
```

---

## Deployment Runbook: Render

```bash
# 1. Ensure all tests pass
python -m pytest tests/ -v
python smoke_test.py

# 2. Deploy via Render dashboard or API
# Dashboard: Services → gods-platform-core → Manual Deploy → Deploy latest

# 3. Monitor deployment
# Render dashboard shows build log and deployment log

# 4. Post-deployment verification
curl https://gods-platform-core.onrender.com/health
python smoke_test.py --target https://gods-platform-core.onrender.com --read-only

# 5. Run pending migrations (if any)
gods-cli migrate --target production
```

---

## Deployment Runbook: Kubernetes

```bash
# 1. Build and push container image
docker build -t gods-platform-core:v2.1.0 ./platform-core
docker push registry.internal:5000/gods-platform-core:v2.1.0

# 2. Update image tag in Kubernetes manifest
kubectl set image deployment/platform-core \
  platform-core=registry.internal:5000/gods-platform-core:v2.1.0 \
  -n gods-production

# 3. Watch rollout
kubectl rollout status deployment/platform-core -n gods-production

# 4. Verify
kubectl get pods -n gods-production
curl https://platform.gods.internal/health
```

---

## Zero-Downtime Deployment

All G.O.D.S deployments target zero downtime. This is achieved through:

1. **Rolling updates** — Kubernetes rolls new pods before removing old ones. `maxUnavailable: 0` ensures old pods serve traffic until new pods are ready.
2. **Readiness probes** — New pods only receive traffic once `GET /health` returns 200.
3. **Database migrations first** — Schema changes are always backward-compatible before deployment. New code is always compatible with both old and new schema.
4. **Feature flags** — New features that require schema changes use feature flags until the migration has been applied universally.

If a deployment goes wrong, rollback:
```bash
kubectl rollout undo deployment/platform-core -n gods-production
```

The rolled-back version is the previously running image. The database schema is left as-is (since it was designed to be backward-compatible).

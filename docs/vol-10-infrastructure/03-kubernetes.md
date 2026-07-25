# Chapter 03 — Kubernetes Orchestration

## Why Kubernetes

Kubernetes provides the production-grade orchestration that the G.O.D.S ecosystem requires:
- **High availability** — automatic pod restart, health-based routing
- **Horizontal scaling** — add capacity without downtime
- **Rolling deployments** — zero-downtime updates
- **Secret management** — Kubernetes Secrets for sensitive configuration
- **Network policies** — service-to-service traffic control

Kubernetes manifests are in `infra/k8s/`.

---

## Namespace Strategy

```
gods-production     — All production workloads
gods-staging        — Staging/pre-production
gods-monitoring     — Prometheus, Grafana, alerting
gods-infra          — Databases, Kafka, Redis (if self-managed)
```

Service accounts are scoped per namespace. A pod in `gods-production` cannot access resources in `gods-staging`.

---

## Core Deployments

### platform-core Deployment

```yaml
# infra/k8s/platform-core/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: platform-core
  namespace: gods-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime
  selector:
    matchLabels:
      app: platform-core
  template:
    metadata:
      labels:
        app: platform-core
    spec:
      serviceAccountName: platform-core-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: platform-core
          image: gods-platform-core:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: platform-core-secrets
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "2000m"
              memory: "2Gi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 30
            failureThreshold: 3
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: platform-core-hpa
  namespace: gods-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: platform-core
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
```

---

## Network Policies

G.O.D.S implements deny-by-default networking. Only explicitly permitted traffic flows between pods.

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: gods-production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Allow platform-core to receive traffic from ingress only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-platform-core-ingress
  namespace: gods-production
spec:
  podSelector:
    matchLabels:
      app: platform-core
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: nginx-ingress
      ports:
        - protocol: TCP
          port: 8000
```

---

## Secret Management

Production secrets are managed via Kubernetes Secrets, populated by the deployment pipeline from a secrets vault (HashiCorp Vault in air-gapped deployments; cloud-native secrets manager in cloud deployments).

```yaml
# infra/k8s/platform-core/secrets.yaml (template — actual values from CI/CD)
apiVersion: v1
kind: Secret
metadata:
  name: platform-core-secrets
  namespace: gods-production
type: Opaque
stringData:
  DATABASE_URL: "$(DATABASE_URL)"
  SECRET_KEY: "$(SECRET_KEY)"
  REDIS_URL: "$(REDIS_URL)"
  # ... etc
```

Secrets are never stored in the repository. The `secrets.yaml` files in the repository are templates with placeholder values that are substituted by the CI/CD pipeline at deployment time.

---

## Persistent Volume Strategy

Database services require persistent storage. In Kubernetes:

| Service | Storage Class | Size | Backup |
|---------|-------------|------|--------|
| PostgreSQL | `ssd-retain` | 100Gi initial, auto-expand | Daily + WAL streaming |
| Cassandra | `ssd-retain` | 500Gi per node | Nodetool snapshot daily |
| OpenSearch | `ssd-retain` | 200Gi | Snapshot to object storage |
| Redis | `ssd-retain` | 20Gi | RDB + AOF |

All persistent volumes use `reclaimPolicy: Retain` — volumes are not deleted when a PVC is deleted. Manual deletion of volumes requires explicit operator action and is logged.

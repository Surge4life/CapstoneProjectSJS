# Chapter 02 — Docker & Container Strategy

## Container Architecture

Every service in the G.O.D.S ecosystem runs in a Docker container. This provides:
- **Environment consistency** — development, staging, and production run the same container image
- **Dependency isolation** — no "works on my machine" problems
- **Deployment flexibility** — any container orchestrator (Render, Kubernetes, self-hosted Docker)
- **Security boundary** — containers isolate service processes from each other

---

## Container Images

### platform-core

```dockerfile
# platform-core/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (separate layer for cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Non-root user (security)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Image size target:** < 400MB  
**Build time target:** < 2 minutes (with layer caching)  
**Base image policy:** Use official slim images. No alpine (glibc compatibility issues with binary wheels).

---

### Frontend Apps

```dockerfile
# seths-app/Dockerfile (build stage)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK CMD curl -f http://localhost/health || exit 1
```

Multi-stage builds keep the final image small (< 50MB for frontend apps).

---

## Docker Compose — Development Stack

The `infra/docker-compose.yml` provides the complete development stack:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: gods_dev
      POSTGRES_USER: gods
      POSTGRES_PASSWORD: gods_dev_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gods -d gods_dev"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass gods_redis_password
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
    ports:
      - "9092:9092"
    depends_on:
      zookeeper:
        condition: service_healthy

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "2181"]
      interval: 10s

  cassandra:
    image: cassandra:4.1
    environment:
      CASSANDRA_CLUSTER_NAME: gods_audit
    volumes:
      - cassandra_data:/var/lib/cassandra
    ports:
      - "9042:9042"
    healthcheck:
      test: ["CMD-SHELL", "nodetool status | grep UN"]
      interval: 30s
      timeout: 10s
      retries: 10

  opensearch:
    image: opensearchproject/opensearch:2.11.0
    environment:
      - discovery.type=single-node
      - DISABLE_SECURITY_PLUGIN=true  # Dev only
    volumes:
      - opensearch_data:/usr/share/opensearch/data
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q 'green\\|yellow'"]
      interval: 30s

volumes:
  postgres_data:
  redis_data:
  cassandra_data:
  opensearch_data:
```

---

## Container Security Standards

### Non-Root Users
All application containers run as a non-root user. Root-required operations happen only in infrastructure containers.

### Read-Only Filesystems
Where possible, containers use read-only root filesystems with specific write volumes:
```dockerfile
# In docker-compose or Kubernetes spec
security_context:
  read_only_root_filesystem: true
  run_as_non_root: true
```

### Image Scanning
All container images are scanned with `trivy` before deployment:
```bash
trivy image gods-platform-core:latest --severity HIGH,CRITICAL --exit-code 1
```

CI pipeline fails if any HIGH or CRITICAL vulnerabilities are found in the base image or installed packages.

### No Secrets in Images
Secrets are injected at runtime via environment variables or mounted secret files. No secrets are baked into container images. Container images can be safely pushed to a registry.

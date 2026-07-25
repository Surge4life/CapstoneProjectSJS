# Chapter 01 — Environment Setup

## Setting Up the G.O.D.S Development Environment

This chapter guides you through getting the complete G.O.D.S development environment running on your local machine. A fully working local environment is a prerequisite for contributing to the codebase.

---

## Prerequisites

| Requirement | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | platform-core, governance-engines (eva, udoc) |
| Node.js | 20+ | Frontend apps, governance-engines (gods, gis) |
| Docker | Latest stable | Database services, full-stack testing |
| Docker Compose | v2+ | Service orchestration |
| Git | Latest stable | Version control |
| `make` | Latest stable | Development convenience commands |

**Optional (for mobile development):**
- Android Studio + JDK 17 (for Capacitor APK builds)
- Xcode (macOS only, for iOS builds)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/[org]/CapstoneProjectSJS.git gods-ecosystem
cd gods-ecosystem
```

---

## Step 2: Start Infrastructure Services

The G.O.D.S ecosystem depends on several infrastructure services. The quickest way to start them all is via Docker Compose:

```bash
cd infra
docker compose up -d postgres redis kafka cassandra opensearch
```

Wait for all services to report healthy:
```bash
docker compose ps
```

Expected output: all services showing `healthy` status. Allow 60–90 seconds for Kafka and Cassandra to fully initialise.

**Individual service ports (local development):**

| Service | Port |
|---------|------|
| PostgreSQL | 5432 |
| Redis | 6379 |
| Kafka | 9092 |
| Cassandra | 9042 |
| OpenSearch | 9200 |

---

## Step 3: Set Up platform-core

```bash
cd platform-core

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
```

Edit `.env` with your local configuration:

```env
DATABASE_URL=postgresql://gods:gods_dev_password@localhost:5432/gods_dev
REDIS_URL=redis://localhost:6379/0
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
CASSANDRA_HOSTS=localhost
OPENSEARCH_URL=http://localhost:9200
SECRET_KEY=dev-only-secret-key-change-in-production
ENVIRONMENT=development
OBJECT_STORAGE_URL=file://./local-storage  # Local file storage for dev
HSM_PKCS11_LIB=./hw-bringup/drivers/hsm_pkcs11/emulated/libsofthsm2.so
GOVERNANCE_ENGINE_URL=http://localhost:3001
```

```bash
# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --port 8000
```

Verify: open `http://localhost:8000/health` — should return `{"status": "healthy", ...}`.

---

## Step 4: Set Up Governance Engines

```bash
cd governance-engines

# EVA engine (Python)
cd eva
pip install -r requirements.txt
python main.py &  # Starts on port 3002

# UDOC orchestrator (Python)
cd ../udoc
pip install -r requirements.txt
python main.py &  # Starts on port 3003

# G.O.D.S engine (Node.js)
cd ../gods
npm install
npm start &  # Starts on port 3001

# GIS engine (Node.js)
cd ../gis
npm install
npm start &  # Starts on port 3004
```

---

## Step 5: Set Up a Frontend App

Choose one frontend app to start with. The pattern is identical for all four:

```bash
cd udoc-app  # or seths-app, madiba-app, ts-app

npm install

# Configure the backend URL
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:8000

npm run dev
```

The app will be available at `http://localhost:5173` (default Vite port).

---

## Step 6: Run the Smoke Tests

```bash
cd ..  # Root of repository

# Set the API base URL
export GODS_API_URL=http://localhost:8000

# Run all 31 smoke tests
python smoke_test.py
```

Expected: `31/31 tests passed`. All tests must pass before any development work begins. If any test fails, your environment is not correctly configured — do not proceed until it is resolved.

---

## Development Convenience Commands

A `Makefile` at the root provides convenience commands:

```makefile
make dev          # Start all services in development mode
make test         # Run the full test suite
make smoke        # Run smoke tests only
make migrate      # Run pending database migrations
make lint         # Run linters on all Python and TypeScript code
make format       # Auto-format all code
make clean        # Stop all services and clean temporary files
```

---

## IDE Setup

### VS Code (recommended)
Install the following extensions:
- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- SQLTools + PostgreSQL driver
- Thunder Client (API testing)

Workspace settings (`.vscode/settings.json` is committed):
- Python interpreter: `.venv/bin/python`
- Format on save: enabled
- Ruff as Python linter

### PyCharm
Configure Python interpreter to the `.venv` created in Step 3. The project includes a `pyproject.toml` with tool configuration.

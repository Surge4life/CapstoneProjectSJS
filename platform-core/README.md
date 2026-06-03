# GODS Platform Core (backend)
Sovereign AI governance backend — FastAPI. Real, runnable, tested.

## Run
```bash
pip install -r requirements.txt
python seed.py                       # admin@gods.za / admin123 + model-001
uvicorn app.main:app --reload        # http://localhost:8000/docs
```

## What works (verified by pytest, 8/8)
- JWT auth (bcrypt) + role guards (admin/operator/auditor/client/gov/viewer)
- **UDOC governance path** `/decisions`: EVA 6-D score + sovereignty (SVS=min), sealed
  (HMAC; Dilithium-ref in prod), **fail-closed** for unknown/critical, sub-50ms (≈0.1ms measured)
- **Immutable audit** `/audit`: hash-chained records, chain verification, Merkle root
- **Registry** `/registry`, **Oversight** `/oversight` (human-in-the-loop, Pillar VIII)
- **Divisions**: `/seths` (workforce), `/ts` (production SPVs), `/madiba` (capital recycle loop)
- **UDOC**: `/compliance`, `/bias`, `/sovereignty`, `/intelligence` (closed-loop snapshot), `/admin`

## Honest boundary
SQLite + in-memory bus/audit for dev/emulation; PostgreSQL 16 + Kafka/Redpanda +
Cassandra/WORM in production (interfaces identical, swap via config). HSM/Dilithium are
emulated here and finalised against real hardware in `hw-bringup` + `infra`.

# Task 2 · Operator smoke (surfaces 1–5)

**Updated:** 2026-08-04 · Core automation green

## Before UI checks

1. Open `https://gods-platform-core.onrender.com/health` (wake free tier if cold).
2. Optional: `GET /udoc/demo/ready` (auth) — should report `ready: true` (auto-heals model-001).

## Matrix

### 1 · Sentinel
- URL: `https://gods-platform-core.onrender.com/Sentinel`
- Wait for full UI (bootstrap loads last-good page).
- Run **Smoke** or **Full EVA**.
- **Pass:** biased → **BLOCK**, fair ≠ BLOCK.

### 2 · Client
- URL: Client host (gods-udoc-client).
- Hard-refresh once.
- Login `client@udoc.demo` (or operator).
- **Govern** → Full EVA batch / Biased chip.
- **Pass:** biased → **BLOCK**.

### 3 · Citizen
- URL: `https://gods-udoc-client.onrender.com/citizen.html`
- Submit a challenge.
- **Pass:** receives `case_ref` / status lookup works.

### 4 · Admin
- URL: gods-udoc-admin.
- Hard-refresh **twice** (SW pwa-v8).
- Nav **EIF · Diamond** loads framework.
- **EVA Command** → Full EVA batch.
- **Pass:** biased → **BLOCK** + EIF panel loads.

### 5 · Sector
- URL: gods-udoc-sector.
- **Decisions · EVA** → Run Full EVA batch (uses `/decisions/batch` overlay).
- **Pass:** biased → **BLOCK**.

## Close

Tick all five or attach screenshots to Capstone evidence pack.

**Task 1** remains founder GBS/Canon offline track.

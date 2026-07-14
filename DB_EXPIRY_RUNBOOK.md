# DB_EXPIRY_RUNBOOK — preserve everything before `gods-db` expires (July 3, 2026)

**Situation (from the Render dashboard):** the live PostgreSQL `gods-db` is on the **free** tier and
**Render deletes it on July 3, 2026** unless it is upgraded. `gods-platform-core` stores *all* live
data there — tenants, AI models, EVA decisions, the audit hash-chain, policy packs/versions, API-key
hashes, users, and any loaded G.O.D.S Intelligence corpus. The web/static services are fine; only the
**database** is deleted.

> Nothing here is faked. The backup/restore was verified end-to-end in build: a full export, a
> simulated database loss (all decisions + the entire audit chain wiped), and a clean restore that
> brought every row back, with logins and seals intact. A tampered bundle is refused.

---

## What was built for this (all in this package, all verified)

1. **Full export/restore in the core** (admin-only):
   - `GET /system/backup` → one signed JSON bundle of **every table** (FK-ordered, datetimes preserved).
   - `GET /system/backup/summary` → row counts only (quick check).
   - `POST /system/restore` → loads a bundle into the current database. **Seal is verified first**;
     it is a **dry-run by default** and only wipes + loads with `?confirm=true`. Postgres id
     sequences are realigned automatically after load.
2. **CLI tools** (standard library only — run on any machine):
   - `tools/db_backup.py` — download the bundle from the live core.
   - `tools/db_restore.py` — dry-run, then `--confirm` to restore.
3. **Empty-database bootstrap** — on a brand-new (recreated) database the core auto-creates a single
   admin (`admin@gods.local` / `admin123`, override via `GODS_BOOTSTRAP_PASSWORD`) so you can log in
   and restore **without needing direct database access**. A restore replaces it with your real users.
4. **Blueprint wired as code** — `render.yaml` now declares `gods-db` and wires the core's
   `DATABASE_URL` from it via `fromDatabase`, so if the DB is recreated the connection re-populates
   automatically.

---

## STEP 1 — DO THIS NOW (take a backup while the data is live)

From your machine (the core URL is your live API host):

```bash
python3 tools/db_backup.py \
  --base https://gods-platform-core.onrender.com \
  --email admin@gods.local --password <YOUR_ADMIN_PASSWORD>
```

This writes `gods_backup_<UTC-timestamp>.json` and prints the row counts captured. **Keep this file
safe** — it contains password/key hashes. Re-run any time you want a fresh snapshot (e.g. the night
before July 3). *(The free core sleeps; the tool wakes it and retries login automatically.)*

### Optional belt-and-suspenders — native `pg_dump`
A raw database dump as well, in case you ever want it outside the app:
1. Render → `gods-db` → **Connect** → copy the **External Database URL**.
2. Render → `gods-db` → **Access Control** → add your current IP (or `0.0.0.0/0` temporarily; remove after).
3. Use a **PostgreSQL 18** client (match the server version):
   ```bash
   pg_dump "<EXTERNAL_DATABASE_URL>" -Fc -f gods-db.dump
   ```

---

## STEP 2 — the one setting you MUST preserve: `GODS_SOV_KEY`

Certificate seals, the audit chain, and policy-version signatures are all signed with `GODS_SOV_KEY`.
If that value changes, **previously issued seals stop verifying** (the data restores fine, but old
certificates read as INVALID). Render generates it once and keeps it for the **same service**, so:

- **Do NOT delete the `gods-platform-core` service.** Recreating the *database* is fine; recreating
  the *core service* mints a new key.
- If you ever must recreate the core: first copy the existing `GODS_SOV_KEY` value
  (Render → `gods-platform-core` → **Environment**) and set it explicitly on the new service.
- (`JWT` secret is dev-default; existing login tokens simply expire — harmless.)

---

## STEP 3 — recovery when `gods-db` is gone (on/just after July 3)

Pick ONE path.

### Path A — stay on free (quickest; recurs every ~30 days)
1. **Recreate the database.** Easiest: in Render, re-sync the Blueprint (it will create a fresh
   `gods-db` and auto-wire `DATABASE_URL` into the core). Or create a new free PostgreSQL and set the
   core's `DATABASE_URL` to its **Internal** connection string.
2. **Let the core redeploy.** On boot it creates the tables and a **bootstrap admin** (empty DB).
3. **Restore your data:**
   ```bash
   # dry-run first (changes nothing):
   python3 tools/db_restore.py --base https://gods-platform-core.onrender.com \
     --email admin@gods.local --password admin123 --file gods_backup_XXXX.json
   # then for real (WIPES the bootstrap, loads your data):
   python3 tools/db_restore.py --base https://gods-platform-core.onrender.com \
     --email admin@gods.local --password admin123 --file gods_backup_XXXX.json --confirm
   ```
4. After restore, log in with your **original** admin password (from the backup).
> ⚠ A new free DB will itself expire ~30 days later. Set a calendar reminder, or use Path B.

### Path B — make it permanent (recommended before showing investors)
- **Option B1 — Render paid Postgres:** upgrade `gods-db` to a paid instance (no expiry, daily
  managed backups). In `render.yaml`, change `gods-db`'s `plan:` accordingly. No data move needed if
  you upgrade in place; otherwise restore as in Path A.
- **Option B2 — external free Postgres that doesn't auto-delete (e.g. Neon / Supabase):**
  1. Create a free Postgres there; copy its connection string (includes `sslmode=require`).
  2. In `render.yaml`, **remove the `DATABASE_URL` `fromDatabase` block** and set `DATABASE_URL`
     to that DSN (or set it directly in the core's Environment).
  3. Redeploy the core (tables auto-create), then restore with `tools/db_restore.py --confirm`.
  - Preserve `GODS_SOV_KEY` as in Step 2.

---

## STEP 4 — verify after any restore

```bash
# row counts back to expected:
curl -s -H "Authorization: Bearer <ADMIN_TOKEN>" https://<core>/system/backup/summary
# regulator rollup renders with your systems/decisions:
curl -s -H "Authorization: Bearer <ADMIN_TOKEN>" https://<core>/udoc/regulator/summary
```
Then in the admin console (`/udoc-admin`) or the mobile app: log in as a **client** user (proves
hashes survived), open **Evidence/Replay** on a decision, and **verify a certificate** (proves seals
survived — requires the same `GODS_SOV_KEY`).

---

## Notes / honest caveats
- The backup bundle is **sensitive** (hashes inside). Store it like a secret; don't commit it to git.
- **Intelligence corpus** persists and is included in the backup **only because the core is on
  Postgres**. On ephemeral SQLite it is wiped on every redeploy/sleep regardless — another reason to
  keep a managed/durable DB.
- The app-level backup (`/system/backup`) needs only the **core URL + admin login** — no direct DB
  access. The `pg_dump` path is the only one that needs the external DB URL + IP allow-list.
- This tooling is a portable safety net, **not** a replacement for managed backups on a paid plan.

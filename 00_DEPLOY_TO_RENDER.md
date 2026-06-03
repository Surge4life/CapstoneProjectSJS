# Deploy G.O.D.S to Render — step by step

You have a free Render account. The order is: **GitHub first, then Render Blueprint.**
Render deploys *from* a Git repo, so the code must live on GitHub before Render can build it.

## Part 1 — Put the project on GitHub (one time)

### Option A — GitHub website (no command line)
1. Go to github.com → **New repository** → name it `gods-ecosystem` → **Private** → Create.
2. On the repo page: **Add file → Upload files**.
3. Drag the **contents** of the GODS_ECOSYSTEM folder in (not the zip — unzip first).
   - Skip `node_modules/`, `dist/`, `_packages/`, and `*.db` files (the .gitignore handles
     these for future pushes, but on a manual upload just don't drag them).
4. **Commit changes.** Your code is now on GitHub.

### Option B — Git on your machine (faster for updates later)
```bash
cd GODS_ECOSYSTEM
git init
git add .
git commit -m "G.O.D.S ecosystem initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/gods-ecosystem.git
git push -u origin main
```
(The included .gitignore keeps node_modules/dist/db out automatically.)

## Part 2 — Deploy on Render (one click via the Blueprint)
1. Render Dashboard → **New → Blueprint**.
2. **Connect** your GitHub account, pick the `gods-ecosystem` repo.
3. Render reads `render.yaml` and shows: a Postgres DB + 3 services
   (gods-platform-core, gods-platform-internal, gods-portals).
4. Click **Apply**. Render provisions the database, builds the backend, then the frontends.
   Green checkmarks appear as each comes up.
5. When `gods-platform-core` is live, open its URL and add `/health` — you should see
   `{"status":"ok",...}`. Then `/docs` shows the full API.

## Part 3 — Point the apps at the live backend
Your apps (UDOC/SETHS/MADIBA/TS + portals) have a **connect screen**. On a device:
- Paste your live backend URL: `https://gods-platform-core.onrender.com`
- Connect → sign in (admin@gods.za / admin123) → use it live.
The internal console + portals deployed by the blueprint already point at the backend.

## Free-tier facts to know (so nothing surprises you)
- **Backend sleeps after 15 min idle** → first request after a nap takes ~30s–2min to wake.
  For a demo: hit the URL a minute before you present so it's warm. Upgrade `gods-platform-core`
  to the `starter` plan to remove sleeping.
- **Free Postgres expires after 30 days.** Upgrade `gods-db` to a paid plan before then, or
  the data resets. For a capstone demo this is usually fine; just know it.
- The `seed.py` in the start command re-seeds admin + demo data on each boot, so a fresh DB
  still has a working login.

## Workflow after this
Every `git push` to `main` auto-redeploys the affected services. So future updates =
push to GitHub, Render rebuilds. No manual steps.

## What about Netlify / Vercel?
- Render fits your **full-stack backend** (FastAPI + Postgres) — Netlify/Vercel don't host that well.
- You can keep a frontend on Vercel/Cloudflare Pages if you like, pointed at the Render backend.
- No need to wait for the 25 June Netlify credit reset — Render gives you a live backend now.

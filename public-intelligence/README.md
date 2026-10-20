# G.O.D.S Public Intelligence (Independent Static Site)

**Purpose:** Simple public link for people who found the main Capstone site too dense.  
**Not** the UDOC governance control plane (EVA policy enforcement lives on Render UDOC hosts).

## What it is
- Offline-first curated Q&A + Capstone corpus search
- Optional read-only status probe to `gods-platform-core.onrender.com` (`/health`, `/udoc/demo/ready`)
- Local training log (thumbs up/down) stored in the browser for improving answer presentation over time

## Render service
- Service name: `gods-public-intelligence`
- rootDir: `public-intelligence`
- Static publish: `.` (index.html)
- Independent of UDOC admin/client/operator surfaces

## Training path
Each answer offers **Yes / Needs work**. Feedback is saved in `localStorage` key `gods_public_intel_train_v1` (last 200). Export via browser console:
```js
copy(localStorage.getItem('gods_public_intel_train_v1'))
```
Use exports to refine domain keyword maps and curated sections.

## Separation
| Surface | Role |
|---------|------|
| This site | Public knowledge advisor / investor-friendly Q&A |
| UDOC on Render | Deterministic governance, EVA, policy, audit |
| Capstone Netlify | Full dense project site |

# G.O.D.S ECOSYSTEM — INTERNAL / EXTERNAL NETWORK TOPOLOGY
Boundary model: **network-layer separation** (same backend code, separated by binding +
firewall), with this documented topology. No code fork — the split is operational.

## Two faces per division (and for G.O.D.S itself)
| Surface | Audience | Reachable from | Binds to | Form |
|---|---|---|---|---|
| **Internal consoles** | staff / operators | INSIDE governance network only | `127.0.0.1` / internal NIC | web (browser) |
| **External apps** | students, investors, clients, submitters | OUTSIDE, via gateway | public NIC behind UDOC gateway | PWA / .apk |
| **G.O.D.S internal** | holdings staff | internal network only | internal NIC | web (platform-web) |
| **G.O.D.S external** | public | internet | gateway | web (password-gated) |

## How the boundary is enforced (network layer)
The SAME `platform-core` serves everything; separation is by WHERE it listens and WHAT the
firewall allows — not by forking the code.

1. **Internal bind (network-locked):** internal consoles talk to platform-core bound to the
   internal interface only:
   `uvicorn app.main:app --host 10.0.0.10 --port 8000`   (internal NIC, no public route)
   Firewall: internal subnet (`10.0.0.0/24`) → :8000 ALLOW; everything else DENY.

2. **External edge (gateway):** the UDOC gateway appliance (udoc-gateway/) is the ONLY thing
   with a public address. It reverse-proxies a restricted set of external-safe paths to
   platform-core and drops everything else. External apps hit the gateway, never core directly.
   ```
   internet ──▶ udoc-gateway (public, TLS) ──▶ platform-core (internal only)
                  exposes: /auth, /portal/*, /saas/*, /madiba/engage/*,
                           /ts/submit/*, /documents/*, /health
                  blocks:  /admin, /oversight, /sovereignty, /audit, /analytics,
                           /registry mutations, internal consoles
   ```

3. **Internal-only paths** (admin, oversight, sovereignty, audit, raw analytics) are reachable
   only on the internal bind — the gateway never forwards them, so they are unreachable from
   outside even though they live in the same app.

## Reference NGINX edge (external boundary)
See `infra/edge/nginx.conf` — allow-list of external paths, deny-by-default, TLS termination,
rate limiting. This is the single controlled boundary between outside and the governance network.

## Deployment shapes
- **Dev (one box):** core on `0.0.0.0:8000`, everything reachable (convenience only).
- **Production (sovereign):** core on internal NIC; gateway on edge with the allow-list;
  internal consoles served only on the internal network; external apps point at the gateway URL.

## Honest note
This is the correct, standard way to separate internal/external for one codebase: bind +
firewall + a deny-by-default reverse proxy. It needs real network interfaces/firewall to be
*enforced* in production; here it is fully specified and the NGINX allow-list is real config
you drop onto the edge node.

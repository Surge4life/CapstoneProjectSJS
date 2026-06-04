> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# G.O.D.S INTERNAL OPERATING CORE — ROLE / DIVISION ACCESS MODEL

The G.O.D.S internal core is the single sign-in. On login it calls `/access/profile`, which
computes — server-authoritatively — which of the four internal systems the user may open, and
the launcher shows exactly those. Every console is also enforced by `/access/guard/{system}`
(hard 403), so UI gating is never the only line of defence.

## Internal systems
holdings-overview · seths-ops · madiba-ops · ts-ops · udoc-gov

## Role → access (baseline)
| Role | Opens |
|---|---|
| admin / exec | all five systems |
| operator | overview + division ops (scoped by division) |
| auditor | overview + UDOC governance |
| governance | overview + UDOC governance |
| viewer | overview only |

## Division scoping
A division-bound operator (division ≠ GODS, and not admin/exec/auditor/governance) is
restricted to THEIR division's ops console:
- operator/SETHS → holdings-overview + seths-ops
- operator/TS → holdings-overview + ts-ops
- operator/MADIBA → holdings-overview + madiba-ops

admin/exec/auditor are cross-division by design.

## Enforcement (two layers, server is authoritative)
1. **Launcher** renders only `profile.systems` — users never see systems they can't open.
2. **Guard**: `/access/guard/{system}` returns 403 if not permitted; the console's `Guarded`
   wrapper blocks render, and any direct API call to a division's data still requires the
   relevant role via existing `require_role` dependencies.

## Verified
Profiles + enforcement tested live and in the smoke test (34/34): admin opens all five; a
SETHS operator is scoped to {overview, seths-ops} and is hard-denied udoc-gov (403).

## Honest note
This is real RBAC at the application layer. For enterprise federation (per the assessment),
the same role/division claims would come from Keycloak/OIDC instead of the local JWT — the
access_control logic stays identical; only the token source changes (see infra/IDENTITY.md).

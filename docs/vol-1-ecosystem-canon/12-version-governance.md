# Chapter 12 — Version Governance

## How the G.O.D.S Ecosystem Is Versioned

Version governance is not just about version numbers. It is about ensuring that every deployment knows exactly what it is running, that changes are traceable, and that no version is deployed without proper authorisation.

---

## Version Scheme

The G.O.D.S ecosystem uses **Semantic Versioning** (SemVer) with governance extensions:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+GOVERNANCE_VERSION]

Examples:
  2.1.0              — Stable release
  2.1.0-rc.1         — Release candidate
  2.1.0+GV3          — Stable, with Governance Version 3 policy packs
```

### Version Component Definitions

| Component | Increments When |
|-----------|----------------|
| MAJOR | Constitutional change (changes to pillars, GBS dimensions, or RBAC model) |
| MINOR | New feature, new division capability, new engine |
| PATCH | Bug fix, performance improvement, documentation update |
| PRERELEASE | alpha, beta, rc — not for production |
| GOVERNANCE_VERSION | Policy pack version changes (can change independently of software version) |

### Why MAJOR = Constitutional Change

Most projects increment MAJOR for breaking API changes. G.O.D.S does too — but adds a stronger condition. Any change to the constitutional pillars, the GBS dimensions, or the RBAC core model automatically triggers a MAJOR increment, regardless of whether the API changes.

This is because institutions deploying G.O.D.S make governance commitments based on the constitutional behaviour of a specific version. If the constitutional behaviour changes, that is a major event — even if all the APIs stay the same.

---

## Policy Pack Versioning

Policy packs (GBS rules, threshold configurations) are versioned independently of the software. This allows governance rules to be updated without a software deployment.

Policy packs are versioned as `GV<number>` (Governance Version). Every deployment records its current Governance Version in the operational configuration and in the startup audit log.

When a new Governance Version is deployed, the previous version is retained in the database. Past decisions are permanently linked to the Governance Version that was in effect at the time of the decision.

---

## Release Authorisation

No release is deployed to production without:

1. **CI pipeline passing** — All tests green, all scans clean
2. **Smoke test suite** — 31/31 paths passing
3. **Code review** — At least one senior review for MINOR; two for MAJOR
4. **Governance review** — For any change that affects GBS rules or constitutional behaviour, a governance review by the designated compliance officer is required
5. **Audit record** — The deployment itself is recorded in the audit chain with the deploying individual's identity, the version deployed, and the CI pipeline run reference

---

## Deprecation Policy

| API / Feature Type | Deprecation Notice | End-of-Life |
|-------------------|--------------------|-------------|
| REST API endpoint | 2 MINOR versions | 1 MAJOR version after EOL notice |
| Database schema field | 2 MINOR versions | 1 MAJOR version after EOL notice |
| GBS dimension | Not deprecated — constitutional | N/A |
| Policy rule | Superseded only — old version retained | Never deleted |
| RBAC role | 1 MAJOR version notice | Requires migration guide |

Nothing in the audit chain is ever deprecated. Audit records from version 1.0 must be readable in version 10.0.

---

## Version Compatibility Matrix

Each release publishes a compatibility matrix that specifies:
- Which policy pack versions are compatible with this software version
- Which attachment components (agent/gateway/edge/sidecar) are compatible
- Which frontend app versions are compatible
- Which mobile app versions are compatible

The compatibility matrix is part of the release documentation and is stored in the repository at `docs/compatibility/vX.Y.md`.

---

## Emergency Releases

Emergency (hotfix) releases bypass the normal release schedule but not the authorisation requirements. An emergency release requires:

1. Written justification for the bypass (recorded in the audit chain)
2. Expedited CI pipeline (all smoke tests still pass — no exceptions)
3. Two-person authorisation (cannot be deployed by the person who wrote the fix)
4. Post-incident review within 5 business days

An emergency release that requires disabling smoke tests is not an emergency release — it is an incomplete fix. Fix the tests first.

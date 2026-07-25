# Chapter 02 — Path to Production

## From Current State to Production

Production means: real clients, real data, real governance, real legal obligations. The path from the current state (fully built, deployed to Render, no paying clients) to production requires completing a defined set of prerequisites.

---

## Production Prerequisites

### Legal Prerequisites

| Item | Owner | Dependency |
|------|-------|-----------|
| CIPC registration of G.O.D.S Holdings (Pty) Ltd | Founder | None |
| IP Trust establishment | Founder + attorney | CIPC registration |
| Domain registration (gods.co.za or equivalent) | Entity | CIPC registration |
| Trademark application for G.O.D.S and division marks | Entity + IP attorney | CIPC registration |
| Client service agreement template | Entity + attorney | None (can run in parallel) |
| Privacy policy (POPIA compliant) | Entity + attorney | None |
| Terms of service | Entity + attorney | None |
| Governance disclosure agreement template | Entity + attorney | None |

### Technical Prerequisites

| Item | Status | Effort |
|------|--------|--------|
| Production secrets configuration on Render | Not done | 1 day |
| SSL certificate for production domain | Not done (pending domain) | 1 hour |
| Production database backups configured | Not done | 1 day |
| Audit chain Kafka → Cassandra path live in production | Not done | 2 days |
| Production monitoring configured | Not done | 2 days |
| Third-party security review | Not started | 2–4 weeks |
| Production smoke test suite run against live environment | Not done | 1 day |

### Business Prerequisites

| Item | Notes |
|------|-------|
| First client identified | The first client defines the production use case |
| Client data processing agreement | POPIA requirement |
| Deployment environment agreed | Cloud vs private |
| Onboarding procedure defined | How a new client gets set up |

---

## The First Client Profile

The ideal first client for the G.O.D.S ecosystem has these characteristics:

**Industry:** SETHS division is the most built-out. A skills development organisation, TVET college, or large employer with a graduate recruitment programme is the strongest fit for the first client.

**Size:** Medium — large enough to generate real governance data (1,000+ decisions per month) but small enough for close engagement during the pilot.

**Governance maturity:** The client should understand why governance matters. An organisation that has already faced regulatory scrutiny for bias or unfair practices is an ideal customer — they understand the problem.

**Technical capacity:** The first client does not need in-house technical capacity. G.O.D.S provides the managed service. But they need someone who can understand the governance dashboard and act on oversight cases.

---

## Production Deployment Runbook

```
Day 1: Legal
  Morning:   File CIPC registration documents
  Afternoon: Brief attorney on IP Trust requirements

Day 3-5: Technical setup
  Day 3: Configure production environment variables on Render
  Day 3: Enable Render PostgreSQL automatic backups
  Day 4: Configure external Kafka (Upstash) for production
  Day 4: Configure external Cassandra (DataStax Astra) for production
  Day 5: Run production migration: alembic upgrade head
  Day 5: Run smoke test suite against production URL

Day 7: Security
  Commission third-party security review (2-4 week turnaround)

Day 14+: Client onboarding
  Week 2-3: Draft and execute client service agreement
  Week 3: Set up client tenant in production
  Week 3: Onboard client users (admin + compliance officer)
  Week 3: Register client's first AI model
  Week 4: First live governance decisions
```

---

## Production Readiness Checklist

Before any client data enters the system, all of the following must be complete:

- [ ] CIPC registration filed (or in process with confirmed date)
- [ ] Client data processing agreement signed
- [ ] SSL certificate valid for production domain
- [ ] All production environment variables set
- [ ] Database backups running (verify first backup succeeded)
- [ ] Audit chain live (verify Cassandra receiving records)
- [ ] Smoke tests 31/31 passing against production URL
- [ ] Security review complete (or client has acknowledged pending review with risk acceptance)
- [ ] Monitoring alerts configured (CPU, memory, error rate, governance latency)
- [ ] Incident response procedure documented and tested
- [ ] Data deletion / POPIA subject access request procedure documented
- [ ] At least one G.O.D.S administrator account created in production
- [ ] At least one compliance officer account created in production

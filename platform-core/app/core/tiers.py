"""G.O.D.S six-tier commercial licensing architecture (entitlements + quotas).
Pre-registration: structure is defined; price is set by the founder per engagement (no fabricated pricing)."""
TIERS = {
    "SANDBOX":       {"rank": 0, "name": "Sandbox",       "decision_quota": 200,     "max_models": 2,   "api_keys": 1,   "certificates": False, "async_tiers": False, "cob": False, "blurb": "Open evaluation access."},
    "STARTER":       {"rank": 1, "name": "Starter",       "decision_quota": 5000,    "max_models": 5,   "api_keys": 2,   "certificates": True,  "async_tiers": False, "cob": False, "blurb": "Single-team production."},
    "GROWTH":        {"rank": 2, "name": "Growth",        "decision_quota": 50000,   "max_models": 20,  "api_keys": 5,   "certificates": True,  "async_tiers": True,  "cob": False, "blurb": "Multi-team, async tiers."},
    "ENTERPRISE":    {"rank": 3, "name": "Enterprise",    "decision_quota": 500000,  "max_models": 100, "api_keys": 20,  "certificates": True,  "async_tiers": True,  "cob": True,  "blurb": "Org-wide + COB workflow."},
    "INSTITUTIONAL": {"rank": 4, "name": "Institutional", "decision_quota": 5000000, "max_models": 500, "api_keys": 50,  "certificates": True,  "async_tiers": True,  "cob": True,  "blurb": "Regulator-grade evidence."},
    "SOVEREIGN":     {"rank": 5, "name": "Sovereign",     "decision_quota": -1,      "max_models": -1,  "api_keys": 200, "certificates": True,  "async_tiers": True,  "cob": True,  "blurb": "Sovereign infrastructure; unlimited."},
}
ORDER = ["SANDBOX", "STARTER", "GROWTH", "ENTERPRISE", "INSTITUTIONAL", "SOVEREIGN"]
def tier_info(key: str) -> dict:
    return TIERS.get((key or "SANDBOX").upper(), TIERS["SANDBOX"])

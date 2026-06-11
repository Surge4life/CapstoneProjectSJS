"""
Access control — server-authoritative mapping of role + division → which internal systems
a staff member may open. The G.O.D.S core uses this to decide what to show AND the backend
enforces it (UI gating alone is never trusted).

Internal systems (the four division work environments + governance):
  seths-ops · madiba-ops · ts-ops · udoc-gov · holdings-overview
"""

SYSTEMS = {
    "holdings-overview": {"title": "Holdings Overview", "path": "/overview"},
    "seths-ops":        {"title": "SETHS Operations", "path": "/seths"},
    "madiba-ops":       {"title": "MADIBA Operations", "path": "/madiba"},
    "ts-ops":           {"title": "TS Industries Operations", "path": "/ts"},
    "udoc-gov":         {"title": "UDOC Governance", "path": "/udoc"},
}

# Role → systems baseline (before division scoping).
# admin/exec see everything; auditor sees governance + overview; operator sees ops; viewer overview only.
ROLE_GRANTS = {
    "admin":    set(SYSTEMS.keys()),
    "exec":     set(SYSTEMS.keys()),
    "auditor":  {"holdings-overview", "udoc-gov"},
    "operator": {"holdings-overview", "seths-ops", "madiba-ops", "ts-ops"},
    "governance": {"holdings-overview", "udoc-gov"},
    "gov":      {"holdings-overview", "udoc-gov"},   # COB / governance authority (seed uses role="gov")
    "viewer":   {"holdings-overview"},
}

# Division scoping: a division-bound operator only gets THEIR division's ops console.
DIVISION_SYSTEM = {
    "SETHS": "seths-ops",
    "MADIBA": "madiba-ops",
    "TS": "ts-ops",
    "UDOC": "udoc-gov",
}


def systems_for(role: str, division: str) -> list[dict]:
    """Compute the list of internal systems this user may open."""
    granted = set(ROLE_GRANTS.get(role, {"holdings-overview"}))

    # Division scoping: if the user is bound to a specific division (not GODS) and is NOT
    # admin/exec/auditor, restrict their ops access to that division's system only.
    if division and division != "GODS" and role not in ("admin", "exec", "auditor", "governance", "gov"):
        own = DIVISION_SYSTEM.get(division)
        ops = {"seths-ops", "madiba-ops", "ts-ops", "udoc-gov"}
        granted = (granted - ops) | ({own} if own else set())
        granted.add("holdings-overview")

    out = []
    for key in ["holdings-overview", "seths-ops", "madiba-ops", "ts-ops", "udoc-gov"]:
        if key in granted:
            out.append({"key": key, **SYSTEMS[key]})
    return out


def may_open(role: str, division: str, system_key: str) -> bool:
    return any(s["key"] == system_key for s in systems_for(role, division))

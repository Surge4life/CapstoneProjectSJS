"""
RBAC model — the single source of truth the consoles use to make role permissions VISIBLE and consistently
gated in the UI. Aligned with what the backend already enforces via require_role(...) on sensitive endpoints
(oversight, sovereignty, admin, tenant/role management, sector assignment, system control).

Two axes:
  VIEWS    — which console sections a role may open
  ACTIONS  — which categories of write/destructive operations a role may perform
Server-side enforcement still lives on the endpoints; this surfaces the same model so the UI reflects it
(hidden/locked nav, disabled actions, an explicit permissions matrix) instead of showing everything to everyone.
"""

ALL_VIEWS = ["overview", "systems", "decisions", "policy", "oversight", "audit", "governance",
             "compliance", "sovereignty", "incidents", "intelligence", "tenants", "divisions",
             "sectors", "access", "roles"]

ALL_ACTIONS = ["system.control", "policy.decide", "oversight.act", "tenant.manage",
               "access.manage", "sector.assign", "analysis"]

ACTION_LABEL = {
    "system.control": "Control AI systems (register / suspend / deploy)",
    "policy.decide": "Approve / veto policy (COB)",
    "oversight.act": "Open / resolve oversight cases",
    "tenant.manage": "Manage tenants",
    "access.manage": "Manage users & roles",
    "sector.assign": "Assign tenant sectors",
    "analysis": "Run scans / reports",
}

ROLE_LABEL = {"admin": "Administrator", "exec": "Executive", "gov": "Regulator (Gov)",
              "auditor": "Auditor", "operator": "Operator", "viewer": "Viewer", "client": "Client"}

# role -> permitted views ("*" = all) and action categories
_ROLES = {
    "admin": {"views": "*", "actions": "*", "read_only": False},
    "exec": {
        "views": ["overview", "systems", "decisions", "policy", "oversight", "audit", "governance",
                  "compliance", "sovereignty", "incidents", "intelligence", "tenants", "divisions", "sectors", "roles"],
        "actions": ["system.control", "policy.decide", "oversight.act", "tenant.manage", "sector.assign", "analysis"],
        "read_only": False,
    },
    "gov": {
        "views": ["overview", "decisions", "policy", "oversight", "governance", "compliance",
                  "sovereignty", "intelligence", "sectors"],
        "actions": ["policy.decide", "oversight.act", "analysis"],
        "read_only": False,
    },
    "auditor": {
        "views": ["overview", "decisions", "oversight", "audit", "governance", "compliance", "sovereignty"],
        "actions": ["oversight.act", "analysis"],
        "read_only": False,
    },
    "operator": {
        "views": ["overview", "systems", "decisions", "oversight", "incidents", "divisions"],
        "actions": ["system.control", "oversight.act", "analysis"],
        "read_only": False,
    },
    "viewer": {
        "views": ["overview", "decisions", "governance", "compliance"],
        "actions": [],
        "read_only": True,
    },
    "client": {"views": [], "actions": [], "read_only": True},
}


def _resolve(spec, universe):
    return list(universe) if spec == "*" else [x for x in universe if x in spec]


def permissions_for(role: str) -> dict:
    r = (role or "viewer").lower()
    cfg = _ROLES.get(r, _ROLES["viewer"])
    return {
        "role": r, "label": ROLE_LABEL.get(r, r.title()),
        "views": _resolve(cfg["views"], ALL_VIEWS),
        "actions": _resolve(cfg["actions"], ALL_ACTIONS),
        "read_only": cfg["read_only"],
    }


def matrix() -> dict:
    """Full role -> permission matrix for transparent display."""
    return {
        "views": ALL_VIEWS,
        "actions": ALL_ACTIONS,
        "action_labels": ACTION_LABEL,
        "roles": [permissions_for(r) for r in ("admin", "exec", "gov", "auditor", "operator", "viewer")],
    }

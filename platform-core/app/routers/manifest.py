"""PUBLIC manifest endpoints — informational, no auth required.
Exposes the platform's stack catalog, hardware profile, EVA dimensions,
capabilities, UDOC specification, and IP/patent architecture."""
from fastapi import APIRouter

router = APIRouter(tags=["Manifest"])

# ─── Stack catalog: software + hardware + storage ───────────────────────────

SOFTWARE = [
    {"name": "FastAPI", "role": "API gateway + routing", "visibility": "PUBLIC"},
    {"name": "SQLAlchemy 2.x", "role": "ORM + schema heal", "visibility": "PUBLIC"},
    {"name": "APScheduler", "role": "24/7 conformance scanner cadence", "visibility": "PUBLIC"},
    {"name": "python-jose", "role": "JWT issuance + validation", "visibility": "INTERNAL"},
    {"name": "passlib+bcrypt", "role": "Password hashing (Argon2-ready)", "visibility": "INTERNAL"},
    {"name": "orjson", "role": "High-perf JSON serialization", "visibility": "PUBLIC"},
    {"name": "httpx", "role": "Async outbound HTTP (webhooks, federation)", "visibility": "PUBLIC"},
    {"name": "psycopg 3", "role": "PostgreSQL wire protocol (binary)", "visibility": "INTERNAL"},
    {"name": "uvicorn", "role": "ASGI server (HTTP/1.1 + WebSocket)", "visibility": "PUBLIC"},
]

HARDWARE = [
    {"component": "FPGA", "role": "Opcode execution + policy enforcement", "status": "DESIGNED",
     "capabilities": ["EVA real-time scoring", "StayChain block sealing", "Policy-to-silicon gate"]},
    {"component": "HSM", "role": "Hardware key storage + PQC signing", "status": "DESIGNED",
     "capabilities": ["CRYSTALS-Dilithium signing", "Key ceremony", "Air-gap root of trust"]},
    {"component": "TPM", "role": "Platform attestation + measured boot", "status": "DESIGNED",
     "capabilities": ["Remote attestation", "Sealed storage", "Boot integrity"]},
    {"component": "SmartNIC", "role": "Network-layer sovereignty enforcement", "status": "DESIGNED",
     "capabilities": ["Geo-fence packet filtering", "Wire-speed audit tap", "DPI classification"]},
    {"component": "Cassandra WORM", "role": "Immutable audit log (write-once-read-many)", "status": "DESIGNED",
     "capabilities": ["Hash-chain persistence", "Regulatory retention", "Cross-DC replication"]},
]

# ─── EVA 6-D scoring manifest ──────────────────────────────────────────────

EVA_DIMENSIONS = {
    "formula": "SVS = min(R, Co, DI, JSD_inv, ECS, SPD_inv)",
    "dimensions": [
        {"code": "R", "name": "Reliability", "floor": 0.80, "direction": "higher-is-better"},
        {"code": "Co", "name": "Coherence", "floor": 0.70, "direction": "lower-is-worse"},
        {"code": "DI", "name": "Distributional Integrity", "floor": 0.80, "direction": "higher-is-better"},
        {"code": "JSD", "name": "Jensen-Shannon Divergence", "floor": 0.40, "direction": "lower-is-better"},
        {"code": "ECS", "name": "Ethical Compliance Score", "floor": 0.65, "direction": "higher-is-better"},
        {"code": "SPD", "name": "Statistical Parity Difference", "floor": 0.05, "direction": "lower-abs-is-better"},
    ],
    "svs_gate": 0.60,
    "review_threshold": 0.75,
    "risk_tiers": ["MINIMAL", "LIMITED", "HIGH", "UNACCEPTABLE"],
}

# ─── Divisions + portals ───────────────────────────────────────────────────

DIVISIONS = [
    {"code": "GODS", "name": "Governance Oversight & Decision Systems", "portals": 6},
    {"code": "SETHS", "name": "Secure Ethical Technology & Hypervisor Systems", "portals": 6},
    {"code": "MADIBA", "name": "Market Analytics & Development Investment Bureau", "portals": 6},
    {"code": "TS", "name": "Technology & Strategy", "portals": 6},
]

# ─── UDOC specification (grounded in GODS_UDOC_Full_Specification v1.0) ────

UDOC_SPEC = {
    "full_name": "Unified Digital Oversight & Coordination",
    "version": "9.3",
    "hardware_planes": ["FPGA Execution", "HSM Key Store", "TPM Attestation", "SmartNIC Sovereignty", "Cassandra WORM Audit"],
    "deployment_packages": ["Sovereign Cloud (full)", "Enterprise On-Prem", "Edge Compact", "Air-Gapped Classified"],
    "edge_classes": ["Mobile (APK)", "Browser (PWA)", "IoT Gateway", "Field Terminal"],
    "key_architecture": {"algorithm": "CRYSTALS-Dilithium", "type": "PQC (post-quantum)", "ceremony": "HSM-rooted"},
    "rollout_phases": [
        {"phase": 1, "period": "2024-2025", "milestone": "Software MVP + pilot"},
        {"phase": 2, "period": "2025-2026", "milestone": "Hardware integration + compliance certification"},
        {"phase": 3, "period": "2026-2028", "milestone": "Multi-tenant SaaS + federation"},
        {"phase": 4, "period": "2028-2032", "milestone": "National-scale deployment"},
        {"phase": 5, "period": "2032-2036", "milestone": "Global sovereignty mesh"},
    ],
    "software_routers": 12,
    "specification_sections": 18,
    "constitutional_pillars": 12,
}

# ─── IP / Patent architecture (grounded in Patent_full_updated.png v9.2) ──

UDOC_PATENTS = {
    "instrument_version": "9.2",
    "governance_stack_layers": 8,
    "key_embodiments": [
        {"fig": 21, "title": "AI Governance Hypervisor", "patent_ref": "ZA-UDOC-001"},
        {"fig": 22, "title": "Policy-to-Silicon Pipeline", "patent_ref": "ZA-UDOC-008"},
        {"fig": "23/30", "title": "Federated Governance Mesh", "patent_ref": "ZA-UDOC-005"},
        {"fig": 24, "title": "Air-Gapped Sovereignty Module", "patent_ref": "ZA-UDOC-006"},
        {"fig": 29, "title": "Post-Quantum Cryptographic Layer", "patent_ref": "ZA-UDOC-009"},
        {"fig": 33, "title": "Edge Governance Terminal", "patent_ref": "ZA-UDOC-010"},
    ],
    "core_claims": [15, 38, 39],
    "eva_formula": "SVS = min(R, Co, DI, JSD_inv, ECS, SPD_inv)",
    "fpga_opcodes": True,
    "staychain": True,
    "claim_hierarchy": {"categories": ["A — System Architecture", "B — Method Claims", "C — Apparatus Claims"]},
    "jurisdiction": "ZA (South Africa) + PCT international phase",
    "uspto_defense": "Section 101 — technical improvement (hardware-rooted governance)",
}

# ─── Endpoints ─────────────────────────────────────────────────────────────

@router.get("/catalog")
def catalog():
    """Full stack catalog: software, hardware, and per-component capabilities."""
    return {"software": SOFTWARE, "hardware": HARDWARE,
            "total_software": len(SOFTWARE), "total_hardware": len(HARDWARE)}


@router.get("/hardware")
def hardware():
    """Hardware self-test status for the 5 sovereign components."""
    return {"components": HARDWARE, "total": len(HARDWARE),
            "note": "Status reflects design-phase readiness; production attestation via TPM + HSM ceremony."}


@router.get("/eva/manifest")
def eva_manifest():
    """EVA 6-D scoring dimensions, floors, SVS gate, and risk tier taxonomy."""
    return EVA_DIMENSIONS


@router.get("/platform/capabilities")
def platform_capabilities():
    """Full platform vision: divisions, portals, compliance basis."""
    return {
        "system": "G.O.D.S — Governance Oversight & Decision Systems",
        "udoc": "Unified Digital Oversight & Coordination",
        "divisions": DIVISIONS,
        "total_portals": 24,
        "compliance_basis": ["EU AI Act (Art. 6/9/72)", "SA NAIFP", "POPIA", "King IV"],
        "governance_model": "EVA 6-D + UDOC sovereignty, fail-closed for critical",
    }


@router.get("/udoc/specification")
def udoc_specification():
    """UDOC specification summary (grounded in GODS_UDOC_Full_Specification v1.0)."""
    return UDOC_SPEC


@router.get("/ip/patents")
def ip_patents():
    """Patent architecture summary (grounded in Patent_full_updated.png v9.2)."""
    return UDOC_PATENTS

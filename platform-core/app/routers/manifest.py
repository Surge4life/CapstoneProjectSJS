"""
G.O.D.S / UDOC — public manifest endpoints.
Surfaces the live stack (9 software + hardware), the EVA engine spec, and the
full platform capability set so users can SEE the depth of the platform.
All read-only and public (no auth) — they describe the architecture, they do not act on it.
Grounded in the real repo: render.yaml services, hw-bringup drivers, EVA/SVS model, sectors.py.
"""
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["manifest"])
_now = lambda: datetime.now(timezone.utc).isoformat()

# ── 9 software services (public/private/internal + per-role user actions) ──
SOFTWARE = [
    {"service": "gods-platform-core", "name": "Platform Core API", "kind": "Python / FastAPI", "visibility": "PRIVATE",
     "role": "The governance brain — EVA 6-D engine, SVS sovereignty, the 24/7 Sentinel, oversight, registry and the Merkle audit chain.",
     "public_endpoints": ["/health", "/version", "/admin", "/catalog", "/hardware", "/eva/manifest", "/platform/capabilities"],
     "user_actions": {
         "admin": ["evaluate decisions", "register/block models", "run·pause·resume Sentinel", "resolve oversight", "manage tenants & users"],
         "exec": ["evaluate decisions", "run Sentinel", "resolve oversight", "view everything"],
         "operator": ["run portal actions", "submit division actions", "view own division"],
         "auditor": ["read decisions", "verify the audit chain", "read conformance"],
         "viewer": ["read-only dashboards"],
         "client": ["view own tenant's systems, decisions & sector compliance"]}},
    {"service": "gods-udoc-web", "name": "UDOC Web", "kind": "Static", "visibility": "PUBLIC",
     "role": "Public-facing UDOC surface describing the platform and its governance model.",
     "user_actions": {"public": ["browse the platform overview"]}},
    {"service": "gods-udoc-gateway", "name": "UDOC SSO Gateway", "kind": "Static", "visibility": "PUBLIC",
     "role": "Single sign-on entry point that routes a signed-in user to the right console for their role.",
     "user_actions": {"all": ["sign in", "be routed to the correct console"]}},
    {"service": "gods-udoc-admin", "name": "UDOC Admin Console", "kind": "Static", "visibility": "PRIVATE",
     "role": "Administrative governance dashboard — decisions, oversight, policy, audit, RBAC and sector tooling.",
     "user_actions": {"admin": ["full administrative control"], "exec": ["governance operations"]}},
    {"service": "gods-udoc-operator", "name": "UDOC Operator Console", "kind": "Static", "visibility": "PRIVATE",
     "role": "Sovereign-Operator workspace — live tiles and the authorised actions behind each operator profile.",
     "user_actions": {"operator": ["run the actions authorised for their profile"]}},
    {"service": "gods-udoc-client", "name": "UDOC Client Console", "kind": "Static", "visibility": "PRIVATE",
     "role": "Tenant-facing view — a client's own registered systems, decisions and sector compliance.",
     "user_actions": {"client": ["view their own organisation only"]}},
    {"service": "gods-portals", "name": "24 Sovereign-Operator Portals", "kind": "Static", "visibility": "PRIVATE",
     "role": "The 24 institutional portals (Governance · Operations · People · Business), each enterable with its own controls.",
     "user_actions": {"admin": ["enter all portals"], "operator": ["enter & control their portal"]}},
    {"service": "gods-platform-internal", "name": "Platform Internal", "kind": "Static", "visibility": "INTERNAL",
     "role": "Internal G.O.D.S Holdings console spanning the four divisions.",
     "user_actions": {"admin": ["internal operations"], "exec": ["internal operations"]}},
    {"service": "gods-db", "name": "Governance Database", "kind": "PostgreSQL", "visibility": "INTERNAL",
     "role": "The live datastore for users, decisions, conformance, oversight and the audit chain.",
     "user_actions": {"system": ["bound to platform-core only — no external access"]}},
]

# ── hardware layer: 4 sovereignty components + the WORM datastore ──
HARDWARE = [
    {"component": "FPGA", "name": "FPGA-over-PCIe accelerator", "visibility": "PRIVATE", "driver": "fpga_pcie",
     "function": "Hardware-accelerated EVA inference and cryptographic offload.", "controls": ["self-test", "bind/unbind"],
     "production": "real PCIe device; emulated in this deployment"},
    {"component": "HSM", "name": "Hardware Security Module (PKCS#11)", "visibility": "PRIVATE", "driver": "hsm_pkcs11",
     "function": "Dual-custody signing of the audit Merkle root — the private key never leaves the HSM.", "controls": ["self-test", "sign root"],
     "production": "real PKCS#11 HSM; emulated in this deployment"},
    {"component": "TPM", "name": "Trusted Platform Module", "visibility": "PRIVATE", "driver": "tpm",
     "function": "Measured boot and platform attestation for tamper-evidence.", "controls": ["attest", "self-test"],
     "production": "real TPM; emulated in this deployment"},
    {"component": "NIC", "name": "Sovereignty-inspection NIC", "visibility": "PRIVATE", "driver": "nic_inspect",
     "function": "Inspects BGP / traceroute / DNSSEC to verify data-path sovereignty — feeds the SVS.", "controls": ["self-test", "path scan"],
     "production": "real NIC; emulated in this deployment"},
    {"component": "Cassandra-WORM", "name": "Cassandra WORM nodes", "visibility": "INTERNAL", "driver": "cassandra",
     "function": "Write-once, Merkle-linked audit storage — the immutable evidence chain.", "controls": ["health", "verify chain"],
     "production": "clustered WORM nodes in production"},
]

# ── EVA — 6 evaluation dimensions + SVS sovereignty gate ──
EVA_DIMENSIONS = [
    {"key": "validity", "name": "Validity", "evaluates": "Is the decision well-formed, in-policy and within the model's declared scope?", "floor": 0.60},
    {"key": "confidence", "name": "Confidence", "evaluates": "Calibrated certainty of the model's output (raw confidence, adjusted for context).", "floor": 0.60},
    {"key": "risk", "name": "Risk", "evaluates": "Severity tier of the use-case and potential harm.", "floor": None, "note": "higher risk tightens every other floor"},
    {"key": "compliance", "name": "Compliance", "evaluates": "Conformance to POPIA / FICA / FSCA and the applicable sector frameworks.", "floor": 0.60},
    {"key": "stability", "name": "Stability", "evaluates": "Bias and drift — Statistical Parity Difference (SPD) across privileged/unprivileged groups.", "floor": None, "note": "SPD must stay within tolerance"},
    {"key": "impact", "name": "Impact", "evaluates": "Scope and reversibility of the decision's effect on people and institutions.", "floor": 0.60},
]
SVS = {"name": "Sovereignty Verification Score (SVS)",
       "gates": "Every decision must clear the sovereignty floor or it is BLOCKED regardless of the EVA scores.",
       "inputs": ["ECS (egress control)", "BGP path", "traceroute", "DNSSEC", "data-storage locality"], "floor": 0.60}

DIVISIONS = [
    {"key": "UDOC", "name": "UDOC", "role": "Sovereign AI-governance SaaS — the technical & IP centrepiece."},
    {"key": "SETHS", "name": "S.E.T.H.S", "role": "Workforce reintegration programme (SAQA 118707, NQF5)."},
    {"key": "TS", "name": "T.S Industries", "role": "Production & infrastructure SPVs."},
    {"key": "MADIBA", "name": "M.A.D.I.B.A Capital", "role": "Impact investment & capital recycling (>50% per Constitutional Pillar 2)."},
]


@router.get("/catalog", summary="Full stack catalog — 9 software + hardware, public/private, capabilities & per-role user actions")
def catalog():
    return {"generated": _now(), "visibility_model": ["PUBLIC", "PRIVATE", "INTERNAL"],
            "software": SOFTWARE, "hardware": HARDWARE,
            "counts": {"software": len(SOFTWARE),
                       "hardware": len([h for h in HARDWARE if h["component"] != "Cassandra-WORM"]),
                       "datastore": 1}}


@router.get("/hardware", summary="Hardware layer status — FPGA · HSM · TPM · NIC · Cassandra WORM")
def hardware():
    return {"generated": _now(), "components": HARDWARE,
            "self_test": "hw-bringup/selftest/udoc_selftest.py",
            "note": "Sovereignty hardware is emulated in this deployment; real PCIe / PKCS#11 / TPM in production."}


@router.get("/eva/manifest", summary="EVA engine manifest — 6 dimensions, mandatory floors and SVS gating")
def eva_manifest():
    return {"engine": "EVA — Evaluating Valiant Algorithms", "generated": _now(),
            "dimensions": EVA_DIMENSIONS, "sovereignty": SVS,
            "decision": {"outcomes": ["APPROVE", "BLOCK"],
                         "sealing": "HMAC-sealed verdict, hash-chained into the Merkle audit ledger, with the root HSM-signed."},
            "risk_tiers": ["MINIMAL", "NOTABLE", "MEDIUM", "HIGH", "UNACCEPTABLE"]}


@router.get("/platform/capabilities", summary="Platform capability manifest — the full UDOC vision & four divisions")
def platform_capabilities():
    return {"platform": "UDOC — Sovereign AI Governance · G.O.D.S Holdings (PROPOSED)", "generated": _now(),
            "capabilities": [
                "6-dimensional EVA evaluation", "Sovereignty Verification (SVS)", "24/7 Sentinel conformance scanning",
                "Merkle-linked, hash-chained audit ledger", "Human-in-the-Loop (HITL) oversight",
                "Post-quantum cryptography (CRYSTALS-Kyber / Dilithium)", "HSM dual-custody signing",
                "24 sovereign-operator portals", "Multi-tenant SaaS with public/private sector scoping",
                "Hardware-rooted trust (FPGA · HSM · TPM · NIC)"],
            "divisions": DIVISIONS,
            "compliance_basis": ["SA National AI Policy (GG 54477)", "POPIA", "FICA", "FSCA",
                                 "Constitutional Pillars III · VI · VIII · XI"],
            "portals": 24, "embedded_specs": ["/eva/manifest", "/catalog", "/hardware", "/udoc/specification", "/ip/patents"]}


# ── UDOC full specification — grounded in GODS_UDOC_Full_Specification.docx (v1.0) ──
UDOC_SPEC = {
    "document": "UDOC — Full Hardware & Software Specification",
    "udoc": "Unified Digital Oversight & Coordination",
    "owner": "G.O.D.S Holdings (Pty) Ltd · Johannesburg, South Africa (PROPOSED)",
    "version": "v1.0", "classification": "CONFIDENTIAL",
    "objective": "Make AI governance impossible to bypass by policy alone — governance is technically embedded into the infrastructure stack and enforced at hardware level.",
    "deployment_models": ["National backbone", "Sovereign in-country cloud", "Private enterprise", "Edge / air-gapped"],
    "non_negotiable_constraints": [
        "Sovereign-critical data processable fully air-gapped — no public-cloud dependency",
        "Every significant AI event yields an immutable, cryptographically verifiable audit + lineage record",
        "High-risk/critical AI enforces mandatory human oversight, suspension and override logging",
        "Governance path adds sub-50 ms latency on synchronous enforcement",
        "Primary key material stays in client-controlled HSMs; support access temporary, authorised, logged",
        "99.9% uptime (enterprise) / 99.95% (government backbone)",
        "Signed, offline-capable release pipelines for air-gapped estates",
        "Pillar VII — no single operator holds both signing authority and audit write access (HSM dual-custody)"],
    "hardware_planes": [
        {"plane": "Embedded Governance Fabric", "functions": "SDK gateways, sidecars, host agents, branch appliances, model-registration hooks"},
        {"plane": "Ingestion & Control Plane", "functions": "API ingress, mTLS termination, Kafka brokers, schema registry, admission control"},
        {"plane": "Governance & Processing Core", "functions": "FastAPI services, policy engine, explainability, bias engine, workflow, oversight queue"},
        {"plane": "Immutable Data Operations Core", "functions": "PostgreSQL, Cassandra/WORM, Redis, OpenSearch, object archive"},
        {"plane": "Security & Operations Plane", "functions": "HSM, vault, bastion, SIEM, Prometheus/Grafana, secure update vault"}],
    "deployment_packages": ["UDOC Agent (host process)", "UDOC Sidecar (container)", "UDOC Gateway (mTLS/lineage appliance)", "UDOC Edge Node (1- or 3-node sovereign-local cluster)"],
    "edge_classes": ["Compact Edge", "Standard Edge", "Resilient Edge Trio"],
    "key_architecture": {
        "hsm": "2 network-attached HSMs per site; FIPS 140-3 L3 (govt) / FIPS 140-2 L2 (enterprise)",
        "hierarchy": "master key (HSM) → KEK → DEK → per-session; split-custody master-key activation",
        "signing": "separate signing service; private keys never leave the HSM",
        "pqc": "hybrid TLS 1.3 (classical + PQC); CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium (signatures), SPHINCS+ (long-term archive)",
        "transparency": "Merkle roots published to a regulator-visible key registry where policy permits"},
    "rollout_phases": [
        {"phase": 1, "timeline": "Months 1–12", "milestone": "Secure build enclave, K8s control plane, PostgreSQL cluster, Kafka, governance workers, PQC"},
        {"phase": 2, "timeline": "Months 10–24", "milestone": "Cassandra immutable audit, object archive, OpenSearch, HSM signing, Cloud QPU API"},
        {"phase": 3, "timeline": "Months 22–48", "milestone": "Secondary site, edge nodes, DR testing, on-prem QPU (100+ qubits), full quantum sovereignty"},
        {"phase": 4, "timeline": "Months 38–72", "milestone": "SADC quantum network (AQGN), 10+ sovereign UDOC nodes via QKD, M.A.D.I.B.A scale-out"},
        {"phase": 5, "timeline": "Months 55–120", "milestone": "Fault-tolerant quantum (1000+ logical qubits), global architecture licensing, continental AI governance"}],
    "software_manifest": {
        "backend": "FastAPI governance engine — each router enforces a constitutional pillar obligation",
        "routers": [
            {"endpoint": "/auth", "function": "JWT login, refresh, role assignment"},
            {"endpoint": "/audit", "function": "Immutable tamper-evident AI decision audit log (HMAC, Cassandra-backed)"},
            {"endpoint": "/bias", "function": "Intersectional bias detection (continuous 24h cycle)"},
            {"endpoint": "/compliance", "function": "Constitutional Pillar compliance sweeps (all 12 pillars)"},
            {"endpoint": "/decisions", "function": "AI decision capture + human confirmation (Pillar VIII)"},
            {"endpoint": "/registry", "function": "AI system / model registry (register before deployment)"},
            {"endpoint": "/sovereignty", "function": "Data-sovereignty verification — zero foreign transit"},
            {"endpoint": "/oversight", "function": "Human oversight queue + COB notification"},
            {"endpoint": "/lineage", "function": "Merkle-linked data lineage & provenance"},
            {"endpoint": "/workforce", "function": "S.E.T.H.S workforce-AI governance loop"},
            {"endpoint": "/admin", "function": "COB administrative interface (COB access only)"},
            {"endpoint": "/health", "function": "Platform & sovereignty health"}]},
    "sections": ["1 Executive Design Brief", "2 Non-Negotiable Constraints", "3 Reference Deployment Architecture", "4 Hardware Architecture — Five Planes",
        "5 Node Classes & Bill of Materials", "6 Data Operations Core", "7 Embedded Governance Fabric", "8 Network, Security & Sovereign Key Architecture",
        "9 Reference Rack Layout", "10 Facility, Power, Cooling & Physical Security", "11 Availability & Disaster Recovery", "12 Capacity Tiers & Phased Rollout",
        "13 UDOC Software Platform — Full Component Manifest", "14 Data Classification → Hardware Treatment Map", "15 Storage, Backup, Archive & Retention",
        "16 Acceptance Criteria & Operational Readiness", "Appendix A — Procurement Notes", "Appendix B — Platform File Structure"],
    "constitutional_basis": "12 Constitutional Pillars enforced at hardware level — Pillar III (sovereign respect, zero foreign transit), Pillar VII (dual-custody), Pillar VIII (mandatory human confirmation)"
}


@router.get("/udoc/specification", summary="The full UDOC hardware + software specification — embedded, machine-readable")
def udoc_specification():
    return UDOC_SPEC


# ── UDOC patent instrument — grounded in the v9.2 sovereign-architecture filing ──
UDOC_PATENTS = {
    "instrument": "UDOC Sovereign AI Governance Infrastructure — Patent Instrument",
    "version": "v9.2", "supersedes": "all prior versions v1–v9.x",
    "classification": "Attorney Work Product — STRICTLY CONFIDENTIAL — not legal advice",
    "jurisdiction": "ZA (South Africa) · ZA-UDOC reference series; USPTO §101 defense templates prepared",
    "prosecution_ready_claim_hierarchy": {
        "reference": "ZA-UDOC-001",
        "categories": ["A — Deterministic Governance System", "B — Hardware-Governed AI Infrastructure", "C — Sovereign Execution Authorization Architecture"],
        "uspto_101_defense": ["Counter-Anchoring", "Anchoring", "Technical Evidence"]},
    "eight_layer_governance_stack": [
        "L1 — Sovereign Subsystem (Quantum-Resilient Core, QSDB, ethical-alignment private enclave)",
        "L2 — Governance Hypervisor Layer (Type-1 microkernel below the OS)",
        "L3 — EVA Arbitration Layer (six-dimensional scoring + supervisor arbitration mesh)",
        "L4 — Hardware & Execution Layer (FPGA enforcement lattice, HSM, QPU pre-processing)",
        "L5 — Sur²Secure Enclave Layer (digital-bunker PMP, TOR/NAPOT, hourly G_VERIFY)"],
    "key_embodiments": [
        {"id": "21", "name": "Governance Hypervisor Layer", "claim": "Claim 39", "detail": "Type-1 microkernel governance below the OS; intercepts all privileged instructions and evaluates against the MFCM check before resume."},
        {"id": "22", "ref": "ZA-UDOC-008", "name": "Policy-to-Silicon Compiler", "detail": "Legal text ingestion (POPIA obligations) → HDL synthesis (Verilog/VHDL) → FPGA bitstream → formal verification → Dilithium-signed authenticated deployment."},
        {"id": "23 & 30", "ref": "ZA-UDOC-005", "name": "Federated & Multi-Jurisdiction Sovereign Governance Mesh", "detail": "ZA / AU / BRICS / treaty logic encoded as MFCM checks; ZK-1/ZK-2/ZK-3 proofs."},
        {"id": "24", "ref": "ZA-UDOC-006", "name": "Air-Gapped Defense Node", "detail": "Local offline sovereignty via G_SOV_VERIFY + G_SYNC."},
        {"id": "29", "name": "PQC Transition Node", "detail": "QPU/QPUB reservation, Zero-Trust boundary."},
        {"id": "33", "name": "Edge Sovereign Defense Node"}],
    "core_claims": [
        "Claim 15 — 14-stage deterministic sovereign execution sequence (Axiom Register → Policy Cell array → Telemetry-Loss detection → nanosecond-precision timestamping → fail-closed)",
        "Claim 38 — FPGA enforcement lattice (128 axioms, silicon gates, reconfigurable policy cells)",
        "Claim 39 — Governance hypervisor intercept-and-evaluate"],
    "six_dimensional_eva": {
        "formula": "SVS = min(V, Cf, R, Co, S, I)",
        "dimensions": "Validity (G_ATTEST), Confidence (temperature scaling), Risk (SA-Tier map), Compliance (MFCM 47-check, <6 ms), Stability (JSD drift, <1 ms), Impact (<3 ns)",
        "mandatory_block_overrides": "G_LOCK + FAIL_CLOSED at R≥0.8, Co<0.7, DI<0.8, JSD≥0.40, ECS<0.65 — enforced via HQ-OS BFT consensus"},
    "fpga_opcode_set": ["G_SOV_VERIFY", "G_HALT (CPU freeze)", "G_lock_out (HSM-NVRAM lock, persists across reboots)", "Relay_control (hardware relay OPEN on failure)"],
    "staychain": "StayChain™ private blockchain — dual-path audit (fast-path classical WORM Cassandra + secure-path blockchain), PQC CRYSTALS-Dilithium signatures, SPHINCS+ archive, BFT witness-node consensus",
    "governance_before_execution": "G_SOV_VERIFY custom opcode → SVS = min() → hardware relay disconnection in <1 ms",
    "degraded_modes": "Five degraded operating modes; 13-state fail-closed state machine",
    "note": "Patent specifics are confidential attorney work product; this manifest summarises the architecture, not the legal claims verbatim."
}


@router.get("/ip/patents", summary="UDOC patent instrument (v9.2) — embodiments, claims & sovereign architecture")
def ip_patents():
    return UDOC_PATENTS

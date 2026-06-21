"""
G.O.D.S / UDOC — StayChain dual-path audit (patent v9.2, Part 8.1 / Fig 3).

StayChain is the patent's immutable audit design: a DUAL-PATH log where every governance
event is written to (a) a classical WORM fast-path and (b) a blockchain secure-path with
post-quantum signatures, witnessed by BFT nodes and archived under a hash-based scheme.

This router does NOT invent a second audit log. It READS the real, already-running
hash-chained audit (app.services.audit_writer / AuditRef) and presents it in StayChain's
dual-path block form, reusing the real verify_chain() and merkle_root(). What it adds over
the existing /audit endpoints is the patent's block-level view and the dual-path / witness
framing that /audit does not expose.

HONESTY: the SHA-256 hash chain and the Merkle root are REAL (computed over real rows). The
"WORM fast-path", "blockchain secure-path", "BFT witness consensus", "Dilithium signature"
and "SPHINCS+ archive" are the patent's production design — here they are EMULATED / named
placeholders, not a live Cassandra cluster, real BFT quorum, or real lattice signatures.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import hashlib

from app.db.session import get_db
from app.db.models import AuditRef
from app.services.audit_writer import verify_chain, merkle_root
from app.core.dependencies import require_role

router = APIRouter(prefix="/staychain", tags=["UDOC StayChain audit"])
_now = lambda: datetime.now(timezone.utc).isoformat()

# Dual-path design (Part 8.1). 4 BFT witnesses → quorum 3 (tolerate 1 fault).
WITNESS_NODES = ["ZA-JHB-01", "ZA-CT-02", "ZA-PTB-03", "ZA-DBN-04"]
BFT_QUORUM = 3


def _witness_consensus(block_hash: str) -> dict:
    """Emulated BFT witness attestation: deterministic per-block, quorum-checked."""
    votes = []
    for node in WITNESS_NODES:
        # deterministic 'attestation' so the same block always yields the same result
        h = hashlib.sha256(f"{node}:{block_hash}".encode()).hexdigest()
        votes.append({"node": node, "attests": True, "sig": h[:16]})
    agree = sum(1 for v in votes if v["attests"])
    return {"witnesses": votes, "agree": agree, "quorum": BFT_QUORUM,
            "consensus": agree >= BFT_QUORUM}


def _block_view(r: AuditRef) -> dict:
    """Present one real audit row as a StayChain block."""
    return {
        "height": r.seq,
        "block_hash": r.event_hash,
        "prev_hash": r.prev_hash,
        "event_type": r.event_type,
        "classification": r.classification,
        "actor_class": r.actor_class,
        "secure_path": {
            "chain": "StayChain (blockchain secure-path)",
            "dilithium_sig_ref": r.dilithium_ref or f"dil-ref-{r.seq}",
            "pqc": "CRYSTALS-Dilithium3 (emulated placeholder)",
        },
        "fast_path": {"store": "Cassandra WORM (emulated)", "append_only": True},
        "witness_consensus": _witness_consensus(r.event_hash),
        "timestamp": r.created_at.isoformat() if r.created_at else None,
    }


@router.get("/status")
def staychain_status():
    """Public: the StayChain dual-path architecture (Part 8.1). Describes; does not act."""
    return {
        "name": "StayChain — dual-path immutable audit",
        "patent_ref": "v9.2 Part 8.1 / Fig 3",
        "fast_path": {
            "store": "Classical WORM (Cassandra)", "role": "Low-latency append-only write",
            "status": "emulated in this deployment",
        },
        "secure_path": {
            "store": "Private blockchain (StayChain)", "role": "Tamper-evident chained blocks",
            "signatures": "CRYSTALS-Dilithium (PQC)", "status": "emulated; SHA-256 chain is real",
        },
        "witness_nodes": WITNESS_NODES,
        "bft_quorum": f"{BFT_QUORUM}/{len(WITNESS_NODES)} (tolerate 1 fault)",
        "archive": "SPHINCS+ hash-based long-term archive (emulated)",
        "real_vs_emulated": "SHA-256 hash chain + Merkle root are REAL; WORM/blockchain/"
                            "witness/Dilithium/SPHINCS+ are the production design, emulated here.",
        "endpoints": {
            "GET /staychain/verify": "Verify chain integrity + Merkle root + witness consensus (auth).",
            "GET /staychain/blocks": "Recent StayChain blocks (auth).",
            "GET /staychain/block/{height}": "One StayChain block by height (auth).",
        },
        "generated_at": _now(),
    }


@router.get("/verify")
def staychain_verify(db: Session = Depends(get_db),
                     _=Depends(require_role("auditor", "admin"))):
    """Consolidated StayChain verification over the REAL audit chain: hash-chain integrity
    (verify_chain), Merkle root, dual-path status, and BFT witness consensus on the head."""
    chain = verify_chain(db)          # real: {records, intact, broken_at, head}
    root = merkle_root(db)            # real Merkle root
    head = chain.get("head")
    witness = _witness_consensus(head) if head and head != "0" * 64 else {
        "witnesses": [], "agree": 0, "quorum": BFT_QUORUM, "consensus": False}
    return {
        "chain_intact": chain["intact"],
        "height": chain["records"],
        "broken_at": chain["broken_at"],
        "head_hash": head,
        "merkle_root": root,
        "fast_path_status": "WORM append-only — consistent (emulated)",
        "secure_path_status": "blockchain chained — verified" if chain["intact"]
                              else f"BROKEN at height {chain['broken_at']}",
        "witness_consensus": witness,
        "tamper_evident": chain["intact"] and witness["consensus"],
        "note": "Hash chain + Merkle root are real; WORM/witness/PQC are emulated.",
        "generated_at": _now(),
    }


@router.get("/blocks")
def staychain_blocks(limit: int = 20, db: Session = Depends(get_db),
                     _=Depends(require_role("auditor", "admin"))):
    """Recent StayChain blocks (newest first), presented from the real audit rows."""
    limit = max(1, min(limit, 100))
    rows = db.execute(select(AuditRef).order_by(AuditRef.seq.desc()).limit(limit)).scalars().all()
    total = db.execute(select(func.count(AuditRef.id))).scalar() or 0
    return {
        "height": total,
        "returned": len(rows),
        "blocks": [_block_view(r) for r in rows],
        "merkle_root": merkle_root(db),
        "generated_at": _now(),
    }


@router.get("/block/{height}")
def staychain_block(height: int, db: Session = Depends(get_db),
                    _=Depends(require_role("auditor", "admin"))):
    """One StayChain block by height (= audit seq), with witness consensus and link proof."""
    r = db.execute(select(AuditRef).where(AuditRef.seq == height)).scalar_one_or_none()
    if not r:
        raise HTTPException(404, f"no StayChain block at height {height}")
    prev = db.execute(select(AuditRef).where(AuditRef.seq == height - 1)).scalar_one_or_none()
    block = _block_view(r)
    block["link_proof"] = {
        "links_to_prev": r.prev_hash == (prev.event_hash if prev else "0" * 64),
        "prev_height": prev.seq if prev else 0,
    }
    block["generated_at"] = _now()
    return block

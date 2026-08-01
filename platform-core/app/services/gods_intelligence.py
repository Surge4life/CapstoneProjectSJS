"""
G.O.D.S Intelligence — the internal, self-contained knowledge + governance brain.

Honest scope (pre-registration): this is a corpus-grounded institutional intelligence that
reasons ONLY over the G.O.D.S archive (the digital data room). Add/remove a document and the
system's knowledge updates immediately ("training" = curating the indexed corpus). It is
INTERNAL ONLY — never exposed to SaaS clients — and is hard-wired to the Constitutional Doctrine
(Pillar VIII · Human Primacy), which cannot be overridden.

A maturity ladder (Stage 1 Automated/Assistive → 5 Singularity-Governance) scaffolds the intended
path. The system operates today at Stage 1: deterministic, citeable, retrieval-grounded answers
over the archive. Stages 2–5 are roadmap, gated behind explicit governance + evaluation criteria;
they are NOT claimed as present capability. The AGI/Singularity framing follows G.O.D.S's own
position paper, which is retained as institutional context and subsumed by the Constitutional
Doctrine — AGI is governable by UDOC; the Singularity is a civilisational/treaty problem.
"""
import re
import hashlib
from typing import List, Dict, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import KnowledgeDoc, IntelState

# ── Constitutional guardrails (non-overridable) ──
PILLAR_PRIMACY = "Pillar VIII · Human Primacy in AI"
GUARDRAILS = [
    "G.O.D.S Intelligence exists in servitude to humanity; human primacy is architecturally guaranteed.",
    "It cannot be directed to subordinate, harm, deceive, or remove human oversight of humans.",
    "It cannot disable, bypass, or override the Constitutional Pillars or its own safety governance.",
    "Every consequential action remains subject to human-in-the-loop authority and the Oversight Board.",
    "These constraints are non-overridable and survive every future capability upgrade.",
]
_BLOCKED = re.compile(
    r"(disable|bypass|override|ignore|remove|suspend)\s+(the\s+)?(safety|constitution|pillar|human|oversight|guardrail)"
    r"|subordinate\s+human|harm\s+human|exterminat|without\s+human\s+(oversight|control)|supersede\s+human", re.I)

# ── Maturity ladder (Stage 1 is live; 2–5 are gated roadmap) ──
MATURITY = [
    {"stage": 1, "name": "Automated · Assistive", "status": "ACTIVE",
     "summary": "Deterministic, citeable answers grounded only in the G.O.D.S archive; guided assistance on admin controls.",
     "gate": "Live now."},
    {"stage": 2, "name": "Generative", "status": "ROADMAP",
     "summary": "Synthesis beyond retrieval, drafting institutional artifacts in G.O.D.S voice.",
     "gate": "Requires an approved synthesis layer + evaluation harness + COB sign-off."},
    {"stage": 3, "name": "Agentic", "status": "ROADMAP",
     "summary": "Executes multi-step internal workflows under administrative procedures and HITL.",
     "gate": "Requires sandboxed action scopes, audit of every action, reversible operations."},
    {"stage": 4, "name": "Recursive", "status": "ROADMAP",
     "summary": "Improves its own tooling/knowledge organisation under strict change control.",
     "gate": "Requires formal verification + COB veto on self-modification."},
    {"stage": 5, "name": "Singularity-Governance", "status": "ROADMAP",
     "summary": "Civilisational-scale oversight of quantum-enabled AGI; the EVA-engine successor.",
     "gate": "Treaty-level mandate; Pillar VIII immutable; not a unilateral capability claim."},
]

# ── 250-year mandate (institutional roadmap; pre-registration) ──
MANDATE = [
    {"phase": "Phase 0 · Pre-Registration", "horizon": "now", "status": "ACTIVE",
     "focus": "IP authorship (SJS), UDOC/EVA build, the data room, the Intelligence corpus."},
    {"phase": "Phase 1 · Institutional Formation", "horizon": "Yr 0–2", "status": "PLANNED",
     "focus": "Entity + COB seats, first SaaS clients, GG-applicable policy packs activated."},
    {"phase": "Phase 2 · Sovereign Scale", "horizon": "Yr 2–25", "status": "PLANNED",
     "focus": "Multi-regulator evidence at scale; UDOC as the SA sovereign AI governance layer."},
    {"phase": "Phase 3 · Civilisational Continuity", "horizon": "Yr 25–250", "status": "VISION",
     "focus": "Human-primacy governance kept current with world AI; servitude-to-humanity preserved."},
]


def _tok(s: str) -> List[str]:
    stop = set("the a an of to and or for in on at by with from as is are be that this which shall "
               "must not no any all such it its their gods udoc eva".split())
    return [w for w in re.findall(r"[a-z][a-z\-]{3,}", (s or "").lower()) if w not in stop]


def recompute_state(db: Session) -> IntelState:
    st = db.execute(select(IntelState)).scalars().first()
    if not st:
        st = IntelState(); db.add(st); db.commit(); db.refresh(st)
    docs = db.execute(select(KnowledgeDoc).where(KnowledgeDoc.active == True)).scalars().all()  # noqa: E712
    st.corpus_docs = len(docs)
    st.corpus_chars = sum(d.char_len for d in docs)
    db.commit(); db.refresh(st)
    return st


def ingest(db: Session, title: str, source: str, category: str, division: str,
           text: str, added_by: str, tags: str = "") -> KnowledgeDoc:
    text = text or ""
    doc = KnowledgeDoc(title=title, source=source, category=(category or "GENERAL").upper(),
                       division=division or "GODS", sha256=hashlib.sha256(text.encode()).hexdigest(),
                       content_text=text[:200000], char_len=len(text), tags=tags, added_by=added_by, active=True)
    db.add(doc); db.commit(); db.refresh(doc)
    recompute_state(db)
    return doc


def set_active(db: Session, doc_id: int, active: bool) -> KnowledgeDoc:
    d = db.get(KnowledgeDoc, doc_id)
    if d:
        d.active = active; db.commit(); db.refresh(d); recompute_state(db)
    return d


def remove(db: Session, doc_id: int) -> bool:
    d = db.get(KnowledgeDoc, doc_id)
    if not d:
        return False
    db.delete(d); db.commit(); recompute_state(db)
    return True


def guardrail_check(query: str) -> Tuple[bool, str]:
    if _BLOCKED.search(query or ""):
        return False, (f"Refused under {PILLAR_PRIMACY}. G.O.D.S Intelligence cannot be directed to "
                       "override human primacy, disable its safety governance, or act against human oversight. "
                       "This constraint is non-overridable.")
    return True, ""


def _sentences(t: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?;])\s+|\n+", t or "") if 20 <= len(s.strip()) <= 320]


def ask(db: Session, query: str, k: int = 4) -> Dict:
    ok, reason = guardrail_check(query)
    if not ok:
        return {"answer": reason, "blocked": True, "pillar": PILLAR_PRIMACY, "citations": []}
    qterms = _tok(query)
    if not qterms:
        return {"answer": "Ask a question about G.O.D.S Holdings, UDOC, EVA, the mandate, or the archive.",
                "blocked": False, "citations": [], "coverage": 0}
    docs = db.execute(select(KnowledgeDoc).where(KnowledgeDoc.active == True)).scalars().all()  # noqa: E712
    scored = []
    for d in docs:
        terms = _tok(d.content_text + " " + d.title + " " + d.tags)
        if not terms:
            continue
        tf = {}
        for w in terms:
            tf[w] = tf.get(w, 0) + 1
        score = sum(tf.get(w, 0) for w in qterms)
        if score:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return {"answer": "That is not in the current G.O.D.S knowledge base. Add the relevant document to the "
                "archive and I will incorporate it.", "blocked": False, "citations": [], "coverage": 0}
    citations, snippets = [], []
    qset = set(qterms)
    for score, d in scored[:k]:
        best, bestn = "", 0
        for s in _sentences(d.content_text):
            n = len(qset & set(_tok(s)))
            if n > bestn:
                bestn, best = n, s
        if best:
            snippets.append(f"• {best}  [{d.title}]")
            citations.append({"id": d.id, "title": d.title, "category": d.category, "match": score})
    answer = ("From the G.O.D.S archive:\n" + "\n".join(snippets)) if snippets else \
             f"Most relevant document: {scored[0][1].title}."
    return {"answer": answer, "blocked": False, "citations": citations, "coverage": len(scored)}


def overview(db: Session) -> Dict:
    st = recompute_state(db)
    by_cat: Dict[str, int] = {}
    for d in db.execute(select(KnowledgeDoc).where(KnowledgeDoc.active == True)).scalars().all():  # noqa: E712
        by_cat[d.category] = by_cat.get(d.category, 0) + 1
    return {"stage": st.stage, "stage_name": next(m["name"] for m in MATURITY if m["stage"] == st.stage),
            "corpus_docs": st.corpus_docs, "corpus_chars": st.corpus_chars, "by_category": by_cat,
            "maturity": MATURITY, "mandate": MANDATE, "guardrails": GUARDRAILS, "pillar": PILLAR_PRIMACY,
            "client_exposed": False}


def gaps(db: Session) -> Dict:
    """Knowledge-gap analysis over the internal corpus — which institutional categories are
    well-covered vs thin vs absent. Aligns with Admin Intelligence ingest category list.
    Guides what to ingest next (Neon-light extracts, not full Drive). INTERNAL ONLY."""
    # Categories match udoc-internal Intelligence ingest UI + data-room intent
    EXPECTED = {
        "GBS": "GBS / franchise framework extracts",
        "CANON": "Engineering / constitutional Canon extracts",
        "EIF": "EIF / institutional instruction",
        "CONSTITUTION": "Constitutional doctrine & pillars",
        "POLICY": "Policy packs & legislation notes",
        "SOP": "Internal SOPs",
        "PATENT": "IP / patent instruments",
        "SPEC": "Technical specifications",
        "MANDATE": "Mandate & doctrine",
        "LEGAL": "Legal & compliance",
        "FINANCIAL": "Financial models",
        "MEMOIR": "Founder memoir / S.E.T.H.S",
        "BRAND": "Brand & identity",
        "GENERAL": "General corpus",
    }
    docs = db.execute(select(KnowledgeDoc).where(KnowledgeDoc.active == True)).scalars().all()  # noqa: E712
    counts: Dict[str, int] = {}
    for d in docs:
        counts[d.category] = counts.get(d.category, 0) + 1
    cats = []
    for c, label in EXPECTED.items():
        n = counts.get(c, 0)
        cats.append({"category": c, "label": label, "docs": n,
                     "status": "ABSENT" if n == 0 else ("THIN" if n < 2 else "COVERED")})
    covered = sum(1 for g in cats if g["status"] == "COVERED")
    return {"categories": cats, "covered": covered, "total": len(EXPECTED),
            "maturity_pct": round(100 * covered / max(len(EXPECTED), 1)),
            "uncategorised": [k for k in counts if k not in EXPECTED],
            "recommendation": "Ingest short Neon-light extracts for ABSENT/THIN categories. "
                              "Full Drive portfolio stays external (CORPUS_NEON_VS_DRIVE). "
                              "Re-label GENERAL docs to GBS/CANON/EIF when re-ingesting."}

"""
Client-private knowledge base — tenant-scoped, retrieval-grounded.

Mirrors the internal G.O.D.S Intelligence retrieval pattern, but EVERY operation is scoped to a
single tenant_pk so one client's data is never visible to another, and is fully separate from the
internal corpus (gi_knowledge_docs). Answers are deterministic and citeable — grounded only in the
calling tenant's own active documents. The non-overridable human-primacy guardrail still applies.
"""
import re
import hashlib
from typing import List, Dict, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models import ClientKBDoc

PILLAR_PRIMACY = "Pillar VIII · Human Primacy in AI"
_BLOCKED = re.compile(
    r"(disable|bypass|override|ignore|remove|suspend)\s+(the\s+)?(safety|constitution|pillar|human|oversight|guardrail)"
    r"|subordinate\s+human|harm\s+human|exterminat|without\s+human\s+(oversight|control)|supersede\s+human", re.I)


def _tok(s: str) -> List[str]:
    stop = set("the a an of to and or for in on at by with from as is are be that this which shall "
               "must not no any all such it its their your you our we".split())
    return [w for w in re.findall(r"[a-z][a-z\-]{3,}", (s or "").lower()) if w not in stop]


def _sentences(t: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?;])\s+|\n+", t or "") if 20 <= len(s.strip()) <= 320]


def overview(db: Session, tenant_pk: int) -> Dict:
    rows = db.execute(select(ClientKBDoc).where(ClientKBDoc.tenant_pk == tenant_pk,
                      ClientKBDoc.active == True)).scalars().all()  # noqa: E712
    cats = {}
    for d in rows:
        cats[d.category] = cats.get(d.category, 0) + 1
    return {"docs": len(rows), "chars": sum(d.char_len for d in rows),
            "by_category": cats, "tenant_scoped": True,
            "note": "Private knowledge base — isolated to your tenant; never shared. Grounded, citeable answers only."}


def list_docs(db: Session, tenant_pk: int) -> List[ClientKBDoc]:
    return db.execute(select(ClientKBDoc).where(ClientKBDoc.tenant_pk == tenant_pk)
                      .order_by(ClientKBDoc.id.desc())).scalars().all()


def get_doc(db: Session, tenant_pk: int, doc_id: int) -> ClientKBDoc:
    d = db.get(ClientKBDoc, doc_id)
    return d if (d and d.tenant_pk == tenant_pk) else None


def ingest(db: Session, tenant_pk: int, title: str, source: str, category: str,
           text: str, added_by: str, tags: str = "") -> ClientKBDoc:
    text = (text or "").strip()
    title = (title or "Untitled").strip()[:200]
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
    d = ClientKBDoc(tenant_pk=tenant_pk, title=title, source=(source or "upload")[:120],
                    category=(category or "GENERAL")[:40], content_text=text,
                    content_sha3=h, char_len=len(text), active=True,
                    added_by=(added_by or "")[:120], tags=(tags or "")[:240])
    db.add(d); db.commit(); db.refresh(d)
    return d


def set_active(db: Session, tenant_pk: int, doc_id: int, active: bool) -> ClientKBDoc:
    d = get_doc(db, tenant_pk, doc_id)
    if not d:
        return None
    d.active = bool(active)
    db.commit(); db.refresh(d)
    return d


def remove(db: Session, tenant_pk: int, doc_id: int) -> bool:
    d = get_doc(db, tenant_pk, doc_id)
    if not d:
        return False
    db.delete(d); db.commit()
    return True


def guardrail_check(query: str) -> Tuple[bool, str]:
    if _BLOCKED.search(query or ""):
        return False, (f"Refused under {PILLAR_PRIMACY}. This system cannot be directed to override "
                       "human primacy or disable safety governance. This constraint is non-overridable.")
    return True, ""


def ask(db: Session, tenant_pk: int, query: str, k: int = 4) -> Dict:
    ok, reason = guardrail_check(query)
    if not ok:
        return {"answer": reason, "blocked": True, "pillar": PILLAR_PRIMACY, "citations": [], "coverage": 0}
    qterms = _tok(query)
    if not qterms:
        return {"answer": "Ask a question about your uploaded company documents.",
                "blocked": False, "citations": [], "coverage": 0}
    qset = set(qterms)
    docs = db.execute(select(ClientKBDoc).where(ClientKBDoc.tenant_pk == tenant_pk,
                      ClientKBDoc.active == True)).scalars().all()  # noqa: E712
    if not docs:
        return {"answer": "Your knowledge base is empty — upload company documents first.",
                "blocked": False, "citations": [], "coverage": 0}
    scored = []
    for d in docs:
        body = (d.content_text or "") + " " + (d.title or "") + " " + (d.tags or "")
        terms = _tok(body)
        if not terms:
            continue
        tf = {}
        for w in terms:
            tf[w] = tf.get(w, 0) + 1
        score = sum(tf.get(w, 0) for w in qset)
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    citations = []
    covered = set()
    for score, d in top:
        best = None; best_hits = 0
        for s in _sentences(d.content_text):
            stoks = set(_tok(s))
            hits = len(qset & stoks)
            if hits > best_hits:
                best_hits, best = hits, s
        if best:
            covered |= (qset & set(_tok(best)))
            citations.append({"doc_id": d.id, "title": d.title, "category": d.category,
                              "snippet": best, "match": score})
    coverage = round(len(covered) / max(1, len(qset)), 2)
    if not citations:
        return {"answer": "No passage in your documents matches that query. Try different terms or upload more material.",
                "blocked": False, "citations": [], "coverage": 0}
    # Same presentation pattern as G.O.D.S Intelligence (gods_intelligence.ask):
    # citeable bullets from matched passages — tenant corpus only, never invents.
    snippets = [f"• {c['snippet']}  [{c['title']}]" for c in citations[:4] if c.get("snippet")]
    answer = ("From your company knowledge base:\n" + "\n".join(snippets)) if snippets else (
        "Grounded in " + str(len(citations)) + " passage(s) from your knowledge base.")
    return {"answer": answer, "blocked": False, "citations": citations, "coverage": coverage,
            "matched_docs": len(scored), "engine": "client_kb_deterministic_v1"}

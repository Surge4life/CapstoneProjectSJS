"""
G.O.D.S Intelligence API — INTERNAL ONLY (admin / operator / gov; auditor read-only).
Never exposed to SaaS clients. Manages the archive (add/remove data), reports the maturity
ladder + 250-year mandate, and answers questions grounded strictly in the G.O.D.S corpus,
hard-wired to Pillar VIII (Human Primacy).
"""
import hashlib
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import KnowledgeDoc
from app.core.dependencies import current_user
from app.services import gods_intelligence as gi
from app.services import policy_engine as pe  # reuse PDF/DOCX/TXT extraction
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/intel", tags=["G.O.D.S Intelligence · INTERNAL"])

_READ = {"admin", "operator", "gov", "auditor"}
_WRITE = {"admin", "operator", "gov"}


def _gate(user: dict, write: bool = False):
    role = user.get("role")
    allowed = _WRITE if write else _READ
    if role not in allowed:
        raise HTTPException(403, "G.O.D.S Intelligence is internal-only — not available to this role")


def _doc_out(d: KnowledgeDoc) -> dict:
    return {"id": d.id, "title": d.title, "source": d.source, "category": d.category,
            "division": d.division, "char_len": d.char_len, "tags": d.tags,
            "active": d.active, "added_by": d.added_by, "created_at": d.created_at.isoformat()}


@router.get("/state")
def state(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user)
    return gi.overview(db)


@router.get("/docs")
def docs(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user)
    rows = db.execute(select(KnowledgeDoc).order_by(KnowledgeDoc.id.desc())).scalars().all()
    return [_doc_out(d) for d in rows]


class TextIngest(BaseModel):
    title: str
    text: str
    category: str = "GENERAL"
    division: str = "GODS"
    tags: str = ""
    source: str = "inline"


@router.post("/ingest-text")
def ingest_text(body: TextIngest, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user, write=True)
    d = gi.ingest(db, body.title, body.source, body.category, body.division, body.text,
                  user.get("sub", ""), body.tags)
    append_audit(db, "INTEL_INGEST", {"doc": d.id, "title": d.title, "chars": d.char_len},
                 classification="INTERNAL", actor_class=user.get("role", "SYSTEM"))
    return {"doc": _doc_out(d), "state": gi.overview(db)}


@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...), title: str = Form(""),
                      category: str = Form("GENERAL"), division: str = Form("GODS"),
                      tags: str = Form(""), db: Session = Depends(get_db),
                      user: dict = Depends(current_user)):
    _gate(user, write=True)
    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "file exceeds 25MB limit")
    text = pe.extract_text(file.filename or "doc.txt", data)
    d = gi.ingest(db, title or (file.filename or "Untitled"), file.filename or "", category,
                  division, text, user.get("sub", ""), tags)
    append_audit(db, "INTEL_INGEST", {"doc": d.id, "title": d.title, "chars": d.char_len,
                 "sha256": d.sha256[:16]}, classification="INTERNAL", actor_class=user.get("role", "SYSTEM"))
    return {"doc": _doc_out(d), "state": gi.overview(db),
            "note": "Document added to the G.O.D.S archive — knowledge updated immediately."}


@router.patch("/docs/{doc_id}")
def toggle_doc(doc_id: int, active: bool, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user, write=True)
    d = gi.set_active(db, doc_id, active)
    if not d:
        raise HTTPException(404, "doc not found")
    return _doc_out(d)


@router.delete("/docs/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user, write=True)
    if not gi.remove(db, doc_id):
        raise HTTPException(404, "doc not found")
    append_audit(db, "INTEL_REMOVE", {"doc": doc_id}, classification="INTERNAL",
                 actor_class=user.get("role", "SYSTEM"))
    return {"removed": doc_id, "state": gi.overview(db)}


class AskReq(BaseModel):
    query: str


@router.post("/ask")
def ask(body: AskReq, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    _gate(user)
    res = gi.ask(db, body.query)
    append_audit(db, "INTEL_QUERY", {"q": body.query[:80], "blocked": res.get("blocked", False),
                 "coverage": res.get("coverage", 0)}, classification="INTERNAL",
                 actor_class=user.get("role", "SYSTEM"))
    return res


@router.get("/gaps")
def gaps(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    """Internal knowledge-gap report — coverage by institutional category."""
    _gate(user)
    return gi.gaps(db)

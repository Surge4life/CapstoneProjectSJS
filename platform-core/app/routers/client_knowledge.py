"""
Client-private knowledge base API — TENANT-SCOPED.

Available to a SaaS client (JWT role 'client' or an X-API-Key) strictly for THEIR OWN tenant.
Internal staff use /intel instead; this endpoint is not a window into client data for staff.
Every call is scoped by scope_pk(principal) -> the caller's tenant_pk; cross-tenant access is
impossible by construction.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import principal, scope_pk
from app.services import client_knowledge as ckb
from app.services import policy_engine as pe  # PDF/DOCX/TXT extraction (reused)
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/client/knowledge", tags=["Client Knowledge · TENANT-PRIVATE"])


def _tenant(user: dict) -> int:
    """Resolve and enforce the caller's own tenant. Staff (None) and tenant-less (-1) are refused —
    this surface is exclusively a tenant's private store."""
    pk = scope_pk(user)
    if pk is None:
        raise HTTPException(403, "Company Knowledge is a tenant-private client surface. Internal staff use /intel.")
    if pk < 0:
        raise HTTPException(403, "No tenant context for this account.")
    return pk


def _doc_out(d) -> dict:
    return {"id": d.id, "title": d.title, "source": d.source, "category": d.category,
            "char_len": d.char_len, "tags": d.tags, "active": d.active,
            "added_by": d.added_by, "created_at": d.created_at.isoformat()}


@router.get("/state")
def state(db: Session = Depends(get_db), user: dict = Depends(principal)):
    return ckb.overview(db, _tenant(user))


@router.get("/docs")
def docs(db: Session = Depends(get_db), user: dict = Depends(principal)):
    return [_doc_out(d) for d in ckb.list_docs(db, _tenant(user))]


@router.get("/docs/{doc_id}")
def doc(doc_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    d = ckb.get_doc(db, _tenant(user), doc_id)
    if not d:
        raise HTTPException(404, "document not found in your knowledge base")
    out = _doc_out(d); out["content_text"] = d.content_text
    return out


class TextIngest(BaseModel):
    title: str
    text: str
    category: str = "GENERAL"
    tags: str = ""
    source: str = "inline"


@router.post("/ingest-text")
def ingest_text(body: TextIngest, db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = _tenant(user)
    d = ckb.ingest(db, pk, body.title, body.source, body.category, body.text,
                   user.get("sub", ""), body.tags)
    append_audit(db, "CLIENT_KB_INGEST", {"doc": d.id, "title": d.title, "chars": d.char_len,
                 "tenant_pk": pk}, classification="CLIENT", actor_class="client")
    return {"doc": _doc_out(d), "state": ckb.overview(db, pk)}


@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...), title: str = Form(""),
                      category: str = Form("GENERAL"), tags: str = Form(""),
                      db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = _tenant(user)
    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "file exceeds 25MB limit")
    text = pe.extract_text(file.filename or "doc.txt", data)
    d = ckb.ingest(db, pk, title or (file.filename or "Untitled"), file.filename or "",
                   category, text, user.get("sub", ""), tags)
    append_audit(db, "CLIENT_KB_INGEST", {"doc": d.id, "title": d.title, "chars": d.char_len,
                 "tenant_pk": pk}, classification="CLIENT", actor_class="client")
    return {"doc": _doc_out(d), "state": ckb.overview(db, pk),
            "note": "Document added to your private knowledge base — available to your team immediately."}


@router.patch("/docs/{doc_id}")
def toggle(doc_id: int, active: bool, db: Session = Depends(get_db), user: dict = Depends(principal)):
    d = ckb.set_active(db, _tenant(user), doc_id, active)
    if not d:
        raise HTTPException(404, "document not found in your knowledge base")
    return _doc_out(d)


@router.delete("/docs/{doc_id}")
def delete(doc_id: int, db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = _tenant(user)
    if not ckb.remove(db, pk, doc_id):
        raise HTTPException(404, "document not found in your knowledge base")
    append_audit(db, "CLIENT_KB_REMOVE", {"doc": doc_id, "tenant_pk": pk},
                 classification="CLIENT", actor_class="client")
    return {"removed": doc_id, "state": ckb.overview(db, pk)}


class AskReq(BaseModel):
    query: str


@router.post("/ask")
def ask(body: AskReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    pk = _tenant(user)
    res = ckb.ask(db, pk, body.query)
    append_audit(db, "CLIENT_KB_QUERY", {"q": body.query[:80], "coverage": res.get("coverage", 0),
                 "tenant_pk": pk}, classification="CLIENT", actor_class="client")
    return res

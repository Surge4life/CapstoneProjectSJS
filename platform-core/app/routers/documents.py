"""
Documents API — upload (multipart) + download, recorded through UDOC.
Used by SETHS (CVs/qualifications), TS (project docs), MADIBA (reports), UDOC (compliance).
"""
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import current_user
from app.services import document_store as ds

router = APIRouter(prefix="/documents", tags=["Documents · UDOC records"])


@router.post("/upload")
async def upload(division: str = Form(...), owner_ref: str = Form(...),
                 category: str = Form("GENERAL"), file: UploadFile = File(...),
                 db: Session = Depends(get_db), _: dict = Depends(current_user)):
    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "file exceeds 25MB limit")
    doc = ds.store(db, division, owner_ref, category, file.filename or "upload.bin",
                   file.content_type or "application/octet-stream", data)
    return {"doc_ref": doc.doc_ref, "filename": doc.filename, "size_bytes": doc.size_bytes,
            "sha256": doc.sha256, "category": doc.category}


@router.get("/owner/{owner_ref}")
def list_owner(owner_ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    docs = ds.list_for_owner(db, owner_ref)
    return [{"doc_ref": d.doc_ref, "filename": d.filename, "category": d.category,
             "size_bytes": d.size_bytes, "created_at": d.created_at.isoformat()} for d in docs]


@router.get("/{doc_ref}/download")
def download(doc_ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    res = ds.fetch(db, doc_ref)
    if not res:
        raise HTTPException(404, "document not found")
    doc, data = res
    return Response(content=data, media_type=doc.content_type,
                    headers={"Content-Disposition": f'attachment; filename="{doc.filename}"'})


@router.get("/{doc_ref}/meta")
def meta(doc_ref: str, db: Session = Depends(get_db), _: dict = Depends(current_user)):
    res = ds.fetch(db, doc_ref)
    if not res:
        raise HTTPException(404, "document not found")
    doc, _data = res
    return {"doc_ref": doc.doc_ref, "filename": doc.filename, "sha256": doc.sha256,
            "size_bytes": doc.size_bytes, "verified": True}

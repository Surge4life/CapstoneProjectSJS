"""
Document store — real file persistence with integrity hashing, recorded through UDOC.
Dev/emulation: files under ./storage/. Production: swap _write/_read for S3/object storage
(same interface). Every upload is hash-sealed and logged to the audit chain + analytics.
"""
import hashlib
import os
import uuid
from sqlalchemy.orm import Session
from app.db.models import Document
from app.services.audit_writer import append_audit
from app.services import analytics_engine as ae

STORAGE_ROOT = os.environ.get("GODS_STORAGE", os.path.join(os.path.dirname(__file__), "..", "..", "storage"))


def _ensure_root():
    os.makedirs(STORAGE_ROOT, exist_ok=True)


def store(db: Session, division: str, owner_ref: str, category: str,
          filename: str, content_type: str, data: bytes) -> Document:
    _ensure_root()
    doc_ref = f"DOC-{uuid.uuid4().hex[:10]}"
    sha = hashlib.sha256(data).hexdigest()
    safe = doc_ref + "_" + os.path.basename(filename).replace("/", "_")
    path = os.path.join(STORAGE_ROOT, safe)
    with open(path, "wb") as f:
        f.write(data)
    doc = Document(doc_ref=doc_ref, division=division.upper(), owner_ref=owner_ref,
                   category=category, filename=filename, content_type=content_type,
                   size_bytes=len(data), sha256=sha, storage_path=path)
    db.add(doc); db.commit(); db.refresh(doc)
    # UDOC: record + audit the upload (immutable trail)
    append_audit(db, "DOCUMENT_UPLOAD", {"doc_ref": doc_ref, "division": division,
                 "owner": owner_ref, "sha256": sha[:16]}, classification="RECORDS")
    ae.record(db, division.upper(), "DOC_UPLOAD", entity_ref=owner_ref,
              metric_name="documents", metric_value=1)
    return doc


def fetch(db: Session, doc_ref: str) -> tuple[Document, bytes] | None:
    doc = db.query(Document).filter(Document.doc_ref == doc_ref).first()
    if not doc or not os.path.exists(doc.storage_path):
        return None
    with open(doc.storage_path, "rb") as f:
        data = f.read()
    # integrity check on fetch
    if hashlib.sha256(data).hexdigest() != doc.sha256:
        raise ValueError("document integrity check failed")
    return doc, data


def list_for_owner(db: Session, owner_ref: str) -> list[Document]:
    return db.query(Document).filter(Document.owner_ref == owner_ref).all()

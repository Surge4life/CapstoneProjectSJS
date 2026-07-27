# Chapter 11 — Document Engine

## Purpose

The Document Engine manages the complete lifecycle of user-submitted documents: upload, storage, integrity sealing, retrieval, and integrity verification. It provides the SHA-256 + UDOC audit chain sealing that makes SETHS documents cryptographically verifiable.

---

## Location

- **Router:** `platform-core/app/routers/documents.py`
- **Service:** `platform-core/app/services/document_store.py`
- **Model:** `platform-core/app/db/models/documents.py` — `Document`

---

## The Document Integrity Promise

When a learner uploads a CV or qualification certificate:

1. The file is uploaded to the G.O.D.S system
2. The system computes a SHA-256 hash of the exact file bytes
3. This hash is stored in the `Document` table
4. An audit record is created on the UDOC audit chain, sealing the hash permanently
5. The hash on the audit chain is HMAC-signed with the HSM key

When anyone downloads that document later:

1. The file is retrieved from object storage
2. The system recomputes the SHA-256 hash of the retrieved bytes
3. The recomputed hash is compared to the stored hash
4. If they match: `X-Integrity-Verified: true` header, document served
5. If they don't match: `INTEGRITY_FAILURE` — the document was tampered with

The UDOC audit chain record is permanent. Even if someone modified the document in object storage AND modified the database record, the audit chain record would still contain the original hash — and the HMAC seal would prevent silent modification of that record.

---

## Document Service

```python
class DocumentStore:
    async def upload(
        self,
        file: UploadFile,
        document_type: str,
        uploader_id: UUID,
        tenant_id: UUID,
        metadata: DocumentMetadata
    ) -> Document:
        # Read file into memory
        content = await file.read()

        # Compute SHA-256 hash
        sha256 = hashlib.sha256(content).hexdigest()

        # Generate storage key
        storage_key = f"{tenant_id}/{uploader_id}/{uuid4()}/{file.filename}"

        # Upload to object storage
        await self.storage.put(
            key=storage_key,
            content=content,
            content_type=file.content_type
        )

        # Create database record
        doc = Document(
            learner_id=uploader_id,
            tenant_id=tenant_id,
            document_type=document_type,
            file_name=file.filename,
            file_size_bytes=len(content),
            mime_type=file.content_type,
            storage_key=storage_key,
            storage_bucket=self.storage.bucket,
            sha256_hash=sha256,
            **metadata.dict()
        )
        db.add(doc)

        # Seal to audit chain
        audit_ref = await self.audit_writer.write(
            event_type="DATA_CHANGE.DOCUMENT_UPLOADED",
            resource_type="Document",
            resource_id=doc.id,
            actor_id=uploader_id,
            event_summary={
                "document_type": document_type,
                "file_name": file.filename,
                "sha256_hash": sha256,
                "sealed": True
            }
        )
        doc.udoc_audit_ref_id = audit_ref.id

        await db.commit()
        return doc

    async def download(self, document_id: UUID, requestor_id: UUID) -> tuple[bytes, Document]:
        doc = await db.get(Document, document_id)

        # Authorisation check (service layer)
        await self._verify_download_access(doc, requestor_id)

        # Retrieve from object storage
        content = await self.storage.get(doc.storage_key)

        # Integrity verification
        recomputed = hashlib.sha256(content).hexdigest()
        if recomputed != doc.sha256_hash:
            await self.audit_writer.write(
                event_type="SYSTEM.DOCUMENT_INTEGRITY_FAILURE",
                resource_id=doc.id,
                event_summary={
                    "stored_hash": doc.sha256_hash,
                    "computed_hash": recomputed,
                    "requestor_id": str(requestor_id)
                }
            )
            raise IntegrityFailureError(doc.id, doc.sha256_hash, recomputed)

        # Log download in audit chain
        await self.audit_writer.write(
            event_type="DATA_CHANGE.DOCUMENT_DOWNLOADED",
            resource_id=doc.id,
            actor_id=requestor_id,
            event_summary={"integrity": "VERIFIED"}
        )

        return content, doc
```

---

## Supported Document Types

| `document_type` | Max Size | Accepted MIME Types |
|----------------|---------|-------------------|
| `cv` | 10 MB | `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| `qualification` | 20 MB | `application/pdf`, `image/jpeg`, `image/png` |
| `id_document` | 5 MB | `application/pdf`, `image/jpeg`, `image/png` |
| `reference` | 10 MB | `application/pdf` |
| `portfolio` | 50 MB | `application/pdf`, `application/zip` |
| `other` | 10 MB | `application/pdf`, text types |

Virus scanning: all uploaded files are scanned with ClamAV before storage. Infected files are rejected and the upload attempt is logged in the audit chain.

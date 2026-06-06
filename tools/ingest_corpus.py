#!/usr/bin/env python3
"""
G.O.D.S Intelligence corpus loader — ingest a folder or .zip (e.g. your Google Drive export)
into the internal Intelligence archive. "Training" = curating this corpus.

Usage:
  python3 tools/ingest_corpus.py <path-to-folder-or-zip> [--category AUTO]
Run from the repo root with platform-core deps installed (the station venv). Ingests directly
into the platform DB via the same engine the /intel API uses. INTERNAL ONLY.
"""
import os, sys, zipfile, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "platform-core"))
from app.db.session import SessionLocal, init_db          # noqa: E402
from app.services import gods_intelligence as gi          # noqa: E402
from app.services.policy_engine import extract_text        # noqa: E402

SUPPORTED = (".pdf", ".docx", ".txt", ".md", ".markdown", ".html", ".htm")
SKIP_DIRS = {"node_modules", ".git", "dist", "__pycache__", ".venv", ".udoc-venv"}


def guess_category(name: str) -> str:
    n = name.lower()
    for kw, cat in [("patent", "PATENT"), ("whitepaper", "SPEC"), ("white_paper", "SPEC"),
                    ("brand", "BRAND"), ("mandate", "MANDATE"), ("constitution", "LEGAL"),
                    ("financial", "FINANCIAL"), ("budget", "FINANCIAL"), ("legal", "LEGAL"),
                    ("memoir", "MEMOIR"), ("spec", "SPEC")]:
        if kw in n:
            return cat
    return "GENERAL"


def ingest_dir(db, base: str) -> int:
    n = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.lower().endswith(SUPPORTED):
                continue
            path = os.path.join(root, fn)
            try:
                with open(path, "rb") as fh:
                    text = extract_text(fn, fh.read())
                if not text or len(text.strip()) < 20:
                    continue
                rel = os.path.relpath(path, base)
                gi.ingest(db, title=fn, source=rel, category=guess_category(fn),
                          division="GODS", text=text, added_by="corpus-loader")
                n += 1
                print(f"  + {rel[:70]} ({len(text)} chars · {guess_category(fn)})")
            except Exception as e:
                print(f"  ! skip {fn}: {e}")
    return n


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    init_db()
    db = SessionLocal()
    if src.lower().endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmp:
            print(f"▶ extracting {src} ...")
            with zipfile.ZipFile(src) as z:
                z.extractall(tmp)
            n = ingest_dir(db, tmp)
    else:
        n = ingest_dir(db, src)
    st = gi.overview(db)
    db.close()
    print(f"\n✓ ingested {n} document(s). Corpus now: {st['corpus_docs']} docs · {st['corpus_chars']} chars · stage {st['stage']} ({st['stage_name']}).")


if __name__ == "__main__":
    main()

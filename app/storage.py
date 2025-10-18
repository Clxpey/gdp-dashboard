from __future__ import annotations
import hashlib
import mimetypes
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import json
import shutil

from tinydb import TinyDB, Query
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document as DocxDocument

from .config import DOCS_DIR, INDEX_DIR, MAX_TEXT_PREVIEW_CHARS
from .embeddings import EmbeddingIndex
from .ai import summarize_text


@dataclass
class DocumentMeta:
    id: str
    filename: str
    path: str
    size: int
    mime_type: str
    tags: List[str]
    client: Optional[str]
    created_at: str
    modified_at: str
    archived: bool
    checksum: str
    summary: Optional[str] = None


class DocumentStore:
    def __init__(self, db_path: Path | None = None) -> None:
        self.docs_dir = DOCS_DIR
        self.db_path = db_path or (INDEX_DIR / "documents.json")
        self.db = TinyDB(self.db_path)
        self.index = EmbeddingIndex()

    # -------------- helpers --------------
    @staticmethod
    def _now_iso() -> str:
        return datetime.utcnow().isoformat()

    @staticmethod
    def _checksum(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _detect_mime(path: Path) -> str:
        mt, _ = mimetypes.guess_type(str(path))
        return mt or "application/octet-stream"

    @staticmethod
    def _read_text(path: Path, mime: str) -> str:
        try:
            if mime == "application/pdf":
                return extract_pdf_text(str(path))
            if mime in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"):
                d = DocxDocument(str(path))
                return "\n".join([p.text for p in d.paragraphs])
            if mime.startswith("text/"):
                return path.read_text(errors="ignore")
        except Exception:
            pass
        # fallback: nothing
        return ""

    # -------------- CRUD --------------
    def add_file(self, src_path: Path, tags: Optional[List[str]] = None, client: Optional[str] = None) -> DocumentMeta:
        tags = tags or []
        dest_path = self.docs_dir / src_path.name
        if src_path.resolve() != dest_path.resolve():
            shutil.copy2(src_path, dest_path)
        else:
            shutil.copystat(src_path, dest_path)

        mime = self._detect_mime(dest_path)
        size = dest_path.stat().st_size
        checksum = self._checksum(dest_path)
        doc_id = checksum[:16]
        created = self._now_iso()
        modified = created
        text = self._read_text(dest_path, mime)
        summary = summarize_text(text) if text else None

        meta = DocumentMeta(
            id=doc_id,
            filename=dest_path.name,
            path=str(dest_path),
            size=size,
            mime_type=mime,
            tags=tags,
            client=client,
            created_at=created,
            modified_at=modified,
            archived=False,
            checksum=checksum,
            summary=summary,
        )
        self.db.insert(asdict(meta))
        # index text
        if text:
            self.index.upsert_document(doc_id, text)
        return meta

    def import_bytes(self, data: bytes, filename: str, tags: Optional[List[str]] = None, client: Optional[str] = None) -> DocumentMeta:
        dest_path = self.docs_dir / filename
        dest_path.write_bytes(data)
        return self.add_file(dest_path, tags=tags, client=client)

    def list_documents(self, include_archived: bool = False) -> List[DocumentMeta]:
        docs = [DocumentMeta(**d) for d in self.db.all()]
        if not include_archived:
            docs = [d for d in docs if not d.archived]
        docs.sort(key=lambda d: d.modified_at, reverse=True)
        return docs

    def get_by_id(self, doc_id: str) -> Optional[DocumentMeta]:
        q = Query()
        res = self.db.search(q.id == doc_id)
        if not res:
            return None
        return DocumentMeta(**res[0])

    def update_meta(self, doc_id: str, updates: Dict[str, Any]) -> Optional[DocumentMeta]:
        q = Query()
        res = self.db.search(q.id == doc_id)
        if not res:
            return None
        current = res[0]
        current.update(updates)
        current["modified_at"] = self._now_iso()
        self.db.update(current, q.id == doc_id)
        return DocumentMeta(**current)

    def move(self, doc_id: str, dest_folder: Path) -> Optional[DocumentMeta]:
        meta = self.get_by_id(doc_id)
        if not meta:
            return None
        dest_folder.mkdir(parents=True, exist_ok=True)
        src_path = Path(meta.path)
        dest_path = dest_folder / src_path.name
        shutil.move(str(src_path), str(dest_path))
        return self.update_meta(doc_id, {"path": str(dest_path)})

    def rename(self, doc_id: str, new_name: str) -> Optional[DocumentMeta]:
        meta = self.get_by_id(doc_id)
        if not meta:
            return None
        src_path = Path(meta.path)
        dest_path = src_path.with_name(new_name)
        shutil.move(str(src_path), str(dest_path))
        return self.update_meta(doc_id, {"path": str(dest_path), "filename": new_name})

    def set_tags(self, doc_id: str, tags: List[str]) -> Optional[DocumentMeta]:
        return self.update_meta(doc_id, {"tags": tags})

    def add_tags(self, doc_id: str, tags: List[str]) -> Optional[DocumentMeta]:
        meta = self.get_by_id(doc_id)
        if not meta:
            return None
        new_tags = sorted(set(list(meta.tags) + list(tags)))
        return self.set_tags(doc_id, new_tags)

    def archive(self, doc_id: str) -> Optional[DocumentMeta]:
        return self.update_meta(doc_id, {"archived": True})

    # -------------- Search --------------
    def smart_search(self, query: str, top_k: int = 8) -> List[Tuple[DocumentMeta, float]]:
        """Hybrid: filter by simple heuristics, then semantic rank."""
        # naive heuristics: if contains month or client name, filter
        docs = self.list_documents()
        q = query.lower()

        def likely(doc: DocumentMeta) -> bool:
            if "invoice" in q and "invoice" not in ",".join(doc.tags).lower():
                return True  # include; tags may not be complete
            if "contract" in q and ("contract" in doc.filename.lower() or "contract" in ",".join(doc.tags).lower()):
                return True
            if "latest" in q:
                return True
            if doc.client and (doc.client.lower() in q):
                return True
            # fallback include, will be semantically ranked
            return True

        candidate_docs = [d for d in docs if likely(d)]
        # Use embeddings ranking
        scored: List[Tuple[DocumentMeta, float]] = []
        hits = self.index.search(query, top_k=max(top_k, len(candidate_docs)))
        score_map = {doc_id: score for doc_id, score in hits}
        for d in candidate_docs:
            s = score_map.get(d.id, 0.0)
            scored.append((d, s))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[: top_k]

    # -------------- Utilities --------------
    def preview_text(self, doc_id: str) -> str:
        meta = self.get_by_id(doc_id)
        if not meta:
            return ""
        path = Path(meta.path)
        text = self._read_text(path, meta.mime_type)
        return text[:MAX_TEXT_PREVIEW_CHARS]

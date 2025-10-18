from __future__ import annotations
from typing import List, Tuple, Dict, Optional
import faiss  # type: ignore
import numpy as np
from pathlib import Path
import json

from sentence_transformers import SentenceTransformer

from .config import INDEX_DIR, DEFAULT_EMBEDDING_MODEL, EMBEDDING_DIM, MAX_EMBED_TEXT_CHARS


class EmbeddingIndex:
    def __init__(self, index_dir: Path = INDEX_DIR, model_name: str = DEFAULT_EMBEDDING_MODEL) -> None:
        self.index_dir = index_dir
        self.index_path = index_dir / "faiss.index"
        self.meta_path = index_dir / "meta.json"
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.Index] = None
        self.id_to_doc: Dict[int, str] = {}
        self.doc_to_id: Dict[str, int] = {}
        self._load()

    def _load(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        if self.index_path.exists() and self.meta_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            data = json.loads(self.meta_path.read_text())
            self.id_to_doc = {int(k): v for k, v in data.get("id_to_doc", {}).items()}
            self.doc_to_id = {v: int(k) for k, v in self.id_to_doc.items()}
        else:
            self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
            self._persist()

    def _persist(self) -> None:
        assert self.index is not None
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps({"id_to_doc": self.id_to_doc}, indent=2))

    def _get_model(self) -> SentenceTransformer:
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model

    @staticmethod
    def _normalize(v: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(v, axis=1, keepdims=True) + 1e-10
        return v / norms

    def embed_text(self, text: str) -> np.ndarray:
        model = self._get_model()
        text = text[:MAX_EMBED_TEXT_CHARS]
        vec = model.encode([text], convert_to_numpy=True)
        vec = self._normalize(vec)
        return vec.astype("float32")

    def upsert_document(self, doc_id: str, text: str) -> None:
        assert self.index is not None
        vec = self.embed_text(text)
        if doc_id in self.doc_to_id:
            idx = self.doc_to_id[doc_id]
            self.index.remove_ids(np.array([idx], dtype=np.int64))
            del self.id_to_doc[idx]
        new_idx = max(self.id_to_doc.keys(), default=-1) + 1
        self.index.add_with_ids(vec, np.array([new_idx]))
        self.id_to_doc[new_idx] = doc_id
        self.doc_to_id[doc_id] = new_idx
        self._persist()

    def delete_document(self, doc_id: str) -> None:
        if doc_id not in self.doc_to_id:
            return
        assert self.index is not None
        idx = self.doc_to_id.pop(doc_id)
        self.index.remove_ids(np.array([idx], dtype=np.int64))
        self.id_to_doc.pop(idx, None)
        self._persist()

    def search(self, query: str, top_k: int = 8) -> List[Tuple[str, float]]:
        assert self.index is not None
        vec = self.embed_text(query)
        scores, ids = self.index.search(vec, top_k)
        result: List[Tuple[str, float]] = []
        for i, s in zip(ids[0], scores[0]):
            if i == -1:
                continue
            doc_id = self.id_to_doc.get(int(i))
            if doc_id is not None:
                result.append((doc_id, float(s)))
        return result

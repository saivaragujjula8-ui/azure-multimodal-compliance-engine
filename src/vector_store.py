from dataclasses import dataclass
import numpy as np

from .chunking import EvidenceChunk


@dataclass(frozen=True)
class SearchResult:
    chunk: EvidenceChunk
    score: float


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._items: list[tuple[EvidenceChunk, np.ndarray]] = []

    def add(self, chunk: EvidenceChunk, embedding: np.ndarray) -> None:
        self._items.append((chunk, embedding))

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> list[SearchResult]:
        scored = [
            SearchResult(chunk=chunk, score=float(np.dot(query_embedding, embedding)))
            for chunk, embedding in self._items
        ]
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

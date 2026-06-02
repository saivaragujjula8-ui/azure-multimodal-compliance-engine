import hashlib
import numpy as np


class LocalEmbeddingModel:
    """Deterministic hashing embeddings for local demos and tests."""

    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimensions, dtype=float)
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        return vector if norm == 0 else vector / norm


def get_embedding_model() -> LocalEmbeddingModel:
    return LocalEmbeddingModel()

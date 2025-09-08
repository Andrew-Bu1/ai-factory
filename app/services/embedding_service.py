from sentence_transformers import SentenceTransformer
import numpy as np
from app.core.config import settings

class EmbeddingService:
    _model: SentenceTransformer | None = None

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(settings.embedding_model_name, device=settings.embedding_device)
        return cls._model

    @classmethod
    def embed(cls, texts: list[str]) -> list[list[float]]:
        model = cls._get_model()
        vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return vectors.astype(np.float32).tolist()

from sentence_transformers import SentenceTransformer
import asyncio
import logging

_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")


class EmbeddingService:
    def __init__(self, device: str = "cpu"):
        self.device: str = device
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def embed(self, *, model: str, inputs: list[str] | str) -> list[list[float]]:
        try:
            vectors = await asyncio.to_thread(
                _model.encode, inputs, convert_to_numpy=True, show_progress_bar=False
            )
            return vectors.tolist()
        except Exception as e:
            self._logger.error(f"Error during embedding: {e}")
            raise e

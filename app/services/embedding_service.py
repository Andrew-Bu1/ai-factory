from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Union, List
import asyncio
import logging

_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
class EmbeddingService:
    def __init__(
        self,
        device: str = "cpu"
    ):
        self.device = device   
        self.logger = logging.getLogger(__name__)     

    async def embed(self, *, model: str, inputs: Union[List[str], str]) -> List[List[float]]:
        try:
            vectors = await asyncio.to_thread(
                _model.encode,
                inputs,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            self.logger.debug(f"vectors {vectors}")
            return vectors.tolist()
        except Exception as e:
            self.logger.error(f"Error during embedding: {e}")
            return None

        
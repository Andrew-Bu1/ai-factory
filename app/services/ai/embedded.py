from sentence_transformers import SentenceTransformer
import asyncio
from typing import Any
from .base import BaseModel
import os


class EmbeddingModel(BaseModel):
    """AI model for generating embeddings using SentenceTransformer."""
    
    def __init__(self, device: str = "cpu"):
        """Initialize embedding model without loading any specific model.
        
        Args:
            device: Device to run model on ('cpu', 'cuda', 'mps', etc.)
        """
        self.device = device


    async def infer(
        self, 
        inputs: list[str], 
        model_id: str = "all-MiniLM-L6-v2",
        normalize_embeddings: bool = True,
        **kwargs
    ) -> list[list[float]]:
        """Generate embeddings for the given inputs.
        
        Args:
            inputs: Input string or list of strings to embed
            model_id: SentenceTransformer model ID to use
            normalize_embeddings: Whether to normalize embeddings
            **kwargs: Additional parameters for model.encode()
            
        Returns:
            List of embeddings, each embedding is a list of floats
        """
        if isinstance(inputs, str):
            inputs = [inputs]
        
        base = os.path.dirname(os.path.abspath(__file__))

        model = SentenceTransformer(f"{base}/models/{model_id}", device=self.device)
        
        # Run encoding in executor to avoid blocking
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None, 
            lambda: model.encode(inputs, normalize_embeddings=normalize_embeddings, **kwargs)
        )
        return embeddings.tolist()
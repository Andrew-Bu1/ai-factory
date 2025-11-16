from abc import ABC, abstractmethod
from typing import Any

class BaseModel(ABC):
    """Abstract base class for AI models."""
    
    @abstractmethod
    async def infer(self, inputs: list[str], **kwargs) -> Any:
        """Generate response based on the input.
        
        Args:
            inputs: Input string or list of strings
            **kwargs: Additional model-specific parameters
            
        Returns:
            Generated response (type depends on model implementation)
        """
        pass

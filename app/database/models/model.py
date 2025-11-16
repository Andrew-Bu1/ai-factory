from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from .base import BaseModel, TimestampMixin, IDMixin


class Model(BaseModel, TimestampMixin, IDMixin):
    __tablename__ = "models"

    name = Column(String(255), nullable=False)
    provider = Column(String(100), nullable=False)  # e.g., "openai", "anthropic", "cohere"
    model_id = Column(String(255), nullable=False)  # e.g., "gpt-4", "claude-3", etc.
    model_type = Column(String(50), nullable=False)  # e.g., "chat", "completion", "embedding"
    description = Column(Text, nullable=True)
    
    # Model capabilities and limits
    max_tokens = Column(Integer, nullable=True)
    input_cost_per_token = Column(Float, nullable=True)  # Cost per input token
    output_cost_per_token = Column(Float, nullable=True)  # Cost per output token
    context_window = Column(Integer, nullable=True)  # Context window size
    dimension = Column(Integer, nullable=True)  # For embedding models
   
    # Metadata
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}', provider='{self.provider}', model_id='{self.model_id}')>"
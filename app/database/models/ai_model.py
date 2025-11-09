from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.database.base import Base


class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    provider = Column(String(100), nullable=False)  # e.g., "openai", "anthropic", "cohere"
    model_id = Column(String(255), nullable=False)  # e.g., "gpt-4", "claude-3", etc.
    model_type = Column(String(50), nullable=False)  # e.g., "chat", "completion", "embedding"
    description = Column(Text, nullable=True)
    
    # Model capabilities and limits
    max_tokens = Column(Integer, nullable=True)
    input_cost_per_token = Column(Float, nullable=True)  # Cost per input token
    output_cost_per_token = Column(Float, nullable=True)  # Cost per output token
    context_window = Column(Integer, nullable=True)  # Context window size
   
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}', provider='{self.provider}', model_id='{self.model_id}')>"
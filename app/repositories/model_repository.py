from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models.ai_model import AIModel
from app.api.schemas.ai_model import AIModelCreate, AIModelUpdate


class AIModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ai_model: AIModelCreate) -> AIModel:
        """Create a new AI model"""
        db_ai_model = AIModel(**ai_model.model_dump())
        self.db.add(db_ai_model)
        self.db.commit()
        self.db.refresh(db_ai_model)
        return db_ai_model

    def get_by_id(self, model_id: int) -> Optional[AIModel]:
        """Get AI model by ID"""
        return self.db.query(AIModel).filter(AIModel.id == model_id).first()

    def get_by_model_id(self, model_id: str, provider: str) -> Optional[AIModel]:
        """Get AI model by model_id and provider"""
        return self.db.query(AIModel).filter(
            and_(AIModel.model_id == model_id, AIModel.provider == provider)
        ).first()

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[AIModel]:
        """Get all AI models with optional filtering"""
        query = self.db.query(AIModel)
        
        if provider:
            query = query.filter(AIModel.provider == provider)
        if model_type:
            query = query.filter(AIModel.model_type == model_type)
        if is_active is not None:
            query = query.filter(AIModel.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()

    def count(
        self, 
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """Count AI models with optional filtering"""
        query = self.db.query(AIModel)
        
        if provider:
            query = query.filter(AIModel.provider == provider)
        if model_type:
            query = query.filter(AIModel.model_type == model_type)
        if is_active is not None:
            query = query.filter(AIModel.is_active == is_active)
            
        return query.count()

    def update(self, model_id: int, ai_model_update: AIModelUpdate) -> Optional[AIModel]:
        """Update an AI model"""
        db_ai_model = self.get_by_id(model_id)
        if db_ai_model:
            update_data = ai_model_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_ai_model, field, value)
            self.db.commit()
            self.db.refresh(db_ai_model)
        return db_ai_model

    def delete(self, model_id: int) -> bool:
        """Delete an AI model"""
        db_ai_model = self.get_by_id(model_id)
        if db_ai_model:
            self.db.delete(db_ai_model)
            self.db.commit()
            return True
        return False

    def soft_delete(self, model_id: int) -> Optional[AIModel]:
        """Soft delete an AI model (set is_active to False)"""
        return self.update(model_id, AIModelUpdate(is_active=False))
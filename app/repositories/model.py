from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models.model import Model
from app.api.schemas.model import ModelCreate, ModelUpdate


class ModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, model: ModelCreate) -> Model:
        """Create a new AI model"""
        db_model = Model(**model.model_dump())
        self.db.add(db_model)
        self.db.commit()
        self.db.refresh(db_model)
        return db_model
    
    def get_by_id(self, id: int) -> Optional[Model]:
        """Get AI model by ID"""
        return self.db.query(Model).filter(Model.id == id).first()

    def get_by_model_id(self, model_id: str, provider: str) -> Optional[Model]:
        """Get AI model by model_id and provider"""
        return self.db.query(Model).filter(
            and_(Model.model_id == model_id, Model.provider == provider)
        ).first()

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Model]:
        """Get all AI models with optional filtering"""
        query = self.db.query(Model)
        
        if provider:
            query = query.filter(Model.provider == provider)
        if model_type:
            query = query.filter(Model.model_type == model_type)
        
        if is_active is not None:
            query = query.filter(Model.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()

    def count(
        self, 
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """Count AI models with optional filtering"""
        query = self.db.query(Model)
        
        if provider:
            query = query.filter(Model.provider == provider)
        if model_type:
            query = query.filter(Model.model_type == model_type)
        if is_active is not None:
            query = query.filter(Model.is_active == is_active)
            
        return query.count()

    def update(self, model_id: int, ai_model_update: ModelUpdate) -> Optional[Model]:
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

    def soft_delete(self, model_id: int) -> Optional[Model]:
        """Soft delete an AI model (set is_active to False)"""
        return self.update(model_id, ModelUpdate(is_active=False))
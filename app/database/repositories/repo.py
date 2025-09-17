from typing import Any, List, Optional, Type, TypeVar, Generic, Mapping
from sqlalchemy.ext.asyncio import AsyncSession
from models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    

    async def get(self, id_: Any) -> Optional[T]:
        return await self.session.get(self.model, id_)
    
    async def get_by(self, **kwargs: Any) -> Optional[T]:
        query = await self.session.execute(
            self.model.__table__.select().filter_by(**kwargs)
        )
        return query.scalars().first()
    
    async def list(self, **kwargs: Any) -> List[T]:
        query = await self.session.execute(
            self.model.__table__.select().filter_by(**kwargs)
        )
        return query.scalars().all()
    

    async def update(self, obj: T, data: Mapping[str, Any]) -> T:
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
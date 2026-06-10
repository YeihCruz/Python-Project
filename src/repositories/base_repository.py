from typing import TypeVar, Generic, Optional, List, Type
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()
        return instance

    def get_by_id(self, id_value: int) -> Optional[ModelType]:
        return self.session.get(self.model, id_value)

    def get_all(self) -> List[ModelType]:
        result = self.session.execute(select(self.model))
        return list(result.scalars().all())

    def update(self, id_value: int, **kwargs) -> Optional[ModelType]:
        instance = self.get_by_id(id_value)
        if instance is None:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.session.flush()
        return instance

    def delete(self, id_value: int) -> bool:
        instance = self.get_by_id(id_value)
        if instance is None:
            return False
        self.session.delete(instance)
        self.session.flush()
        return True

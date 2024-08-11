from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session, DeclarativeBase
from typing import Generic, TypeVar, List, Dict, Any, Optional, Union, Type

T = TypeVar('T', bound=DeclarativeBase)


class BaseRepository(Generic[T], ABC):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def list(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        page: int = 1,
        per_page: int = 10,
        order_by: Optional[str] = None
    ) -> List[T]:
        query = select(self.model)

        if filter_params:
            for key, value in filter_params.items():
                query = query.filter(getattr(self.model, key) == value)

        if order_by:
            query = query.order_by(order_by)

        query = query.offset((page - 1) * per_page).limit(per_page)

        return list(self.session.execute(query).scalars())

    def get_by_id(self, id: str) -> Optional[T]:
        return self.session.get(self.model, id)

    def get_by_props(self, props: Dict[str, Any]) -> Optional[T]:
        return self.session.query(self.model).filter_by(**props).first()

    def create(self, data: Dict[str, Any]) -> T:
        entity = self.model(**data)
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, id: str, changes: Dict[str, Any]) -> Optional[T]:
        entity = self.get_by_id(id)
        if entity:
            for key, value in changes.items():
                setattr(entity, key, value)
            self.session.commit()
            return entity
        return None

    def delete(self, id: str) -> None:
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()

    def delete_all(self) -> None:
        self.session.execute(delete(self.model))
        self.session.commit()

    def delete_by_properties(self, **kwargs) -> None:
        query = delete(self.model).filter_by(**kwargs)
        self.session.execute(query)
        self.session.commit()

    def upsert(self, entity: Dict[str, Any]) -> Optional[T]:
        id = entity.get('id')
        try:
            if id is None or self.get_by_id(id) is None:
                return self.create(entity)
            return self.update(id, entity)
        except IntegrityError:
            self.session.rollback()
            if id is not None:
                return self.update(id, entity)
            raise

    def count(self, filter_params: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count()).select_from(self.model)

        if filter_params:
            for key, value in filter_params.items():
                query = query.filter(getattr(self.model, key) == value)

        return self.session.execute(query).scalar_one()

    def bulk_create(self, entities: List[Dict[str, Any]]) -> List[T]:
        model_entities = [self.model(**entity) for entity in entities]
        self.session.add_all(model_entities)
        self.session.commit()
        return model_entities

    def bulk_update(self, entities: List[Dict[str, Any]]) -> List[T]:
        updated_entities = []
        for entity_dict in entities:
            entity = self.model(**entity_dict)
            updated_entity = self.session.merge(entity)
            updated_entities.append(updated_entity)
        self.session.commit()
        return updated_entities

    @abstractmethod
    def to_dict(self, entity: T) -> Dict[str, Any]:
        pass

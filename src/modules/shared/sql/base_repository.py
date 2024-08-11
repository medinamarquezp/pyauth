from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session, DeclarativeBase
from typing import Generic, TypeVar, List, Dict, Any, Optional, Union, Type

IdType = Union[int, str]
T = TypeVar('T', bound=DeclarativeBase)


class BaseRepository(Generic[T], ABC):
    """
    A base repository class for database operations using SQLAlchemy.

    This class provides common CRUD operations and query methods for a given model.
    It is designed to be subclassed for specific entity types.
    """

    def __init__(self, session: Session, model: Type[T]):
        """
        Initialize the repository with a database session and model class.

        :param session: SQLAlchemy database session
        :param model: The model class this repository will operate on
        """
        self.session = session
        self.model = model

    def list(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        page: int = 1,
        per_page: int = 10,
        order_by: Optional[str] = None
    ) -> List[T]:
        """
        Retrieve a list of entities with optional filtering, pagination, and ordering.

        :param filter_params: Dictionary of filter parameters
        :param page: Page number for pagination
        :param per_page: Number of items per page
        :param order_by: Column name to order by
        :return: List of entities
        """
        query = select(self.model)

        if filter_params:
            for key, value in filter_params.items():
                query = query.filter(getattr(self.model, key) == value)

        if order_by:
            query = query.order_by(order_by)

        query = query.offset((page - 1) * per_page).limit(per_page)

        return list(self.session.execute(query).scalars())

    def get_by_id(self, id: IdType) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param id: The ID of the entity to retrieve
        :return: The entity if found, None otherwise
        """
        return self.session.get(self.model, id)

    def create(self, entity: T) -> T:
        """
        Create a new entity in the database.

        :param entity: The entity to create
        :return: The created entity
        """
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, entity: T) -> T:
        """
        Update an existing entity in the database.

        :param entity: The entity to update
        :return: The updated entity
        """
        self.session.merge(entity)
        self.session.commit()
        return entity

    def delete(self, entity: T) -> None:
        """
        Delete an entity from the database.

        :param entity: The entity to delete
        """
        self.session.delete(entity)
        self.session.commit()

    def delete_all(self) -> None:
        """
        Delete all entities of this model from the database.
        """
        self.session.execute(delete(self.model))
        self.session.commit()

    def delete_by_id(self, id: Any) -> None:
        """
        Delete an entity by its ID.

        :param id: The ID of the entity to delete
        """
        entity = self.get_by_id(id)
        if entity:
            self.delete(entity)

    def delete_by_properties(self, **kwargs) -> None:
        """
        Delete entities that match the given properties.

        :param kwargs: Property name-value pairs to match
        """
        query = delete(self.model).filter_by(**kwargs)
        self.session.execute(query)
        self.session.commit()

    def upsert(self, entity: T) -> T:
        """
        Create a new entity or update if it already exists.

        :param entity: The entity to upsert
        :return: The created or updated entity
        """
        try:
            return self.create(entity)
        except IntegrityError:
            self.session.rollback()
            return self.update(entity)

    def count(self, filter_params: Optional[Dict[str, Any]] = None) -> int:
        """
        Count the number of entities, optionally filtered.

        :param filter_params: Dictionary of filter parameters
        :return: The count of entities
        """
        query = select(func.count()).select_from(self.model)

        if filter_params:
            for key, value in filter_params.items():
                query = query.filter(getattr(self.model, key) == value)

        return self.session.execute(query).scalar_one()

    def bulk_create(self, entities: List[T]) -> List[T]:
        """
        Create multiple entities in the database.

        :param entities: List of entities to create
        :return: List of created entities
        """
        self.session.add_all(entities)
        self.session.commit()
        return entities

    def bulk_update(self, entities: List[T]) -> List[T]:
        """
        Update multiple entities in the database.

        :param entities: List of entities to update
        :return: List of updated entities
        """
        for entity in entities:
            self.session.merge(entity)
        self.session.commit()
        return entities

    @abstractmethod
    def to_dict(self, entity: T) -> Dict[str, Any]:
        """
        Convert an entity to a dictionary representation.
        This method should be implemented by subclasses.

        :param entity: The entity to convert
        :return: Dictionary representation of the entity
        """
        pass

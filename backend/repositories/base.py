from abc import ABC, abstractmethod

from typing import TypeVar, Generic, Type, List

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


Model = TypeVar("Model", bound=Base)


class AbstractRepository(ABC, Generic[Model]):
    @abstractmethod
    async def create(self, obj: dict) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int, limit: int) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, obj: dict) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class BaseRepository(AbstractRepository[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, obj: dict) -> Model:
        """
        Create a new instance of the model.

        Args:
        obj (dict): A dictionary of the model's fields with their values.

        Returns:
        Model: The newly created instance.
        """

        stmt = insert(self.model).values(**obj).returning(self.model)
        res = await self.session.execute(stmt)

        return res.scalar_one()

    async def get(self, id: int) -> Model | None:
        """
        Get a model instance by its id.

        Args:
        id (int): The id of the instance to be retrieved.

        Returns:
        Model | None: The instance with the given id or None if not found.
        """

        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def list(self, skip: int, limit: int) -> List[Model]:
        """
        Retrieve a list of model instances.

        Args:
        skip (int): The number of rows to skip.
        limit (int): The number of rows to return.

        Returns:
        List[Model]: A list of model instances.
        """

        stmt = (
            select(self.model)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)

        return list(res.scalars().all())

    async def update(self, id: int, obj: dict) -> Model | None:
        """
        Update a model instance by its id.

        Args:
        id (int): The id of the instance to be updated.
        obj (dict): The updated fields of the instance.

        Returns:
        Model | None: The updated instance or None if not found.
        """

        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def delete(self, id: int) -> bool:
        """
        Delete an instance of the model by its id.

        Args:
        id (int): The id of the instance to be deleted.

        Returns:
        bool: True if the instance was deleted, False if not found.
        """

        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none() is not None

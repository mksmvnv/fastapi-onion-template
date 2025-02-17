from uuid import UUID
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
    async def get(self, id: UUID) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int, limit: int) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, obj: dict) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        raise NotImplementedError


class BaseRepository(AbstractRepository[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, obj: dict) -> Model:
        stmt = insert(self.model).values(**obj).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, id: UUID) -> Model | None:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list(self, skip: int, limit: int) -> List[Model]:
        stmt = (
            select(self.model)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update(self, id: UUID, obj: dict) -> Model | None:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete(self, id: UUID) -> bool:
        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

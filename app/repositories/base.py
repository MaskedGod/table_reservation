from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Абстрактный репозиторий для базовых CRUD-операций.

    :param session: SQLAlchemy асинхронная сессия
    :param model: SQLAlchemy модель (ORM-класс)
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_all(self) -> list[ModelType]:
        """
        Получить все записи из таблицы.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """
        Получить запись по ID.
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def create(self, obj: ModelType) -> ModelType:
        """Создать и сохранить новую запись."""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        """
        Удалить запись по ID.
        Возвращает True, если удаление успешно, иначе False.
        """
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

from typing import Generic, TypeVar


from app.repositories.base import BaseRepository


ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Абстрактный базовый сервис, предоставляющий базовые CRUD-операции.
    Предназначен для наследования в конкретных сервисах.
    """

    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    async def get_all(self) -> list[ModelType]:
        """Получить все записи."""
        return await self.repository.get_all()

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """Получить запись по ID."""
        return await self.repository.get_by_id(obj_id)

    async def delete(self, obj_id: int) -> bool:
        """Удалить запись по ID."""
        return await self.repository.delete(obj_id)

    async def create(self, obj: ModelType) -> ModelType:
        """Создать новую запись."""
        return await self.repository.create(obj)

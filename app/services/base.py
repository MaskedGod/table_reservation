from typing import Generic, TypeVar


from app.repositories.base import BaseRepository


ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Базовый абстрактный сервис, предоставляющий стандартные CRUD-операции.

    Служит основой для конкретных сервисов, делегируя операции сохранения данных
    в репозиторий. Использует дженерики для работы с разными типами моделей.

    Параметры типа:
        ModelType: Тип доменной модели, с которой работает сервис.

    Атрибуты:
        repository (BaseRepository[ModelType]): Репозиторий для операций с данными.
    """

    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        """Инициализирует сервис экземпляром репозитория.

        Аргументы:
            repository: Реализация репозитория для работы с данными.
        """
        self.repository = repository

    async def get_all(self) -> list[ModelType]:
        """Получает все экземпляры модели из репозитория.

        Возвращает:
            Список всех экземпляров модели. Пустой список, если данных нет.
        """
        return await self.repository.get_all()

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """Получает один экземпляр модели по его ID.

        Аргументы:
            obj_id: Уникальный идентификатор модели.

        Возвращает:
            Экземпляр модели если найден, иначе None.
        """
        return await self.repository.get_by_id(obj_id)

    async def delete(self, obj_id: int) -> bool:
        """Удаляет экземпляр модели по его ID.

        Аргументы:
            obj_id: Уникальный идентификатор модели для удаления.

        Возвращает:
            True если удаление успешно, False если модель не найдена.
        """
        return await self.repository.delete(obj_id)

    async def create(self, obj: ModelType) -> ModelType:
        """Создает новый экземпляр модели.

        Аргументы:
            obj: Экземпляр модели для создания.

        Возвращает:
            Созданный экземпляр модели.
        """
        return await self.repository.create(obj)

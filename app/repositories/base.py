from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий для работы с базой данных.

    Предоставляет стандартный набор CRUD-операций для SQLAlchemy моделей.
    Реализует паттерн Repository для абстракции работы с БД.

    Параметры типа:
        ModelType: Тип SQLAlchemy ORM-модели, с которой работает репозиторий.

    Атрибуты:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
        model (Type[ModelType]): Класс SQLAlchemy ORM-модели
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        """
        Инициализирует репозиторий.

        Аргументы:
            session: Асинхронная сессия для работы с БД
            model: ORM-класс модели, с которой будет работать репозиторий
        """
        self.session = session
        self.model = model

    async def get_all(self) -> list[ModelType]:
        """
        Получает все записи указанной модели из базы данных.

        Возвращает:
            Список всех объектов модели. Если записей нет, вернет пустой список.

        Пример:
            >>> repo = BaseRepository(session, User)
            >>> users = await repo.get_all()
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """
        Находит запись по первичному ключу (ID).

        Аргументы:
            obj_id: Идентификатор искомой записи

        Возвращает:
            Объект модели если найден, None если запись не существует

        Пример:
            >>> user = await repo.get_by_id(1)
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def create(self, obj: ModelType) -> ModelType:
        """
        Создает новую запись в базе данных.

        Аргументы:
            obj: Объект модели для сохранения

        Возвращает:
            Созданный объект модели с обновленными данными (например, ID)

        Исключения:
            sqlalchemy.exc.SQLAlchemyError: При ошибках работы с БД

        Пример:
            >>> new_user = User(name="John")
            >>> created_user = await repo.create(new_user)
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        """
        Удаляет запись по идентификатору.

        Аргументы:
            obj_id: Идентификатор удаляемой записи

        Возвращает:
            True если удаление прошло успешно,
            False если запись с указанным ID не найдена

        Пример:
            >>> success = await repo.delete(1)
            >>> if success:
            ...     print("Запись удалена")
        """
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

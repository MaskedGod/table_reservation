from sqlalchemy.ext.asyncio import AsyncSession


from app.models.table import Table
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    """
    Репозиторий для управления столиками (Table).

    Наследует базовые CRUD-операции от BaseRepository и предоставляет
    специализированные методы для работы со столиками.

    Атрибуты:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        model (Type[Table]): Модель столика, с которой работает репозиторий.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализирует репозиторий столиков.

        Аргументы:
            session: Асинхронная сессия для работы с базой данных.
        """
        super().__init__(session, Table)

from app.models.table import Table
from app.repositories.table_repo import TableRepository
from app.services.base import BaseService


class TableService(BaseService[Table]):
    """
    Сервис для работы со столиками в ресторане.

    Наследует базовые CRUD-операции от BaseService и предоставляет
    дополнительную функциональность для управления столиками.

    Атрибуты:
        table_repo (TableRepository): Репозиторий для работы
            со столиками в базе данных.
    """

    def __init__(self, table_repo: TableRepository) -> None:
        """
        Инициализирует сервис для работы со столиками.

        Аргументы:
            table_repo: Репозиторий для операций с данными столиков.
        """
        super().__init__(table_repo)
        self.table_repo = table_repo

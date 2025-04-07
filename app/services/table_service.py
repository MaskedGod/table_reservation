from app.models.table import Table
from app.repositories.table_repo import TableRepository
from app.services.base import BaseService


class TableService(BaseService[Table]):
    """
    Сервис для управления столиками.
    """

    def __init__(self, table_repo: TableRepository):
        super().__init__(table_repo)
        self.table_repo = table_repo

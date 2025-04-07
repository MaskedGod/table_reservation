from sqlalchemy.ext.asyncio import AsyncSession


from app.models.table import Table
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    """
    Репозиторий для управления столиками (Table).
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, Table)

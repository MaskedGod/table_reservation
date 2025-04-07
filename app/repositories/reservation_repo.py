from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.reservation import Reservation
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """
    Репозиторий для управления бронями (Reservation).
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, Reservation)

    async def get_reservations_by_table(
        self, table_id: int, exclude_id: int | None = None
    ) -> list[Reservation]:
        """
        Получить все бронирования для указанного столика.
        """
        query = select(self.model).where(self.model.table_id == table_id)
        if exclude_id:
            query = query.where(self.model.id != exclude_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def has_conflict(
        self,
        table_id: int,
        start_time: datetime,
        duration: int,
        exclude_id: int | None = None,
    ) -> bool:
        """
        Проверяет, есть ли конфликт времени для указанного столика.
        """
        reservations = await self.get_reservations_by_table(table_id, exclude_id)
        new_end = start_time + timedelta(minutes=duration)

        for reservation in reservations:
            existing_end = reservation.reservation_time + timedelta(
                minutes=reservation.duration_minutes
            )

            # Проверяем пересечение временных интервалов
            if start_time < existing_end and new_end > reservation.reservation_time:
                return True

        return False

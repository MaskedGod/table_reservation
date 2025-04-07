from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.models.reservation import Reservation
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """
    Репозиторий для управления бронями (Reservation).
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, Reservation)

    async def has_conflict(
        self, table_id: int, start_time: datetime, duration: int
    ) -> bool:
        """
        Проверка на пересечение брони по времени.
        Возвращает True, если есть конфликт.
        """
        end_time = start_time + timedelta(minutes=duration)

        stmt = select(Reservation).where(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            (
                Reservation.reservation_time
                + timedelta(minutes=Reservation.duration_minutes)
            )
            > start_time,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

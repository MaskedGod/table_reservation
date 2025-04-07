from app.models.reservation import Reservation
from app.repositories.reservation_repo import ReservationRepository
from app.services.base import BaseService


class ReservationService(BaseService[Reservation]):
    """
    Сервис для управления бронями.
    """

    def __init__(self, reservation_repo: ReservationRepository):
        super().__init__(reservation_repo)
        self.reservation_repo = reservation_repo

    async def create_reservation_if_available(
        self, reservation: Reservation
    ) -> Reservation | None:
        """
        Попытаться создать бронь, если нет конфликта.

        :return: Reservation если успешно, иначе None.
        """
        has_conflict = await self.reservation_repo.has_conflict(
            table_id=reservation.table_id,
            start_time=reservation.reservation_time,
            duration=reservation.duration_minutes,
        )

        if has_conflict:
            return None

        return await self.reservation_repo.create(reservation)

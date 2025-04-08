from app.models.reservation import Reservation
from app.repositories.reservation_repo import ReservationRepository
from app.services.base import BaseService


class ReservationService(BaseService[Reservation]):
    """
    Сервис для работы с бронированиями.

    Наследует базовые CRUD-операции от BaseService и добавляет
    специфичную для бронирований бизнес-логику.

    Атрибуты:
        reservation_repo (ReservationRepository): Репозиторий для работы
            с бронированиями в базе данных.
    """

    def __init__(self, reservation_repo: ReservationRepository) -> None:
        """
        Инициализирует сервис бронирований.

        Аргументы:
            reservation_repo: Репозиторий для работы с бронированиями.
        """
        super().__init__(reservation_repo)
        self.reservation_repo = reservation_repo

    async def create_reservation_if_available(
        self, reservation: Reservation
    ) -> Reservation | None:
        """
        Создает новое бронирование, если нет конфликтов по времени.

        Проверяет наличие существующих броней на указанный стол
        в запрашиваемый временной интервал перед созданием.

        Аргументы:
            reservation: Объект бронирования для создания.

        Возвращает:
            Созданное бронирование если нет конфликтов,
            None если есть пересечение с существующими бронями.

        Пример:
            >>> reservation = Reservation(...)
            >>> created = await service.create_reservation_if_available(reservation)
            >>> if created:
            ...     print("Бронь создана")
        """
        has_conflict = await self.reservation_repo.has_conflict(
            table_id=reservation.table_id,
            start_time=reservation.reservation_time,
            duration=reservation.duration_minutes,
        )

        if has_conflict:
            return None

        return await self.reservation_repo.create(reservation)

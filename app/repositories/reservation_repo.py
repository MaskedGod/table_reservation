from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.reservation import Reservation
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """
    Репозиторий для работы с бронированиями столиков.

    Наследует базовые CRUD-операции от BaseRepository и добавляет
    специализированные методы для работы с бронированиями.

    Атрибуты:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
        model (Type[Reservation]): Модель бронирования
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализирует репозиторий бронирований.

        Аргументы:
            session: Асинхронная сессия для работы с базой данных
        """
        super().__init__(session, Reservation)

    async def get_reservations_by_table(
        self, table_id: int, exclude_id: int | None = None
    ) -> list[Reservation]:
        """
        Получает все бронирования для указанного столика.

        Аргументы:
            table_id: Идентификатор столика
            exclude_id: Идентификатор бронирования, которое следует исключить
                       из результатов (например, текущее редактируемое бронирование)

        Возвращает:
            Список бронирований для указанного столика. Если бронирований нет,
            возвращает пустой список.

        Пример:
            >>> reservations = await repo.get_reservations_by_table(table_id=1)
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
        Проверяет наличие временного конфликта для нового бронирования.

        Аргументы:
            table_id: Идентификатор столика
            start_time: Время начала нового бронирования
            duration: Длительность бронирования в минутах
            exclude_id: Идентификатор бронирования, которое следует исключить
                       из проверки (например, при изменении существующего бронирования)

        Возвращает:
            True если обнаружен конфликт времени, False если столик свободен

        Логика проверки:
            Конфликт определяется как пересечение временных интервалов:
            - Новое бронирование: [start_time, start_time + duration]
            - Существующее бронирование: [reservation_time, reservation_time + duration_minutes]

        Пример:
            >>> conflict = await repo.has_conflict(
            ...     table_id=1,
            ...     start_time=datetime(2023, 1, 1, 12, 0),
            ...     duration=120
            ... )
        """
        reservations = await self.get_reservations_by_table(table_id, exclude_id)
        new_end = start_time + timedelta(minutes=duration)

        for reservation in reservations:
            existing_end = reservation.reservation_time + timedelta(
                minutes=reservation.duration_minutes
            )

            if start_time < existing_end and new_end > reservation.reservation_time:
                return True

        return False

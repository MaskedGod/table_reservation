from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.database import get_db
from app.repositories.table_repo import TableRepository
from app.repositories.reservation_repo import ReservationRepository
from app.services.table_service import TableService
from app.services.reservation_service import ReservationService


def get_table_service(
    session: AsyncSession = Depends(get_db),
) -> TableService:
    """
    Фабрика для создания экземпляра TableService.

    Используется как зависимость в FastAPI для предоставления сервиса управления столиками.
    Создает TableService с репозиторием, использующим предоставленную сессию базы данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных (автоматически внедряется через Depends).

    Возвращает:
        TableService: Экземпляр сервиса для работы со столиками.
    """
    return TableService(TableRepository(session))


def get_reservation_service(
    session: AsyncSession = Depends(get_db),
) -> ReservationService:
    """
    Фабрика для создания экземпляра ReservationService.

    Используется как зависимость в FastAPI для предоставления сервиса управления бронированиями.
    Создает ReservationService с репозиторием, использующим предоставленную сессию базы данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных (автоматически внедряется через Depends).

    Возвращает:
        ReservationService: Экземпляр сервиса для работы с бронированиями.
    """
    return ReservationService(ReservationRepository(session))

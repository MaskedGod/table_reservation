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
    Получение зависимости TableService.
    """
    return TableService(TableRepository(session))


def get_reservation_service(
    session: AsyncSession = Depends(get_db),
) -> ReservationService:
    """
    Получение зависимости ReservationService.
    """
    return ReservationService(ReservationRepository(session))

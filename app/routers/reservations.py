from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_service import ReservationService
from app.dependencies.services import get_reservation_service

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=list[ReservationRead])
async def get_reservations(
    service: ReservationService = Depends(get_reservation_service),
):
    """
    Получить список всех бронирований.

    Возвращает список всех существующих бронирований в системе.
    Использует сервис `ReservationService` для выполнения запроса к базе данных.

    Возвращает:
        list[ReservationRead]: Список бронирований в формате `ReservationRead`.
    """
    return await service.get_all()


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_in: ReservationCreate,
    service: ReservationService = Depends(get_reservation_service),
):
    """
    Создать новое бронирование.

    Проверяет доступность столика на указанное время и создает бронирование,
    если нет конфликтов. Если столик уже забронирован, возвращает ошибку 409 Conflict.

    Аргументы:
        reservation_in (ReservationCreate): Данные для создания нового бронирования.

    Возвращает:
        ReservationRead: Созданное бронирование в формате `ReservationRead`.

    Исключения:
        HTTPException(409): Если столик уже забронирован на указанное время.
    """
    from app.models.reservation import Reservation

    reservation = Reservation(**reservation_in.model_dump())

    created = await service.create_reservation_if_available(reservation)
    if not created:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Table is already reserved at this time.",
        )
    return created


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_reservation_service),
):
    """
    Удалить бронирование по ID.

    Удаляет бронирование с указанным ID. Если бронирование не найдено,
    возвращает ошибку 404 Not Found.

    Аргументы:
        reservation_id (int): Идентификатор бронирования для удаления.

    Исключения:
        HTTPException(404): Если бронирование с указанным ID не существует.
    """
    success = await service.delete(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")

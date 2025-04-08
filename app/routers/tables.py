from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.table import TableCreate, TableRead
from app.services.table_service import TableService
from app.dependencies.services import get_table_service

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableRead])
async def get_tables(service: TableService = Depends(get_table_service)):
    """
    Получить список всех столиков.

    Возвращает список всех существующих столиков в системе.
    Использует сервис `TableService` для выполнения запроса к базе данных.

    Возвращает:
        list[TableRead]: Список столиков в формате `TableRead`.
    """
    return await service.get_all()


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(
    table_in: TableCreate,
    service: TableService = Depends(get_table_service),
):
    """
    Создать новый столик.

    Создает новый столик в системе на основе предоставленных данных.

    Аргументы:
        table_in (TableCreate): Данные для создания нового столика.

    Возвращает:
        TableRead: Созданный столик в формате `TableRead`.
    """
    from app.models.table import Table

    new_table = Table(**table_in.model_dump())
    return await service.create(new_table)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
    service: TableService = Depends(get_table_service),
):
    """
    Удалить столик по ID.

    Удаляет столик с указанным ID. Если столик не найден,
    возвращает ошибку 404 Not Found.

    Аргументы:
        table_id (int): Идентификатор столика для удаления.

    Исключения:
        HTTPException(404): Если столик с указанным ID не существует.
    """
    success = await service.delete(table_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")

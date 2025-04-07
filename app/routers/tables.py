from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.table import TableCreate, TableRead
from app.services.table_service import TableService
from app.dependencies.services import get_table_service

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableRead])
async def get_tables(service: TableService = Depends(get_table_service)):
    return await service.get_all()


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(
    table_in: TableCreate,
    service: TableService = Depends(get_table_service),
):
    from app.models.table import Table

    new_table = Table(**table_in.model_dump())
    return await service.create(new_table)


@router.get("/{table_id}", response_model=TableRead)
async def get_table_by_id(
    table_id: int,
    service: TableService = Depends(get_table_service),
):
    table = await service.get_by_id(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
    service: TableService = Depends(get_table_service),
):
    success = await service.delete(table_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")

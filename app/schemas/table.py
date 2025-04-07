from pydantic import BaseModel, Field


class TableBase(BaseModel):
    name: str = Field(..., example="Table 1")
    seats: int = Field(..., ge=1, example=4)
    location: str | None = Field(None, example="зал у окна")


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    class Config:
        from_attributes = True

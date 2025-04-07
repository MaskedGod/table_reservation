from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


from app.core.database import get_db


app = FastAPI(
    title="Reserver",
    description="REST API for restaurant table reservations. The service allow creating, viewing, and deleting reservations, as well as managing tables and time slots.",
)


@app.get("/")
async def health_check(session=Depends(get_db)):
    "Return database connection status"
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as err:
        raise HTTPException(503, detail={"status": "down", "db": "unhealthy"}) from err
    else:
        return {"status": "ok", "db": "healthy"}

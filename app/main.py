from fastapi import FastAPI


from app.routers import tables, reservations


app = FastAPI(
    title="Reserver",
    description="REST API for restaurant table reservations. The service allow creating, viewing, and deleting reservations, as well as managing tables and time slots.",
)


app.include_router(tables.router)
app.include_router(reservations.router)

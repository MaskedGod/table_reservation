from fastapi import FastAPI


app = FastAPI(
    title="Reserver",
    description="REST API for restaurant table reservations. The service allow creating, viewing, and deleting reservations, as well as managing tables and time slots.",
)

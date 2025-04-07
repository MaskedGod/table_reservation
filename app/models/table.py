from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer


from app.core.database import Base


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return (
            f"Table(name='{self.name}', seats={self.seats}, location='{self.location}')"
        )

    def __repr__(self) -> str:
        return f"<Table(id={self.id}, name='{self.name}')>"

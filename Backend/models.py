
import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Identity,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "Tasks"

    TaskId: Mapped[int] = mapped_column(
        Integer,
        Identity(start=1, increment=1),
        primary_key=True,
    )

    Title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    Status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'Pending'"),
    )

    CreatedAtUtc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    Description: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    DueDateUtc: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
    )

    UpdatedAtUtc: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
    )

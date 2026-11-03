from typing import Optional
import datetime

from sqlalchemy import Identity, Integer, PrimaryKeyConstraint, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = 'Tasks'
    __table_args__ = (
        PrimaryKeyConstraint('TaskId', name='PK__Tasks__7C6949B1BE1548F3'),
    )

    TaskId: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True, autoincrement=True)
    Title: Mapped[str] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Status: Mapped[str] = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("('Pending')"))
    CreatedAtUtc: Mapped[datetime.datetime] = mapped_column(DATETIME2, nullable=False, server_default=text('(sysutcdatetime())'))
    Description: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    DueDateUtc: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)
    UpdatedAtUtc: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)

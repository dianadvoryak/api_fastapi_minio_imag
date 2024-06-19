from datetime import datetime

from database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )

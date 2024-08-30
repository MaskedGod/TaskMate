from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, CheckConstraint, text
from datetime import datetime, timedelta, timezone


from ..database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationship with tasks
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")

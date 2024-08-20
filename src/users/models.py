from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, CheckConstraint, text
from datetime import datetime, timedelta, timezone

from src.database import Base


class Users(Base):
    __tablename__ = "users"

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
    tasks = relationship("Tasks", back_populates="users")


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    # due_date: Mapped[Optional[Date]] = mapped_column(
    #     CheckConstraint("due_date >= CURRENT_DATE", name="due_date_check"),
    #     default=lambda: datetime.now(timezone.utc).date() + timedelta(days=7),
    # )

    # status: Mapped[str] = mapped_column(
    #     CheckConstraint(
    #         "status IN ('pending', 'in-progress', 'completed', 'overdue')",
    #         name="status_check",
    #     ),
    #     default="pending",
    #     nullable=False,
    # )
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=None,
    #     onupdate=datetime.now(timezone.utc),
    # )

    # Relationship with user
    users = relationship("Users", back_populates="tasks")

    # TODO Make functions inside class to check due date and change status

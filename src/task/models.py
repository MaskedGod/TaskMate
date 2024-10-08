from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, CheckConstraint, text
from datetime import datetime, timedelta, timezone


from ..database import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(
        CheckConstraint(
            "status IN ('pending', 'in-progress', 'completed', 'overdue' )",
            name="status_check",
        ),
        default="pending",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )
    due_date: Mapped[Optional[datetime]] = mapped_column(
        CheckConstraint("due_date >= CURRENT_DATE", name="due_date_check"),
        default=lambda: datetime.now(timezone.utc).date() + timedelta(days=7),
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # Relationship with user
    user: Mapped["User"] = relationship("User", back_populates="task")

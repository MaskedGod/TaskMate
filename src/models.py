from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))

    # Relationship with tasks
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # due_date = Column(Date)

    # status = Column(
    #     String,
    #     CheckConstraint(
    #         "status IN ('pending', 'in-progress', 'completed', 'overdue')",
    #         name="status_check",
    #     ),
    #     default="pending",
    #     nullable=False,
    # )
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))

    # Relationship with user
    user = relationship("User", back_populates="tasks")
    # Make functions inside class to check due date and change status

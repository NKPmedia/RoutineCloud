"""
Routine entity module.

This module defines the Routine entity for SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class Routine(Base):
    """Routine entity representing a sequence of tasks."""

    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Whether this routine is active
    is_active = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to routine_tasks (many-to-many)
    routine_tasks = relationship("RoutineTask", back_populates="routine", order_by="RoutineTask.position", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Routine(id={self.id}, name='{self.name}', is_active={self.is_active})>"

    def to_dict(self):
        """Convert the routine to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "tasks": [rt.task.to_dict() for rt in self.routine_tasks]
        }

    def start(self):
        """Start the routine."""
        self.is_active = True
        return self.routine_tasks[0].task if self.routine_tasks else None

    def stop(self):
        """Stop the routine."""
        self.is_active = False

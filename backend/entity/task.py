"""
Task entity module.

This module defines the Task entity for SQLAlchemy.
"""
from PySide6.QtSvgWidgets import QSvgWidget
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from display.utils import get_fa_path
from .base import Base

class Task(Base):
    """Task entity representing a task that can be used in multiple routines."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)
    sound = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in seconds

    # Relationship to routine_tasks (many-to-many)
    routine_tasks = relationship("RoutineTask", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        """Convert the task to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "sound": self.sound,
            "duration": self.duration
        }

    def get_item_as_widget(self):
        return QSvgWidget(
            get_fa_path(self.icon_name)
        )
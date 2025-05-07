"""
RoutineTask entity module.

This module defines the RoutineTask entity for SQLAlchemy, which represents
a single task instance within a specific routine (many RoutineTasks per Routine, but each RoutineTask belongs to only one Routine).
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class RoutineTask(Base):
    """
    RoutineTask entity representing a task instance in a specific routine.
    Each RoutineTask belongs to exactly one Routine and one Task.
    """

    __tablename__ = "routine_tasks"

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    position = Column(Integer, nullable=False)  # Position of this task in the routine (order)

    # Relationships
    routine = relationship("Routine", back_populates="routine_tasks")  # Each RoutineTask has one Routine
    task = relationship("Task", back_populates="routine_tasks")        # Each RoutineTask has one Task

    def __repr__(self):
        return f"<RoutineTask(routine_id={self.routine_id}, task_id={self.task_id}, position={self.position})>"
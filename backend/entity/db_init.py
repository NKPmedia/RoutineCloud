"""
Database initialization script.

This script initializes the database with default data.
"""

from .base import init_db, db_session
from .routine import Routine
from .task import Task
from .routine_task import RoutineTask

def create_default_routine():
    """Create the default bedtime routine with tasks."""
    # Check if the routine already exists
    routine = Routine.query.filter_by(name="Bedtime Routine").first()
    if routine:
        return routine

    # Create the routine
    routine = Routine(
        name="Bedtime Routine",
        description="A routine to help children get ready for bed"
    )

    # Create tasks
    tasks = [
        Task(
            name="Brush Teeth",
            sound="brush_teeth.mp3",
            duration=120
        ),
        Task(
            name="Put on Pajamas",
            sound="pajamas.mp3",
            duration=180
        ),
        Task(
            name="Read a Book",
            sound="book.mp3",
            duration=300
        ),
        Task(
            name="Go to Sleep",
            sound="sleep.mp3",
            duration=60
        )
    ]

    # Add tasks to the session
    for task in tasks:
        db_session.add(task)

    # Add routine to the session
    db_session.add(routine)

    # Commit to get IDs
    db_session.commit()

    # Create routine_task associations
    for i, task in enumerate(tasks):
        routine_task = RoutineTask(
            routine_id=routine.id,
            task_id=task.id,
            position=i
        )
        db_session.add(routine_task)

    # Commit the changes
    db_session.commit()

    return routine

def init_database():
    """Initialize the database with default data."""
    # Create tables
    init_db()

    # Create default routine
    create_default_routine()

    print("Database initialized with default data.")

if __name__ == "__main__":
    init_database()

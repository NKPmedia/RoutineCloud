"""
Example script demonstrating how to use the SQLAlchemy entities.

This script shows how to:
1. Initialize the database
2. Create a routine with tasks
3. Query routines and tasks
4. Update a routine and its tasks
5. Delete a routine
"""

from .base import db_session
from .routine import Routine
from .task import Task
from .routine_task import RoutineTask
from .db_init import init_database

def main():
    """Run the example."""
    # Initialize the database
    init_database()

    print("Database initialized.")

    # Query all routines
    routines = Routine.query.all()
    print(f"Found {len(routines)} routines:")
    for routine in routines:
        print(f"  - {routine}")
        for rt in routine.routine_tasks:
            print(f"    - {rt.task}")

    # Create a new routine
    new_routine = Routine(
        name="Morning Routine",
        description="A routine to help children get ready for school"
    )

    # Create tasks
    tasks = [
        Task(
            name="Wake Up",
            sound="wake_up.mp3",
            duration=60
        ),
        Task(
            name="Eat Breakfast",
            sound="breakfast.mp3",
            duration=300
        ),
        Task(
            name="Get Dressed",
            sound="get_dressed.mp3",
            duration=180
        ),
        Task(
            name="Brush Teeth",
            sound="brush_teeth.mp3",
            duration=120
        )
    ]

    # Add tasks to the session
    for task in tasks:
        db_session.add(task)

    # Commit to get task IDs
    db_session.commit()

    # Create routine_task associations
    for i, task in enumerate(tasks):
        routine_task = RoutineTask(
            routine_id=new_routine.id,
            task_id=task.id,
            position=i
        )
        db_session.add(routine_task)

    # Add routine to the session
    db_session.add(new_routine)

    # Commit the changes
    db_session.commit()

    print("\nCreated new routine:")
    print(f"  - {new_routine}")
    for rt in new_routine.routine_tasks:
        print(f"    - {rt.task}")

    # Update a routine
    bedtime_routine = Routine.query.filter_by(name="Bedtime Routine").first()
    if bedtime_routine:
        bedtime_routine.description = "Updated description for bedtime routine"

        # Create a new task
        new_task = Task(
            name="Take a Bath",
            sound="bath.mp3",
            duration=300
        )
        db_session.add(new_task)

        # Commit to get task ID
        db_session.commit()

        # Create routine_task association
        routine_task = RoutineTask(
            routine_id=bedtime_routine.id,
            task_id=new_task.id,
            position=len(bedtime_routine.routine_tasks)
        )
        db_session.add(routine_task)

        # Commit the changes
        db_session.commit()

        print("\nUpdated bedtime routine:")
        print(f"  - {bedtime_routine}")
        for rt in bedtime_routine.routine_tasks:
            print(f"    - {rt.task}")

    # Delete a routine (uncomment to test)
    # db_session.delete(new_routine)
    # db_session.commit()
    # print("\nDeleted morning routine.")

    print("\nExample complete.")

if __name__ == "__main__":
    main()

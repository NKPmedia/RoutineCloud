"""
Base module for SQLAlchemy setup.

This module provides the base class for all SQLAlchemy models and sets up the
SQLAlchemy engine and session.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Create SQLAlchemy engine
# Using SQLite for simplicity, can be changed to other databases as needed
SQLALCHEMY_DATABASE_URL = "sqlite:///./routinecloud.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread safety
db_session = scoped_session(SessionLocal)

# Create base class for all models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Initialize the database by creating all tables."""
    # Import all models here to ensure they are registered with Base
    from .task import Task
    from .routine import Routine
    from .routine_task import RoutineTask

    Base.metadata.create_all(bind=engine)

def get_db():
    """Get a database session."""
    db = db_session()
    try:
        yield db
    finally:
        db.close()

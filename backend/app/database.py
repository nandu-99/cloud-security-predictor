"""
Database configuration and session management for Cloud Security application.
Uses SQLAlchemy with PostgreSQL for production or SQLite for development.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use SQLite for easier setup (can switch to PostgreSQL if needed)
# For PostgreSQL: postgresql://user:password@localhost/cloud_security_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cloud_security.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Call this on application startup.
    """
    Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from api.models.sql_models import engine
from api.models.mongo_models import MongoDB

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongo_db() -> MongoDB:
    """
    Dependency function to get MongoDB instance.
    """
    return MongoDB()

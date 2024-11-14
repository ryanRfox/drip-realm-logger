from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
from src.config import config
from typing import Generator
from .models import Base

engine = create_engine(f"sqlite:///{config.DATABASE_PATH}")

# Create all tables if they don't exist
Base.metadata.create_all(engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close() 
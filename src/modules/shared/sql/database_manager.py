from typing import Generator
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from src.modules.shared.services import logger

from src.config import DATABASE_URL


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def generate_session(self) -> Generator[Session, None, None]:
        session: Session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Error processing transaction: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    def get_session(self) -> Session:
        with self.generate_session() as session:
            return session

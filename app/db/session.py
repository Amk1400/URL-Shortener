from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.orm import Base


class DatabaseSession:

    def __init__(self, database_url: Optional[str]) -> None:
        self.database_url = database_url
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None

    def connect(self) -> None:
        if not self.database_url:
            raise RuntimeError("Missing database URL")
        try:
            self._engine = create_engine(self.database_url, future=True)
            self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
            Base.metadata.create_all(self._engine)
        except SQLAlchemyError as exc:
            raise RuntimeError("Failed to initialize database engine") from exc

    def get_session(self) -> Session:
        if self._session_factory is None:
            raise RuntimeError("Session factory not initialized")
        return self._session_factory()

    def dispose(self) -> None:
        if self._engine:
            self._engine.dispose()
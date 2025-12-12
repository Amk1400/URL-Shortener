from typing import Optional
from pydantic import AnyHttpUrl
from sqlalchemy import func

from app.models.orm import URL
from app.repository.getter import get_all, get_by_code
from app.repository.poster import create
from app.repository.deleter import delete_by_short_code

class UrlRepository:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def get_all(self) -> list[URL]:
        return get_all(self._session_factory)

    def get_by_code(self, code: str) -> Optional[URL]:
        return get_by_code(self._session_factory, code)

    def create(self, original_url: AnyHttpUrl, expired_at=None) -> URL:
        return create(self._session_factory, original_url, expired_at)

    def delete_by_code(self, code: str) -> Optional[URL]:
        return delete_by_short_code(self._session_factory, code)
    
    def delete_expired(self) -> int:
        session = self._session_factory()
        try:
            q = session.query(URL).filter(URL.expired_at != None, URL.expired_at < func.now())
            count = q.count()
            if count:
                q.delete(synchronize_session=False)
                session.commit()
            return count
        finally:
            session.close()
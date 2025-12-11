from app.repository.deleter import delete_by_short_code as deleter_delete_by_code
from app.models.orm import URL
from pydantic import AnyHttpUrl

from app.repository.poster import create as poster_create

class UrlRepository:
    """Base repository for URL operations."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def create(self, original_url: AnyHttpUrl, expired_at=None):
        """Delegate to poster.create function."""
        return poster_create(self._session_factory, original_url, expired_at)


    def delete_by_code(self, code: str) -> URL | None:
        """Delegate to deleter.delete_by_code function."""
        return deleter_delete_by_code(self._session_factory, code)
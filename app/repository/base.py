from pydantic import AnyHttpUrl

from app.repository.getter import get_by_short_code as getter_get_by_code
from app.repository.poster import create as poster_create

class UrlRepository:
    """Base repository for URL operations."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def create(self, original_url: AnyHttpUrl, expired_at=None):
        """Delegate to poster.create function."""
        return poster_create(self._session_factory, original_url, expired_at)

    def get_by_code(self, code):
        """Delegate to getter.get_by_code function."""
        return getter_get_by_code(self._session_factory, code)

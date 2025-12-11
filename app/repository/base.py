from pydantic import AnyHttpUrl

from app.repository.poster import create as poster_create

class UrlRepository:
    """Base repository for URL operations."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def create(self, original_url: AnyHttpUrl, expired_at=None):
        """Delegate to poster.create function."""
        return poster_create(self._session_factory, original_url, expired_at)

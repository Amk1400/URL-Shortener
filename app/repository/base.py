from app.repository.deleter import delete_by_short_code as deleter_delete_by_code
from app.models.orm import URL

class UrlRepository:
    """Base repository for URL operations."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def delete_by_code(self, code: str) -> URL | None:
        """Delegate to deleter.delete_by_code function."""
        return deleter_delete_by_code(self._session_factory, code)
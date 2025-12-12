from typing import Optional, Callable, List
from pydantic import AnyHttpUrl
from sqlalchemy.orm import Session

from app.models.orm import URL
from app.repository.getter import get_all, get_by_code
from app.repository.poster import create
from app.repository.deleter import delete_by_short_code


class UrlRepository:
    """Repository façade for URL operations.

    Attributes:
        _session_factory (Callable[[], Session]): Factory to create DB sessions.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        """Initialize UrlRepository.

        Args:
            session_factory (Callable[[], Session]): Session factory callable.

        Returns:
            None

        Raises:
            None
        """
        self._session_factory = session_factory

    def get_all(self) -> List[URL]:
        """Return all URL records.

        Args:
            None

        Returns:
            List[URL]: List of URL ORM objects.

        Raises:
            RuntimeError: If underlying DB call fails.
        """
        return get_all(self._session_factory)

    def get_by_code(self, code: str) -> Optional[URL]:
        """Fetch URL by short code.

        Args:
            code (str): Short code to lookup.

        Returns:
            Optional[URL]: URL object or None.

        Raises:
            NotFoundError: If code is not found in repository.
        """
        return get_by_code(self._session_factory, code)

    def create(self, original_url: AnyHttpUrl, expired_at=None) -> URL:
        """Create new shortened URL record.

        Args:
            original_url (AnyHttpUrl): Original URL to shorten.
            expired_at (datetime|None): Optional expiration.

        Returns:
            URL: Newly created URL ORM object.

        Raises:
            RuntimeError: If creation fails due to DB error.
        """
        return create(self._session_factory, original_url, expired_at)

    def delete_by_code(self, code: str) -> Optional[URL]:
        """Delete URL by short code.

        Args:
            code (str): Short code to delete.

        Returns:
            Optional[URL]: Deleted URL object.

        Raises:
            NotFoundError: If code does not exist.
        """
        return delete_by_short_code(self._session_factory, code)

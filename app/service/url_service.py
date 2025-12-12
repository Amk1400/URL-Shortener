from typing import Any, Callable, List, Optional
from fastapi import HTTPException, status
from pydantic import AnyHttpUrl

from app.repository.base import UrlRepository
from app.models.orm import URL
from app.repository.getter import NotFoundError


def _validate_required(value: Any, field: str) -> None:
    """Validate that a required value is present.

    Args:
        value (Any): Value to validate.
        field (str): Field name for error messages.

    Returns:
        None

    Raises:
        ValueError: If value is falsy.
    """
    if not value:
        raise ValueError(f"{field} is required")


def _handle_repo_call(func: Callable[[], Any], action: str) -> Any:
    """Wrap repository calls and convert exceptions.

    Args:
        func (Callable[[], Any]): Repository callable to execute.
        action (str): Description of the action for error messages.

    Returns:
        Any: Result from repository call.

    Raises:
        RuntimeError: If underlying call raises.
    """
    try:
        return func()
    except Exception as e:
        raise RuntimeError(f"Error {action}: {repr(e)}")


class UrlService:
    """Service layer for URL business logic.

    Attributes:
        repository (UrlRepository): Repository instance.
        ttl_minutes (int): Default time-to-live in minutes.
    """

    def __init__(self, repository: UrlRepository, ttl_minutes: int = 1440) -> None:
        """Initialize UrlService.

        Args:
            repository (UrlRepository): Repository instance.
            ttl_minutes (int): TTL in minutes.

        Returns:
            None

        Raises:
            None
        """
        self.repository = repository
        self.ttl_minutes = ttl_minutes

    def create_short_url(self, original_url: AnyHttpUrl) -> URL:
        """Create a shortened URL entry.

        Args:
            original_url (AnyHttpUrl): Original URL to shorten.

        Returns:
            URL: Created URL model.

        Raises:
            ValueError: If original_url is missing.
            RuntimeError: If repository fails to create URL.
        """
        _validate_required(original_url, "original_url")
        url_obj = _handle_repo_call(
            lambda: self.repository.create(original_url=original_url),
            "creating short URL",
        )
        if url_obj is None:
            raise RuntimeError("Failed to create URL in repository")
        return url_obj

    def delete_short_url(self, code: str) -> URL:
        """Delete a short URL by code.

        Args:
            code (str): Short code to delete.

        Returns:
            URL: Deleted URL object.

        Raises:
            HTTPException: 404 if not found, 500 on other errors.
        """
        _validate_required(code, "code")
        try:
            url_obj = self.repository.delete_by_code(code)
            return url_obj
        except NotFoundError as nf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(nf))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting short URL: {repr(e)}",
            )

    def get_all_urls(self) -> List[URL]:
        """Fetch all URLs.

        Args:
            None

        Returns:
            List[URL]: List of URL objects.

        Raises:
            RuntimeError: If repository call fails.
        """
        return _handle_repo_call(lambda: self.repository.get_all(), "fetching URLs")

    def get_original_url(self, code: str) -> URL:
        """Retrieve the original URL for a short code.

        Args:
            code (str): Short code to lookup.

        Returns:
            URL: URL object.

        Raises:
            HTTPException: 404 if not found, 500 on other errors.
        """
        _validate_required(code, "code")
        try:
            url_obj = self.repository.get_by_code(code)
            return url_obj
        except NotFoundError as nf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(nf))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching URL: {repr(e)}",
            )

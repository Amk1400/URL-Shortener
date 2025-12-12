from typing import Optional
from fastapi import HTTPException, status
from pydantic import AnyHttpUrl
from app.repository.base import UrlRepository
from app.models.orm import URL


class UrlService:
    """Business logic for URL shortener.

    Attributes:
        repository (UrlRepository): Repository for persistence.
        ttl_minutes (int): Time-to-live in minutes for created links.
    """

    def __init__(self, repository: UrlRepository, ttl_minutes: int = 1440) -> None:
        self.repository = repository
        self.ttl_minutes = ttl_minutes
        self._ttl = ttl_minutes


    def create_short_url(self, original_url: AnyHttpUrl) -> URL:
        """Create a shortened URL and persist it.

        Args:
            original_url (AnyHttpUrl): Original URL to shorten.

        Returns:
            URL: Created URL ORM object.

        Raises:
            ValueError: If original_url is invalid.
            RuntimeError: If repository fails to create URL.
        """
        if not original_url:
            raise ValueError("original_url is required")

        try:
            url_obj: Optional[URL] = self.repository.create(original_url=original_url)
            if url_obj is None:
                raise RuntimeError("Failed to create URL in repository")
            return url_obj
        except Exception as e:
            raise RuntimeError(f"Error creating short URL: {repr(e)}")

    def delete_short_url(self, code: str) -> URL:
        """Delete a shortened URL by code and return the deleted record.

        Args:
            code (str): Short code to delete.

        Returns:
            URL: The deleted URL ORM object.

        Raises:
            HTTPException: 404 if not found, 500 on error.
        """
        if not code:
            raise ValueError("code is required")

        try:
            url_obj: Optional[URL] = self.repository.delete_by_code(code)
            if url_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="URL not found"
                )
            return url_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting short URL: {repr(e)}"
            )
        
    def get_all_urls(self):
        """Return all shortened URLs."""
        try:
            urls = self.repository.get_all()
            return urls
        except Exception as exc:
            raise RuntimeError(f"Error fetching URLs: {repr(exc)}")
    def get_original_url(self, code: str) -> URL:
        """Return URL object for given short code."""
        if not code:
            raise ValueError("code is required")

        try:
            url_obj = self.repository.get_by_code(code)
            if url_obj is None:
                raise RuntimeError("URL not found")
            return url_obj
        except Exception as e:
            raise RuntimeError(f"Error fetching URL: {repr(e)}")
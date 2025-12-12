from typing import Any
from fastapi import HTTPException, status
from pydantic import AnyHttpUrl

from app.repository.base import UrlRepository
from app.models.orm import URL
from app.repository.getter import NotFoundError

def _validate_required(value: Any, field: str):
    if not value:
        raise ValueError(f"{field} is required")

def _handle_repo_call(func, action: str):
    try:
        return func()
    except Exception as e:
        raise RuntimeError(f"Error {action}: {repr(e)}")

class UrlService:
    def __init__(self, repository: UrlRepository, ttl_minutes: int = 1440) -> None:
        self.repository = repository
        self.ttl_minutes = ttl_minutes

    def create_short_url(self, original_url: AnyHttpUrl) -> URL:
        _validate_required(original_url, "original_url")
        url_obj = _handle_repo_call(
            lambda: self.repository.create(original_url=original_url),
            "creating short URL"
        )
        if url_obj is None:
            raise RuntimeError("Failed to create URL in repository")
        return url_obj

    def delete_short_url(self, code: str) -> URL:
        _validate_required(code, "code")
        try:
            url_obj = self.repository.delete_by_code(code)
            return url_obj
        except NotFoundError as nf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(nf))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error deleting short URL: {repr(e)}")

    def get_all_urls(self):
        return _handle_repo_call(lambda: self.repository.get_all(), "fetching URLs")

    def get_original_url(self, code: str) -> URL:
        _validate_required(code, "code")
        try:
            url_obj = self.repository.get_by_code(code)
            return url_obj
        except NotFoundError as nf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(nf))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching URL: {repr(e)}")

from typing import Optional, Callable, TypeVar
from fastapi import HTTPException, status
from pydantic import AnyHttpUrl
from app.repository.base import UrlRepository
from app.models.orm import URL


T = TypeVar("T")


def _validate_required(value: str | AnyHttpUrl, field: str):
    if not value:
        raise ValueError(f"{field} is required")


def _handle_repo_call(func: Callable[[], T], action: str) -> T:
    try:
        return func()
    except Exception as e:
        raise RuntimeError(f"Error {action}: {repr(e)}")


def _require_found(obj: Optional[T], not_found_msg: str) -> T:
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=not_found_msg
        )
    return obj


class UrlService:
    def __init__(self, repository: UrlRepository, ttl_minutes: int = 1440) -> None:
        self.repository = repository
        self.ttl_minutes = ttl_minutes
        self._ttl = ttl_minutes

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
            return _require_found(url_obj, "URL not found")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting short URL: {repr(e)}"
            )

    def get_all_urls(self):
        return _handle_repo_call(
            lambda: self.repository.get_all(),
            "fetching URLs"
        )

    def get_original_url(self, code: str) -> URL:
        _validate_required(code, "code")

        url_obj = _handle_repo_call(
            lambda: self.repository.get_by_code(code),
            "fetching URL"
        )

        if url_obj is None:
            raise RuntimeError("URL not found")

        return url_obj

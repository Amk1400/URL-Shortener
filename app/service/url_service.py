from app.models.orm import URL
from app.repository.base import UrlRepository


class UrlService:

    def __init__(self, repository: UrlRepository, ttl_minutes: int) -> None:
        self._repo = repository
        self._ttl = ttl_minutes

    def get_original_url(self, code: str) -> URL:
        """Return URL object for given short code."""
        if not code:
            raise ValueError("code is required")

        try:
            url_obj = self._repo.get_by_code(code)
            if url_obj is None:
                raise RuntimeError("URL not found")
            return url_obj
        except Exception as e:
            raise RuntimeError(f"Error fetching URL: {repr(e)}")

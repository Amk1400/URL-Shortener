from app.repository.base import UrlRepository


class UrlService:

    def __init__(self, repository: UrlRepository, ttl_minutes: int) -> None:
        self._repo = repository
        self._ttl = ttl_minutes

    def get_all_urls(self):
        """Return all shortened URLs."""
        try:
            urls = self._repo.get_all()
            return urls
        except Exception as exc:
            raise RuntimeError(f"Error fetching URLs: {repr(exc)}")
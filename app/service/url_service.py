from app.repository.base import UrlRepository


class UrlService:

    def __init__(self, repository: UrlRepository, ttl_minutes: int) -> None:
        self._repo = repository
        self._ttl = ttl_minutes
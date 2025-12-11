from fastapi import FastAPI

from app.api.routers.poster import create_poster_router
from app.service.url_service import UrlService


class Router:
    """Aggregates all API routes into a single FastAPI app."""

    def __init__(self, service: UrlService):
        self._app = FastAPI(title="URL Shortener API", version="0.1.0")
        self._service = service
        self._register_routes()

    @property
    def app(self) -> FastAPI:
        return self._app

    def _register_routes(self) -> None:
        """Include all route modules with injected service."""
        poster_router = create_poster_router(self._service)
        self._app.include_router(poster_router)
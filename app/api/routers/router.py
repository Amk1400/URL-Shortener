from fastapi import FastAPI

from app.api.routers.getter import create_getter_router
from app.api.routers.poster import create_poster_router
from app.api.routers.deleter import create_deleter_router
from app.service.url_service import UrlService


class Router:
    """Router wrapper registering API routes.

    Attributes:
        _app (FastAPI): FastAPI application instance.
        _service (UrlService): Service instance.
    """

    def __init__(self, service: UrlService):
        """Initialize Router.

        Args:
            service (UrlService): Service instance.

        Returns:
            None

        Raises:
            None
        """
        self._app = FastAPI(title="URL Shortener API", version="0.1.0")
        self._service = service
        self._register()

    @property
    def app(self) -> FastAPI:
        """Return the FastAPI app.

        Args:
            None

        Returns:
            FastAPI: The application instance.

        Raises:
            None
        """
        return self._app

    def _register(self) -> None:
        """Register routers on the FastAPI app.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self._app.include_router(create_getter_router(self._service))
        self._app.include_router(create_poster_router(self._service))
        self._app.include_router(create_deleter_router(self._service))

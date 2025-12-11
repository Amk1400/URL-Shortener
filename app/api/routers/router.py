from fastapi import FastAPI

from app.api.routers.getter import create_getter_router
from app.service.url_service import UrlService


class Router:

    def __init__(self, service: UrlService) -> None:
        self._service = service
        self._app = FastAPI(title="URL Shortener API", version="0.1.0")
        self._register_routes()

    @property
    def app(self) -> FastAPI:
        return self._app

    def _register_routes(self) -> None:
        """
        TODO get all/ get by id/ delete/ post
        :return:
        """
        getter_router = create_getter_router(self._service)
        self._app.include_router(getter_router)

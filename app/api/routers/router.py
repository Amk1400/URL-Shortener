from fastapi import FastAPI

from app.api.routers.getter import create_getter_router
from app.api.routers.poster import create_poster_router
from app.api.routers.deleter import create_deleter_router
from app.service.url_service import UrlService

class Router:
    def __init__(self, service: UrlService):
        self._app = FastAPI(title="URL Shortener API", version="0.1.0")
        self._service = service
        self._register()

    @property
    def app(self):
        return self._app

    def _register(self):
        self._app.include_router(create_getter_router(self._service))
        self._app.include_router(create_poster_router(self._service))
        self._app.include_router(create_deleter_router(self._service))
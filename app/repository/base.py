from app.repository.getter import get_all as getter_all
from app.repository.getter import get_by_code

class UrlRepository:

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def get_all(self):
        return getter_all(self._session_factory)
    def get_by_code(self, code: str):
        return get_by_code(self._session_factory, code)



class UrlRepository:

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
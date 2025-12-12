import uvicorn

from app.core.config import AppConfig
from app.repository.base import UrlRepository
from app.db.session import DatabaseSession
from app.service.url_service import UrlService
from app.api.routers.router import Router

def build_router() -> Router:
    """Wire dependencies and return Router instance."""
    config = AppConfig.load()
    db = DatabaseSession(database_url=config.database_url)
    db.connect()
    repo = UrlRepository(session_factory=db.get_session)
    service = UrlService(repository=repo, ttl_minutes=config.ttl_minutes)
    router = Router(service=service)
    return router


def main() -> None:
    """Start the API server."""
    router = build_router()
    #scheduler.run()
    uvicorn.run(router.app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
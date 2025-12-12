import uvicorn

from app.core.config import AppConfig
from app.repository.base import UrlRepository
from app.db.session import DatabaseSession
from app.service.url_service import UrlService
from app.api.routers.router import Router
from app.service.scheduler.url_remove import start_background_scheduler

def build_router() -> tuple[Router, DatabaseSession, AppConfig]:
    config = AppConfig.load()
    db = DatabaseSession(database_url=config.database_url)
    db.connect()
    repo = UrlRepository(session_factory=db.get_session)
    service = UrlService(repository=repo, ttl_minutes=config.ttl_minutes)
    router = Router(service=service)
    return router, db, config

def main() -> None:
    router, db, config = build_router()
    start_background_scheduler(db.get_session, config.ttl_minutes, every_minutes=10)
    uvicorn.run(router.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

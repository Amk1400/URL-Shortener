from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.orm import URL

def get_all(session_factory) -> list[URL]:
    """Return all URL records."""
    session: Session = session_factory()
    try:
        urls = session.query(URL).all()
        return urls
    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f"Database error during GET /urls: {repr(exc)}")
    finally:
        session.close()
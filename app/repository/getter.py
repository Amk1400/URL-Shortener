from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.orm import URL


def get_by_code(session_factory, code: str) -> URL | None:
    """Fetch URL object by its short_code."""
    session: Session = session_factory()
    try:
        return session.query(URL).filter(URL.short_code == code).first()
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while fetching code: {repr(exc)}")
    finally:
        session.close()

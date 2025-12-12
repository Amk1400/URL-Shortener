from sqlalchemy.orm import Session

from app.models.orm import URL

def get_by_short_code(session_factory, code: str) -> URL | None:
    """Retrieve a URL record by short code."""
    session: Session = session_factory()
    try:
        return session.query(URL).filter_by(short_code=code).first()
    finally:
        session.close()
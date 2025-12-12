from typing import List, Optional, Callable, cast
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import SQLAlchemyError

from app.core.exception import NotFoundError
from app.models.orm import URL


def get_all(session_factory: Callable[[], Session]) -> Optional[List[URL]]:
    """Return all URL records.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.

    Returns:
        Optional[List[URL]]: List of URLs or None.

    Raises:
        RuntimeError: On database errors.
    """
    session: Session = session_factory()
    try:
        query: Query[URL] = cast(Query[URL], session.query(URL))
        result: List[URL] = query.all()
        return result
    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f"Database error during GET /urls: {repr(exc)}")
    finally:
        session.close()


def get_by_code(session_factory: Callable[[], Session], code: str) -> Optional[URL]:
    """Fetch a URL by its short code.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.
        code (str): Short code to lookup.

    Returns:
        Optional[URL]: URL object if found.

    Raises:
        NotFoundError: If no matching URL is found.
        RuntimeError: On database errors.
    """
    session: Session = session_factory()
    try:
        query: Query[URL] = cast(Query[URL], session.query(URL))

        condition: ColumnElement[bool] = cast(ColumnElement[bool], URL.short_code == code)

        result: Optional[URL] = query.filter(condition).first()
        if not result:
            raise NotFoundError(f"URL with code {code} not found")

        return result

    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while fetching code: {repr(exc)}")

    finally:
        session.close()

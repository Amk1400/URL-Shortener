from typing import List, Optional, cast

from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import SQLAlchemyError
from app.models.orm import URL


def get_all(session_factory) -> List[URL] | None:
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


def get_by_code(session_factory, code: str) -> Optional[URL]:
    session: Session = session_factory()
    try:
        query: Query[URL] = cast(Query[URL], session.query(URL))

        condition: ColumnElement[bool] = cast(ColumnElement[bool], URL.short_code == code)

        result: Optional[URL] = query.filter(condition).first()
        return result

    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database error while fetching code: {repr(exc)}")

    finally:
        session.close()
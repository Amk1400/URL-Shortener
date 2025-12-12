from typing import Callable
from pydantic import AnyHttpUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.orm import URL
from app.utils.code_generator import CodeGenerator


def create(session_factory: Callable[[], Session], original_url: AnyHttpUrl, expired_at=None) -> URL:
    """Create a new URL row and generate its short code.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.
        original_url (AnyHttpUrl): Original URL to shorten.
        expired_at (datetime|None): Optional expiration datetime.

    Returns:
        URL: The created URL ORM object.

    Raises:
        RuntimeError: On integrity or database errors.
    """
    session: Session = session_factory()
    try:
        url_obj = URL(original_url=str(original_url), expired_at=expired_at, short_code="null")
        session.add(url_obj)
        session.commit()
        session.refresh(url_obj)

        url_obj.short_code = CodeGenerator.generate(url_obj.id)
        session.commit()
        session.refresh(url_obj)
        return url_obj

    except IntegrityError as ie:
        session.rollback()
        raise RuntimeError(f"Integrity error while creating URL: {repr(ie)}")
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error while creating URL: {repr(e)}")
    finally:
        session.close()

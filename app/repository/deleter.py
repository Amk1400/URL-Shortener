from typing import Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.exception import NotFoundError
from app.models.orm import URL
from app.repository.getter import get_by_code
from app.utils.code_generator import CodeGenerator


def delete_by_short_code(session_factory: Callable[[], Session], code: str) -> URL:
    """Delete URL record identified by short code.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.
        code (str): Short code to delete.

    Returns:
        URL: The deleted URL object.

    Raises:
        NotFoundError: If the URL is not found.
        RuntimeError: On database errors.
    """
    session: Session = session_factory()
    try:
        try:
            url_obj = get_by_code(session_factory, code)
        except NotFoundError:
            raise

        decoded_id = CodeGenerator.decode(code)
        target: Optional[URL] = session.query(URL).filter_by(id=decoded_id).first()

        session.delete(target)
        session.commit()
        return url_obj

    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f"Database error while deleting URL: {repr(exc)}")
    finally:
        session.close()

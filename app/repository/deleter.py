from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.orm import URL
from app.repository.getter import get_by_code
from app.utils.code_generator import CodeGenerator

def delete_by_short_code(session_factory, code: str) -> URL | None:
    """Delete a URL record by short code if it exists, using get_by_code and decode for ID.

    Returns:
        URL: The deleted URL object if found and deleted, None if not found.
    """
    url_obj = get_by_code(session_factory, code)
    session: Session = session_factory()
    try:
        attached_obj = session.query(URL).filter_by(id=CodeGenerator.decode(code)).first()
        if attached_obj:
            session.delete(attached_obj)
            session.commit()
            return url_obj
        else:
            return None
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error while deleting URL: {repr(e)}")
    finally:
        session.close()
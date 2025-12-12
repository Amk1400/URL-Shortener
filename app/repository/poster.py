from pydantic import AnyHttpUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.orm import URL
from app.utils.code_generator import CodeGenerator

def create(session_factory, original_url: AnyHttpUrl, expired_at=None) -> URL:
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
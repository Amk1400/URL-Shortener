from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class URL(Base):
    """ORM model for shortened URLs.

    Attributes:
        id (int): Primary key.
        original_url (str): Original long URL.
        short_code (str): Generated short code.
        created_at (datetime): Creation timestamp.
        expired_at (datetime | None): Expiration timestamp.
    """
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    expired_at = Column(DateTime, nullable=True)

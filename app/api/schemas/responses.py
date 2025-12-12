from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UrlResponse(BaseModel):
    """Output schema for shortened URL."""

    id: int = Field(..., description="Unique identifier")
    original_url: str = Field(..., description="Original long URL")
    short_code: str = Field(..., description="Generated short code")
    created_at: datetime = Field(..., description="Creation timestamp")
    expired_at: Optional[datetime] = Field(None, description="Expiration timestamp")


class ApiSuccess(BaseModel):
    """Success wrapper."""
    status: str = "sucess"
    data: list[UrlResponse] | UrlResponse


class ApiFailure(BaseModel):
    """Failure wrapper."""
    status: str = "failure"
    message: str
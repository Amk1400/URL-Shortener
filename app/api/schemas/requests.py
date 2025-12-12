from pydantic import BaseModel, AnyHttpUrl, Field


class UrlCreate(BaseModel):
    """Request schema for creating a shortened URL.

    Attributes:
        original_url (AnyHttpUrl): Original long URL provided by the user.
    """
    original_url: AnyHttpUrl = Field(..., description="Original long URL to shorten")

from typing import Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.api.schemas.responses import ApiSuccess, ApiFailure, UrlResponse


def wrap_success_url(url_obj: Any) -> UrlResponse:
    """Convert ORM URL to UrlResponse schema.

    Args:
        url_obj (Any): ORM URL object.

    Returns:
        UrlResponse: API response schema.

    Raises:
        None
    """
    return UrlResponse(
        id=url_obj.id,
        original_url=url_obj.original_url,
        short_code=url_obj.short_code,
        created_at=url_obj.created_at,
        expired_at=url_obj.expired_at,
    )


def res_success(data: Any, code: int = status.HTTP_200_OK) -> ApiSuccess:
    """Return success payload.

    Args:
        data (Any): Payload data.
        code (int): HTTP status code.

    Returns:
        ApiSuccess: Success response body.

    Raises:
        HTTPException: Used to propagate status code.
    """
    raise HTTPException(
        status_code=code,
        detail=jsonable_encoder(
            ApiSuccess(
                status="success",
                data=data,
            )
        ),
    )


def res_400(msg: str) -> None:
    """Raise 400 bad request error.

    Args:
        msg (str): Error message.

    Returns:
        None

    Raises:
        HTTPException: 400 error.
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=jsonable_encoder(
            ApiFailure(
                status="failure",
                message=msg,
            )
        ),
    )


def res_404(msg: str) -> None:
    """Raise 404 not found error.

    Args:
        msg (str): Error message.

    Returns:
        None

    Raises:
        HTTPException: 404 error.
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=jsonable_encoder(
            ApiFailure(
                status="failure",
                message=msg,
            )
        ),
    )


def res_500(msg: str) -> None:
    """Raise 500 internal server error.

    Args:
        msg (str): Error message.

    Returns:
        None

    Raises:
        HTTPException: 500 error.
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=jsonable_encoder(
            ApiFailure(
                status="failure",
                message=msg,
            )
        ),
    )

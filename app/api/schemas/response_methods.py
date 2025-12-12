from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.api.schemas.responses import ApiSuccess, ApiFailure, UrlResponse


def wrap_success_url(url_obj):
    """Convert ORM URL to UrlResponse schema.

    Args:
        url_obj: ORM URL object.

    Returns:
        UrlResponse: API schema object.

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


def res_success(data, code=status.HTTP_200_OK):
    """Return a standardized success JSONResponse.

    Args:
        data: Payload data.
        code: HTTP status code.

    Returns:
        JSONResponse: Success response.

    Raises:
        None
    """
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(ApiSuccess(status="success", data=data)),
    )


def res_404(msg="URL not found"):
    """Return a standardized 404 JSONResponse.

    Args:
        msg (str): Message text.

    Returns:
        JSONResponse: 404 response.

    Raises:
        None
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(ApiFailure(status="failure", message=msg)),
    )


def res_400(msg):
    """Return a standardized 400 JSONResponse.

    Args:
        msg (str): Message text.

    Returns:
        JSONResponse: 400 response.

    Raises:
        None
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(ApiFailure(status="failure", message=msg)),
    )


def res_500(msg):
    """Return a standardized 500 JSONResponse.

    Args:
        msg (str): Message text.

    Returns:
        JSONResponse: 500 response with internal error message.

    Raises:
        None
    """
    return JSONResponse(
        content=jsonable_encoder(ApiFailure(status="failure", message=f"Internal server error: {msg}"))
    )

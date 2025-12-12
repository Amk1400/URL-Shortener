from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.api.schemas.responses import ApiSuccess, ApiFailure, UrlResponse


def wrap_success_url(url_obj):
    return UrlResponse(
        id=url_obj.id,
        original_url=url_obj.original_url,
        short_code=url_obj.short_code,
        created_at=url_obj.created_at,
        expired_at=url_obj.expired_at,
    )


def res_success(data, code=status.HTTP_200_OK):
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(ApiSuccess(status="success", data=data))
    )


def res_404(msg="URL not found"):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(ApiFailure(status="failure", message=msg))
    )


def res_400(msg):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(ApiFailure(status="failure", message=msg))
    )


def res_500(msg):
    return JSONResponse(
        content=jsonable_encoder(ApiFailure(status="failure", message=f"Internal server error: {msg}"))
    )

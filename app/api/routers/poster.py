from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

from app.service.url_service import UrlService
from app.api.schemas.requests import UrlCreate
from app.api.schemas.responses import UrlResponse, ApiSuccess, ApiFailure


def create_poster_router(service: UrlService) -> APIRouter:
    """Create and return an APIRouter for URL shortening.

    Args:
        service (UrlService): Instance of UrlService for URL operations.

    Returns:
        APIRouter: Configured FastAPI router with /urls POST endpoint.
    """
    router = APIRouter()

    @router.post(
        "/urls",
        response_model=ApiSuccess | ApiFailure,
        responses={
            201: {"model": ApiSuccess,"description": "Short URL successfully created"},
            422: {"model": ApiFailure, "description": "Validation error"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def create_short_url(request: UrlCreate):
        """Endpoint to create a shortened URL from an original URL.

        Args:
            request (UrlCreate): Request body containing original_url field.

        Returns:
            ApiSuccess: On success, returns status="success" and UrlResponse.
            ApiFailure: On failure, returns status="failure" and message.
        """
        try:
            url_obj = service.create_short_url(original_url=request.original_url)
            return _return_success(url_obj)
        except Exception as exc:
            return _return500(exc)

    def _return500(exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                ApiFailure(status="failure", message=f"Internal server error: {str(exc)}")
            ),
        )

    def _return_success(url_obj):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(
                ApiSuccess(status="success", data=_wrap_success(url_obj))
            ),
        )

    return router


def _wrap_success(url_obj: Any) -> UrlResponse:
    """Wrap a URL object into UrlResponse for ApiSuccess.

    Args:
        url_obj (Any): URL object returned from UrlService.

    Returns:
        UrlResponse: URL details for success response.
    """
    return UrlResponse(
        id=url_obj.id,
        original_url=url_obj.original_url,
        short_code=url_obj.short_code,
        created_at=url_obj.created_at,
        expired_at=url_obj.expired_at,
    )

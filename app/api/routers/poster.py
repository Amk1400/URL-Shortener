from fastapi import APIRouter, status, HTTPException
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
        response_model=ApiSuccess,
        status_code=status.HTTP_201_CREATED,
        responses={
            400: {"model": ApiFailure, "description": "Invalid input"},
            422: {"model": ApiFailure, "description": "Validation error"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def create_short_url(request: UrlCreate) -> ApiSuccess:
        """Endpoint to create a shortened URL from an original URL.

        Args:
            request (UrlCreate): Request body containing original_url field.

        Returns:
            ApiSuccess: On successful creation, returns status="success" and the UrlResponse.

        Raises:
            HTTPException: For invalid input (400) or internal server error (500).
        """
        try:
            url_obj = service.create_short_url(original_url=request.original_url)
            return _wrap_success(url_obj)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(exc)}"
            )

    return router


def _wrap_success(url_obj: Any) -> ApiSuccess:
    """Wrap a URL object into ApiSuccess response.

    Args:
        url_obj (Any): URL object returned from UrlService.

    Returns:
        ApiSuccess: Contains status="success" and UrlResponse with URL details.
    """
    response_data = UrlResponse(
        id=url_obj.id,
        original_url=url_obj.original_url,
        short_code=url_obj.short_code,
        created_at=url_obj.created_at,
        expired_at=url_obj.expired_at,
    )
    return ApiSuccess(status="success", data=response_data)

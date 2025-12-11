from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

from app.service.url_service import UrlService
from app.api.schemas.responses import UrlResponse, ApiSuccess, ApiFailure


def create_deleter_router(service: UrlService) -> APIRouter:
    """Create APIRouter for deleting shortened URLs.

    Args:
        service (UrlService): Service handling URL operations.

    Returns:
        APIRouter: Configured router with DELETE /urls/{code} endpoint.
    """
    router = APIRouter()

    @router.delete(
        "/urls/{code}",
        response_model=ApiSuccess | ApiFailure,
        responses={
            404: {"model": ApiFailure, "description": "URL not found"},
            400: {"model": ApiFailure, "description": "Invalid request"},
            422: {"model": ApiFailure, "description": "Validation Error"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def delete_short_url(code: str) -> JSONResponse:
        """Delete a shortened URL by code.

        Args:
            code (str): Short code of the URL to delete.

        Returns:
            JSONResponse: ApiSuccess on success, ApiFailure on failure.
        """
        try:
            url_obj = service.delete_short_url(code)
            return _return_success(url_obj)
        except ValueError as exc:
            return _return_400(str(exc))
        except Exception as exc:
            msg = str(exc)
            if "404" in msg.lower() or "not found" in msg.lower():
                return _return_404()
            return _return_500(msg)

    def _return_success(url_obj: Any) -> JSONResponse:
        """Return a success response with the deleted URL."""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(ApiSuccess(status="success", data=_wrap_url_response(url_obj)))
        )

    def _return_404() -> JSONResponse:
        """Return a 404 not found failure response."""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(ApiFailure(status="failure", message="URL not found"))
        )

    def _return_400(message: str) -> JSONResponse:
        """Return a 400 bad request failure response."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(ApiFailure(status="failure", message=message))
        )

    def _return_500(message: str) -> JSONResponse:
        """Return a 500 internal server error failure response."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(ApiFailure(status="failure", message=f"Internal server error: {message}"))
        )

    def _wrap_url_response(url_obj: Any) -> UrlResponse:
        """Convert URL object to UrlResponse schema."""
        return UrlResponse(
            id=url_obj.id,
            original_url=url_obj.original_url,
            short_code=url_obj.short_code,
            created_at=url_obj.created_at,
            expired_at=url_obj.expired_at,
        )

    return router

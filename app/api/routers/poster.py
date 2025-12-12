from fastapi import APIRouter, status, HTTPException

from app.service.url_service import UrlService
from app.api.schemas.requests import UrlCreate
from app.api.schemas.responses import ApiSuccess, ApiFailure
from app.api.schemas.response_methods import wrap_success_url, res_success, res_500


def create_poster_router(service: UrlService) -> APIRouter:
    """Create poster router for URL creation endpoints.

    Args:
        service (UrlService): Service instance.

    Returns:
        APIRouter: Configured APIRouter.

    Raises:
        None
    """
    router = APIRouter()

    @router.post(
        "/urls",
        response_model=ApiSuccess | ApiFailure,
        responses={
            201: {"model": ApiSuccess, "description": "Short URL successfully created"},
            422: {"model": ApiFailure, "description": "Validation error"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def create_short_url(request: UrlCreate):
        """Endpoint to create a short URL.

        Args:
            request (UrlCreate): Request body with original_url.

        Returns:
            JSONResponse: Created short URL response.

        Raises:
            None
        """
        try:
            obj = service.create_short_url(original_url=request.original_url)
            return res_success(wrap_success_url(obj), status.HTTP_201_CREATED)
        except HTTPException:
            raise
        except Exception as exc:
            return res_500(str(exc))

    return router

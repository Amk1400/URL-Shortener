from fastapi import APIRouter, HTTPException

from app.service.url_service import UrlService
from app.api.schemas.responses import ApiSuccess, ApiFailure
from app.api.schemas.response_methods import wrap_success_url, res_success, res_404, res_400, res_500
from app.repository.getter import NotFoundError


def create_deleter_router(service: UrlService) -> APIRouter:
    """Create delete router for URL deletion endpoints.

    Args:
        service (UrlService): Service instance.

    Returns:
        APIRouter: Configured APIRouter.

    Raises:
        None
    """
    router = APIRouter()

    @router.delete(
        "/urls/{code}",
        response_model=ApiSuccess | ApiFailure,
        responses={
            200: {"model": ApiSuccess, "description": "URL successfully deleted"},
            404: {"model": ApiFailure, "description": "URL not found"},
            400: {"model": ApiFailure, "description": "Invalid request"},
            422: {"model": ApiFailure, "description": "Validation Error"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def delete_short_url(code: str):
        """Endpoint to delete a short URL by code.

        Args:
            code (str): Short code to delete.

        Returns:
            JSONResponse: Success or failure response.

        Raises:
            None
        """
        try:
            url_obj = service.delete_short_url(code)
            return res_success(wrap_success_url(url_obj))
        except HTTPException:
            raise
        except ValueError as ve:
            return res_400(str(ve))
        except NotFoundError as nf:
            return res_404(str(nf))
        except Exception as exc:
            return res_500(str(exc))

    return router

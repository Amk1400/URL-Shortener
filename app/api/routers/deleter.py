from fastapi import APIRouter

from app.service.url_service import UrlService
from app.api.schemas.responses import ApiSuccess, ApiFailure
from app.api.schemas.response_methods import wrap_success_url, res_success
from app.api.schemas.response_methods import res_400, res_404, res_500



def create_deleter_router(service: UrlService) -> APIRouter:
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
        try:
            url_obj = service.delete_short_url(code)
            return res_success(wrap_success_url(url_obj))
        except ValueError as exc:
            return res_400(str(exc))
        except Exception as exc:
            msg = str(exc)
            if "404" in msg.lower() or "not found" in msg.lower():
                return res_404()
            return res_500(msg)

    return router

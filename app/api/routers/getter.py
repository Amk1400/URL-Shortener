from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.service.url_service import UrlService
from app.api.schemas.responses import ApiSuccess, ApiFailure
from app.api.schemas.response_methods import wrap_success_url, res_success, res_404, res_500



def create_getter_router(service: UrlService) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/urls",
        response_model=ApiSuccess | ApiFailure,
        responses={
            200: {"model": ApiSuccess, "description": "List of all URLs"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def get_all_urls():
        try:
            urls = service.get_all_urls()
            data = [wrap_success_url(u) for u in urls]
            return res_success(data)
        except Exception as exc:
            return res_500(str(exc))

    @router.get(
        "/u/{code}",
        responses={
            302: {"description": "Redirect to original URL"},
            404: {"model": ApiFailure, "description": "URL not found"},
            500: {"model": ApiFailure, "description": "Internal server error"},
        },
    )
    def redirect_to_original(code: str):
        try:
            url_obj = service.get_original_url(code)
            return RedirectResponse(url=url_obj.original_url, status_code=302)
        except Exception as exc:
            msg = str(exc)
            if "URL not found" in msg:
                return res_404("URL not found")
            return res_500(msg)

    return router

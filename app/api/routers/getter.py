from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from app.service.url_service import UrlService
from app.api.schemas.responses import ApiFailure


def create_getter_router(service: UrlService) -> APIRouter:
    router = APIRouter()

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
            message = str(exc)

            if "URL not found" in message:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=jsonable_encoder(ApiFailure(
                        status="failure",
                        message="URL not found"
                    )),
                )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(ApiFailure(
                    status="failure",
                    message=f"Internal server error: {message}"
                )),
            )

    return router

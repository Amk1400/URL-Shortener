from fastapi import APIRouter, status

from app.service.url_service import UrlService
from app.api.schemas.responses import ApiSuccess, ApiFailure, UrlResponse

from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

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

            data = [UrlResponse(
                id=u.id,
                original_url=u.original_url,
                short_code=u.short_code,
                created_at=u.created_at,
                expired_at=u.expired_at
            ) for u in urls]
                
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(ApiSuccess(status="success", data=data))
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(
                    ApiFailure(status="failure", message=f"Internal server error: {str(exc)}")
                ),
            )

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

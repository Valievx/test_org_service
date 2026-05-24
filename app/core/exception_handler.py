from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions import AppError


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message}
    )

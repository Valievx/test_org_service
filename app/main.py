from contextlib import asynccontextmanager

from fastapi import FastAPI

from domain.exceptions import AppError
from core.settings import settings
from core.exception_handler import app_error_handler
from db.session import db_helper
from api import department


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        debug=settings.DEBUG,
        docs_url="/api/docs",
        title="Org Manager",
        lifespan=lifespan,
    )

    app.include_router(department.router)

    app.add_exception_handler(AppError, app_error_handler)
    return app

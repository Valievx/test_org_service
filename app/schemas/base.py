from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None


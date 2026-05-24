from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class EmployeeCreateSchema(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None = None

    @field_validator("full_name", "position")
    @classmethod
    def validate_strings(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


class EmployeeResponseSchema(BaseModel):
    id: str
    department_id: str
    full_name: str
    position: str
    hired_at: date | None
    created_at: datetime

    model_config = {"from_attributes": True}

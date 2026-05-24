from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from .employee import EmployeeResponseSchema


class DepartmentCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value


class DepartmentResponseSchema(BaseModel):
    id: str
    name: str
    parent_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DepartmentDetailsQuerySchema(BaseModel):
    depth: int = Field(default=1, ge=1, le=5)
    include_employees: bool = True


class DepartmentTreeSchema(BaseModel):
    id: str
    name: str
    parent_id: str | None
    created_at: datetime

    children: list["DepartmentTreeSchema"] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_tree(
        cls,
        department,
        current_depth: int,
        max_depth: int,
    ):

        if current_depth > max_depth:
            return None

        children = []

        for child in department.children:
            child_schema = cls.from_orm_tree(
                child,
                current_depth=current_depth + 1,
                max_depth=max_depth,
            )

            if child_schema:
                children.append(child_schema)

        return cls(
            id=department.id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=department.created_at,
            children=children,
        )


class DepartmentDetailsSchema(BaseModel):
    department: DepartmentTreeSchema

    employees: list[EmployeeResponseSchema] = []


class DepartmentUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    parent_id: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value


class DeleteDepartmentQuerySchema(BaseModel):
    mode: Literal["cascade", "reassign"]

    reassign_to_department_id: str | None = None

    @model_validator(mode="after")
    def validate_reassign(self):

        if self.mode == "reassign" and self.reassign_to_department_id is None:
            raise ValueError("Reassign to department_id is required")

        return self

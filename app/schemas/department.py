from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field

from .employee import EmployeeResponseSchema


class DepartmentCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: str | None = None


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

    employees: list[EmployeeResponseSchema] = Field(default_factory=list)
    children: list["DepartmentTreeSchema"] = Field(default_factory=list)

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_tree(
        cls,
        department,
        current_depth: int,
        max_depth: int,
        include_employees: bool = True,
    ):
        if current_depth > max_depth:
            return None

        children = list(department.children or [])

        employees = []
        if include_employees:
            employees = sorted(
                list(department.employees or []),
                key=lambda x: x.full_name.lower(),
            )

            employees = [
                EmployeeResponseSchema.model_validate(emp)
                for emp in employees
            ]

        child_schemas = []
        for child in children:
            child_schema = cls.from_orm_tree(
                child,
                current_depth=current_depth + 1,
                max_depth=max_depth,
                include_employees=include_employees,
            )
            if child_schema:
                child_schemas.append(child_schema)

        return cls(
            id=department.id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=department.created_at,
            employees=employees,
            children=child_schemas,
        )


class DepartmentUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    parent_id: str | None = None


class DeleteDepartmentQuerySchema(BaseModel):
    mode: Literal["cascade", "reassign"]
    reassign_to_department_id: str | None = None

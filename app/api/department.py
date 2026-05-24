from fastapi import APIRouter, Depends, status, Query

from schemas.base import BaseResponse
from schemas.department import (
    DepartmentCreateSchema,
    DepartmentResponseSchema,
    DepartmentUpdateSchema,
    DeleteDepartmentQuerySchema,
    DepartmentTreeSchema
)
from schemas.employee import EmployeeCreateSchema, EmployeeResponseSchema
from dependencies.providers import get_department_service, get_employee_service
from services.department_service import DepartmentService
from services.employee_service import EmployeeService

router = APIRouter(prefix="/api/v1/departments", tags=["Departments"])


@router.post(
    path="/",
    summary="Create a new department",
    response_model=BaseResponse[DepartmentResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    data: DepartmentCreateSchema,
    service: DepartmentService = Depends(get_department_service),
):
    department = await service.create_department(data)
    return BaseResponse(success=True, data=department)


@router.post(
    path="/{department_id}/employees/",
    summary="Create employee in department",
    response_model=BaseResponse[EmployeeResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    department_id: str,
    data: EmployeeCreateSchema,
    service: EmployeeService = Depends(get_employee_service),
):
    employee = await service.create_employee(department_id, data)
    return BaseResponse(success=True, data=employee)


@router.get(
    path="/{department_id}/",
    summary="Get department details",
    response_model=BaseResponse[DepartmentTreeSchema],
)
async def get_department(
    department_id: str,
    depth: int = Query(default=1, ge=1, le=5),
    include_employees: bool = Query(default=True),
    service: DepartmentService = Depends(get_department_service),
):
    department = await service.get_department_details(
        department_id=department_id,
        depth=depth,
        include_employees=include_employees,
    )
    return BaseResponse(success=True, data=department)


@router.patch(
    path="/{department_id}",
    summary="Update department details",
    response_model=BaseResponse[DepartmentResponseSchema],
)
async def update_department(
    department_id: str,
    data: DepartmentUpdateSchema,
    service: DepartmentService = Depends(get_department_service),
):
    department = await service.update_department(department_id, data)
    return BaseResponse(success=True, data=department)


@router.delete(
    path="/{department_id}",
    summary="Delete department details",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    department_id: str,
    query: DeleteDepartmentQuerySchema = Depends(),
    service: DepartmentService = Depends(get_department_service),
):
    await service.delete_department(
        department_id=department_id,
        mode=query.mode,
        reassign_to_department_id=query.reassign_to_department_id
    )
    return BaseResponse(success=True)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from services.department_service import DepartmentService
from services.employee_service import EmployeeService
from repositories.department_repo import DepartmentRepository
from repositories.employee_repo import EmployeeRepository


def get_department_service(
    session: AsyncSession = Depends(get_session),
):
    department_repo = DepartmentRepository(session)
    employee_repo = EmployeeRepository(session)
    return DepartmentService(session, department_repo, employee_repo)


def get_employee_service(
    session: AsyncSession = Depends(get_session),
):
    department_repo = DepartmentRepository(session)
    employee_repo = EmployeeRepository(session)
    return EmployeeService(session, department_repo, employee_repo)

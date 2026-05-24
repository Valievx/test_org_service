from domain.exceptions import DepartmentNotFoundError
from repositories.department_repo import DepartmentRepository
from repositories.employee_repo import EmployeeRepository
from schemas.employee import EmployeeCreateSchema


class EmployeeService:
    def __init__(
        self,
        session,
        department_repository: DepartmentRepository,
        employee_repository: EmployeeRepository,
    ):
        self.session = session
        self.department_repository = department_repository
        self.employee_repository = employee_repository

    async def create_employee(
        self,
        department_id: str,
        data: EmployeeCreateSchema,
    ):

        department = await self.department_repository.get_by_id(department_id)
        if not department:
            raise DepartmentNotFoundError()

        employee = await self.employee_repository.create(
            department_id=department_id,
            full_name=data.full_name,
            position=data.position,
            hired_at=data.hired_at,
        )

        await self.session.commit()
        return employee

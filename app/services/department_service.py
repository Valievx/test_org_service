from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions import (
    ParentNotFoundError,
    DepartmentAlreadyExistsError,
    DepartmentNotFoundError,
    DepartmentCycleError,
    InvalidReassignError
)
from models.organization import Department
from schemas.department import (
    DepartmentCreateSchema,
    DepartmentDetailsSchema,
    DepartmentTreeSchema,
    DepartmentUpdateSchema
)
from schemas.employee import EmployeeResponseSchema
from repositories.department_repo import DepartmentRepository
from repositories.employee_repo import EmployeeRepository


class DepartmentService:

    def __init__(
        self,
        session: AsyncSession,
        department_repository: DepartmentRepository,
        employee_repository: EmployeeRepository,
    ):
        self.session = session
        self.department_repository = department_repository
        self.employee_repository = employee_repository

    async def create_department(
        self,
        data: DepartmentCreateSchema
    ) -> Department:

        if data.parent_id is not None:
            parent = await self.department_repository.get_by_id(data.parent_id)

            if not parent:
                raise ParentNotFoundError()

        existing_department = (
            await self.department_repository.get_by_name_and_parent(
                name=data.name,
                parent_id=data.parent_id,
            )
        )

        if existing_department:
            raise DepartmentAlreadyExistsError()

        department = await self.department_repository.create(data.name, data.parent_id)

        await self.session.commit()
        return department

    async def get_department_details(
        self,
        department_id: str,
        depth: int = 1,
        include_employees: bool = True,
    ) -> DepartmentDetailsSchema:

        department = await self.department_repository.get_department_with_relations(department_id)

        if not department:
            raise DepartmentNotFoundError()

        department_tree = DepartmentTreeSchema.from_orm_tree(
            department,
            current_depth=1,
            max_depth=depth,
        )

        employees = []

        if include_employees:
            employees = sorted(
                department.employees,
                key=lambda x: x.full_name.lower(),
            )

            employees = [
                EmployeeResponseSchema.model_validate(emp)
                for emp in employees
            ]

        return DepartmentDetailsSchema(
            department=department_tree,
            employees=employees,
        )

    async def update_department(
        self,
        department_id: str,
        data: DepartmentUpdateSchema,
    ):

        department = await self.department_repository.get_department_with_relations(department_id)
        if not department:
            raise DepartmentNotFoundError()

        update_data = data.model_dump(exclude_unset=True)

        if "parent_id" in update_data:
            new_parent_id = update_data["parent_id"]

            if new_parent_id == department.id:
                raise DepartmentCycleError()

            if new_parent_id is not None:
                new_parent = await self.department_repository.get_department_with_relations(new_parent_id)

                if not new_parent:
                    raise ParentNotFoundError()

                children_ids = await self.department_repository.get_children_ids_recursive(department)
                if new_parent_id in children_ids:
                    raise DepartmentCycleError()

        if "name" in update_data:

            existing = (
                await self.department_repository.get_by_name_and_parent(
                    name=update_data["name"],
                    parent_id=update_data.get(
                        "parent_id",
                        department.parent_id,
                    ),
                )
            )

            if existing and existing.id != department.id:
                raise DepartmentAlreadyExistsError()

        updated_department = await self.department_repository.update(
            department,
            **update_data,
        )

        await self.session.commit()
        return updated_department


    async def delete_department(
        self,
        department_id,
        mode,
        reassign_to_department_id=None,
    ):

        department = await self.department_repository.get_department_with_relations(department_id)
        if not department:
            raise DepartmentNotFoundError()

        if mode == "cascade":
            await self.department_repository.delete(department)
            await self.session.commit()
            return

        reassign_department = await self.department_repository.get_by_id(reassign_to_department_id)
        if not reassign_department:
            raise DepartmentNotFoundError()


        if reassign_to_department_id == department.id:
            raise InvalidReassignError()

        await self.employee_repository.reassign_department(
            from_department_id=department.id,
            to_department_id=reassign_to_department_id,
        )

        await self.department_repository.delete(department)
        await self.session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from models.organization import Employee


class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        department_id: str,
        full_name: str,
        position: str,
        hired_at,
    ) -> Employee:

        employee = Employee(
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
        )

        self.session.add(employee)
        await self.session.flush()
        return employee

    async def reassign_department(self, from_department_id, to_department_id):

        stmt = (
            update(Employee)
            .where(
                Employee.department_id
                == from_department_id
            )
            .values(
                department_id=to_department_id
            )
        )

        await self.session.execute(stmt)

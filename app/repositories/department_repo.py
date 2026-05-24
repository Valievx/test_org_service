from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.organization import Department


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, department_id: str) -> Department | None:
        stmt = select(Department).where( Department.id == department_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name_and_parent(
        self,
        name: str,
        parent_id: str | None,
    ) -> Department | None:

        stmt = select(Department).where(
            Department.name == name,
            Department.parent_id == parent_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_department_detail(self, department_id: str) -> Department | None:
        stmt = (
            select(Department)
            .where(Department.id == department_id)
            .options(
                selectinload(Department.children)
                .selectinload(Department.children)
                .selectinload(Department.children)
                .selectinload(Department.children),
                selectinload(Department.employees),
                selectinload(Department.children)
                .selectinload(Department.employees),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, name: str, parent_id: str | None) -> Department:
        department = Department(name=name, parent_id=parent_id)

        self.session.add(department)
        return department

    async def update(self, department, **kwargs):
        for key, value in kwargs.items():
            setattr(department, key, value)

        await self.session.flush()
        return department

    async def get_children_ids_recursive(self, department, ) -> set[str]:

        result = set()

        async def walk(node):
            for child in node.children:
                result.add(child.id)
                await walk(child)

        await walk(department)
        return result

    async def delete(self, department):
        await self.session.delete(department)

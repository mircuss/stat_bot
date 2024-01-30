from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sql.models import GeoFilter, ProjectFilter, BuyerFilter


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_geo(self, name: str, filter: str) -> GeoFilter:
        geo_filter = GeoFilter(name=name, filter=filter)
        self.session.add(geo_filter)
        await self.session.commit()
        return geo_filter

    async def add_buyer(self, name: str, filter: str) -> BuyerFilter:
        buyer_filter = BuyerFilter(name=name, filter=filter)
        self.session.add(buyer_filter)
        await self.session.commit()
        return buyer_filter

    async def add_project(self, name: str, filter: str) -> ProjectFilter:
        project_filter = ProjectFilter(name=name, filter=filter)
        self.session.add(project_filter)
        await self.session.commit()
        return project_filter

    async def delet_geo_filter(self, filter_id: int):
        stmt = delete(GeoFilter).where(GeoFilter.id == filter_id)
        await self.session.execute(stmt)

    async def delet_buyer_filter(self, filter_id: int):
        stmt = delete(BuyerFilter).where(BuyerFilter.id == filter_id)
        await self.session.execute(stmt)

    async def delet_project_filter(self, filter_id: int):
        stmt = delete(ProjectFilter).where(ProjectFilter.id == filter_id)
        await self.session.execute(stmt)

    async def get_all_geo_filters(self) -> List[GeoFilter]:
        stmt = select(GeoFilter)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_buyer_filters(self) -> List[BuyerFilter]:
        stmt = select(BuyerFilter)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_project_filters(self) -> List[ProjectFilter]:
        stmt = select(ProjectFilter)
        result = await self.session.execute(stmt)
        return result.scalars().all()

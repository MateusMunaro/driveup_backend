from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import *
from schemas.schemas import *

class CompanyRepository:
    @staticmethod
    async def get_company_by_id(db: AsyncSession, company_id: int):
        result = await db.execute(select(DimCompanies).filter(DimCompanies.company_id == company_id))
        return result.scalars().first()
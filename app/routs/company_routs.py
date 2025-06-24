from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from repository.company_repository import CompanyRepository
from schemas.schemas import *
from database import get_db

router = APIRouter()

@router.get("/companies/{company_id}")
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await CompanyRepository.get_company_by_id(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return company

@router.post("/add/companies")
async def create_company(company: DimCompaniesSchema, db: AsyncSession = Depends(get_db)):
    company = await CompanyRepository.create_company(db, company)
    if company is None:
        raise HTTPException(status_code=400, detail="Erro ao criar empresa")
    return DimCompaniesSchema.model_validate(company.__dict__)
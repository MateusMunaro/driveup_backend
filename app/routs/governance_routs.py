from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from schemas.user_schemas import Token, User, TokenData
from repository.governance_repository import GovernancaRepository
from repository.user_repository import *
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import DriverSchema, RankingSchema
from database import get_db
from functools import partial
from typing import Optional

router = APIRouter()

@router.get("/drivers")
async def get_drivers(db: AsyncSession = Depends(get_db)):
    drivers = await GovernancaRepository.get_all_drivers(db)
    validate_drivers = [DriverSchema.model_validate(driver.__dict__) for driver in drivers]
    if not validate_drivers:
        raise HTTPException(status_code=404, detail="Drivers não encontrados")
    return validate_drivers

@router.get("/ranking")
async def get_ranking(db: AsyncSession = Depends(get_db), driver_id: Optional[int] = None):
    ranking_data = await GovernancaRepository.get_ranking(db, driver_id)
    
    if not ranking_data:
        raise HTTPException(status_code=404, detail="Ranking não encontrado")
    
    validate_ranking = [
        RankingSchema(
            driver_id=item["driver_id"],
            driver_name=item["driver_name"],
            ride_count=item["ride_count"]
        ) 
        for item in ranking_data
    ]
    
    # Return either model_dump() for cleaner output or the Pydantic objects directly
    return [rank.model_dump() for rank in validate_ranking]

@router.post("/add/driver")
async def post_driver(driver_data: DriverSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_driver = await UserRepository.create_user(db, driver_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_driver
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from repository.car_repository import CarRepository
from schemas.schemas import *
from database import get_db

router = APIRouter()

@router.get("/cars")
async def get_car(car_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    cars = await CarRepository.get_car(db, car_id)
    validate_cars = [DimCarsSchema.model_validate(car.__dict__) for car in cars]
    if validate_cars is None:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return validate_cars

@router.post("/add/cars")
async def create_car(car: DimCarsSchema, db: AsyncSession = Depends(get_db)):
    car = await CarRepository.create_car(db, car)
    if car is None:
        raise HTTPException(status_code=400, detail="Erro ao criar carro")
    return DimCarsSchema.model_validate(car.__dict__)
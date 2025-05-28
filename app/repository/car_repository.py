from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import *
from app.schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class CarRepository:
    @staticmethod
    async def get_car(db: AsyncSession, car_id: Optional[int] = None):
        if car_id is not None:
            result = await db.execute(select(DimCars).where(DimCars.car_id == car_id))
            car = result.scalars().first()
            return [car] if car else []
        else:
            result = await db.execute(select(DimCars))
            cars = result.scalars().all()
            return cars
        
    @staticmethod
    async def create_car(db: AsyncSession, car: DimCarsSchema):
        new_car = DimCars(
            car_id=uuid.uuid4(),
            car_name=car.car_name,
            car_brand=car.car_brand,
            car_model=car.car_model,
            car_year=car.car_year,
            car_price=car.car_price
        )
        db.add(new_car)
        await db.commit()
        await db.refresh(new_car)
        return new_car
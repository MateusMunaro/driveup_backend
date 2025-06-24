from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import *
from schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class HotelRepository:
    @staticmethod
    async def get_hotel(db: AsyncSession, hotel_id: Optional[int] = None):
        if hotel_id is not None:
            result = await db.execute(select(DimHotels).where(DimHotels.hotel_id == hotel_id))
            hotel = result.scalars().first()
            return [hotel] if hotel else []
        else:
            result = await db.execute(select(DimHotels))
            hotel = result.scalars().all()
            return hotel
        
    @staticmethod
    async def create_hotel(db: AsyncSession, hotel_data: DimHotelsSchema):
        new_hotel = DimHotels(**hotel_data.dict())
        db.add(new_hotel)
        await db.commit()
        await db.refresh(new_hotel)
        return new_hotel
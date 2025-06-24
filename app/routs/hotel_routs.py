from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from repository.hotel_repository import HotelRepository
from schemas.schemas import *
from database import get_db

router = APIRouter()

@router.get("/hotels")
async def get_hotel(hotel_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    hotels = await HotelRepository.get_hotel(db, hotel_id)
    validate_hotels = [DimHotelsSchema.model_validate(hotel.__dict__) for hotel in hotels]
    if validate_hotels is None:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    return validate_hotels

@router.post("/add/hotel")
async def post_hotel(hotel: DimHotelsSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_hotel = await HotelRepository.create_hotel(db, hotel)
        return new_hotel
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno ao criar hotel")
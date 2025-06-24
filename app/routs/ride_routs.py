from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from repository import *
from database import get_db
from schemas.schemas import *
from services.rides import (
    get_ride_by_month, 
    get_consistence_rides,
    create_tracked_ride,
    get_ride_with_track,
    get_ride_statistics,
    get_distance_per_ride 
)
from app.repository.ride_repository import RideRepository
from typing import Optional, Dict, Any, List
from datetime import *

router = APIRouter()

@router.get("/rides")
async def get_ride(ride_id: Optional[int] = None, start_date: Optional[datetime] = None, db: AsyncSession = Depends(get_db)):
    rides = await RideRepository.get_ride(db, ride_id, start_date)
    validate_rides = [StgRidesSchema.model_validate(ride.__dict__) for ride in rides]
    if validate_rides is None:
        raise HTTPException(status_code=404, detail="Ride não encontrada")
    return validate_rides

@router.get("/monthly_rides")
async def get_monthly_rides(db: AsyncSession = Depends(get_db)):
    rides = await get_ride_by_month(db)
    if not rides:
        raise HTTPException(status_code=404, detail="Nenhuma corrida encontrada")
    
    validated_rides = [MonthlyRidesSchema(data=datetime.strptime(data, '%Y-%m').date(), total_rides=total_rides) for data, total_rides in rides.items()]
    return validated_rides

@router.get("/consistence_rides")
async def get_consistence_rides_endpoint(start_date: Optional[date] = None, db: AsyncSession = Depends(get_db)):
    rides = await get_consistence_rides(db, start_date)
    validate_rides = [MonthlyRidesSchema(data=data, total_rides=total_rides) for data, total_rides in rides.items()]
    if not rides:
        raise HTTPException(status_code=404, detail="Nenhuma corrida encontrada")
    
    return validate_rides

@router.post("/add/tracked_ride")
async def add_tracked_ride(ride_data: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Adiciona uma nova corrida com dados de rastreamento de localização
    
    O corpo da requisição deve conter:
    - Dados básicos da corrida (cliente, hotel, etc.)
    - Tempo de início e fim
    - Distância total percorrida
    - Coordenadas de origem e destino
    - Opcionalmente, todas as posições registradas durante a corrida
    """
    try:
        result = await create_tracked_ride(db, ride_data)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a corrida: {str(e)}")

@router.get("/rides/tracked/{ride_id}")
async def get_tracked_ride(ride_id: str, db: AsyncSession = Depends(get_db)):
    """
    Obtém detalhes de uma corrida específica com seu percurso completo
    """
    return await get_ride_with_track(db, ride_id)

@router.get("/rides/statistics")
async def get_rides_statistics(db: AsyncSession = Depends(get_db)):
    """
    Obtém estatísticas gerais das corridas:
    - Total de corridas
    - Distância total percorrida
    - Faturamento total
    - Duração média das corridas
    """
    return await get_ride_statistics(db)

@router.get("/rides/distance_per_ride")
async def get_distance_per_ride_endpoint(date: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    """
    Obtém a distância total percorrida por mês
    """
    try:
        result = await get_distance_per_ride(db, date)
        print(f"resultado{result}")
        if not result:
            raise HTTPException(status_code=404, detail="Nenhuma corrida encontrada com os filtros especificados")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados de distância: {str(e)}")

@router.get("/locations")
async def get_locations():
    """
    Endpoint para fornecer algumas localizações comuns para o autocomplete
    """
    # Você pode carregar isso de um banco de dados ou arquivo
    locations = [
        {"name": "Aeroporto Internacional de Guarulhos", "type": "origin"},
        {"name": "Aeroporto de Congonhas", "type": "origin"},
        {"name": "Shopping Ibirapuera", "type": "destination"},
        {"name": "Avenida Paulista", "type": "destination"},
        {"name": "Parque Ibirapuera", "type": "destination"},
        {"name": "Shopping Morumbi", "type": "destination"},
        {"name": "Centro de São Paulo", "type": "destination"},
        {"name": "Estação da Luz", "type": "destination"},
        {"name": "Shopping Eldorado", "type": "destination"},
        {"name": "Mercado Municipal de São Paulo", "type": "destination"}
    ]
    return locations
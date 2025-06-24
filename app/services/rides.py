from sqlalchemy.ext.asyncio import AsyncSession
from repository.ride_repository import RideRepository
from collections import defaultdict
from datetime import *
from typing import Optional, Dict, List, Any
from fastapi import HTTPException

async def get_ride_by_month(db: AsyncSession):
    rides = await RideRepository.get_ride(db)
    rides_by_month = defaultdict(int)
    
    for ride in rides:
        data = ride.ride_date.strftime('%Y-%m')
        rides_by_month[data] += 1
    
    return dict(rides_by_month)

async def get_distance_per_ride(db: AsyncSession, date: Optional[int] = None) -> List[Dict]:
    query_results = await RideRepository.get_rides_with_distance(db, date)

    print("Query:", query_results)  # Debugging line to check the query result

    return [
        {
            "ride_id": ride[0],           # ride_id is the first element
            "client_id": ride[1],         # client_id is the second element
            "driver_id": ride[2],         # driver_id is the third element
            "driver_name": ride[3],       # driver_name is the fourth element
            "creation_date": ride[4],     # creation_date is the fifth element
            "latitude": ride[5],          # latitude is the sixth element  
            "longitude": ride[6],         # longitude is the seventh element
            "accuracy": ride[7]           # accuracy is the eighth element
        }
        for ride in query_results
    ]

async def get_consistence_rides(db: AsyncSession, start_date: Optional[date] = None):
    rides = await RideRepository.get_ride(db)
    rides_by_day = defaultdict(int)
    
    if start_date:
        data = start_date.strftime('%Y-%m')
    else:
        data = datetime.now().strftime('%Y-%m')
    
    for ride in rides:
        ride_month = ride.ride_date.strftime('%Y-%m')
        if ride_month == data:
            day = ride.ride_date.strftime('%Y-%m-%d')
            rides_by_day[day] += 1
    
    if rides_by_day:
        return dict(rides_by_day)
    else:
        raise HTTPException(status_code=404, detail="Nenhuma corrida encontrada para o mês especificado")

async def create_tracked_ride(db: AsyncSession, ride_data: Dict[str, Any]):
    """
    Cria uma nova corrida com rastreamento de localização
    
    Args:
        db: Sessão assíncrona do banco de dados
        ride_data: Dados da corrida incluindo posições
        
    Returns:
        A corrida criada
    """
    try:
        # Extrair posições do payload, se existirem
        positions = ride_data.get("ride_positions", [])
        
        # Validar dados essenciais
        if not ride_data.get("client_name"):
            raise HTTPException(status_code=400, detail="Nome do cliente é obrigatório")
        
        if not ride_data.get("start_time") or not ride_data.get("end_time"):
            raise HTTPException(status_code=400, detail="Horários de início e fim são obrigatórios")
            
        # Criar a corrida no banco de dados
        new_ride = await RideRepository.create_tracked_ride(db, ride_data, positions)
        
        return {
            "id": new_ride.ride_id,
            "message": "Corrida registrada com sucesso"
        }
        
    except Exception as e:
        # Registrar o erro para debugging
        print(f"Erro ao criar corrida: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a corrida: {str(e)}")

async def get_ride_with_track(db: AsyncSession, ride_id: str):
    """
    Busca uma corrida com dados de rastreamento
    
    Args:
        db: Sessão assíncrona do banco de dados
        ride_id: ID da corrida
        
    Returns:
        Dados da corrida e suas posições
    """
    result = await RideRepository.get_ride_with_positions(db, ride_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")
    
    ride = result["ride"]
    positions = result["positions"]
    
    # Formatar a resposta
    formatted_positions = []
    for pos in positions:
        formatted_positions.append({
            "latitude": pos.latitude,
            "longitude": pos.longitude,
            "accuracy": pos.accuracy,
            "timestamp": pos.timestamp.isoformat() if pos.timestamp else None
        })
    
    # Montar o objeto de resposta
    response = {
        "id": ride.id,
        "client_name": ride.client_name,
        "hotel_name": ride.hotel_name,
        "car_model": ride.car_model,
        "payment_method": ride.payment_method,
        "total_value": ride.total_value,
        "start_time": ride.start_time.isoformat() if ride.start_time else None,
        "end_time": ride.end_time.isoformat() if ride.end_time else None,
        "duration_seconds": ride.duration_seconds,
        "distance_km": ride.distance_km,
        "origin": {
            "latitude": ride.origin_latitude,
            "longitude": ride.origin_longitude
        } if ride.origin_latitude and ride.origin_longitude else None,
        "destination": {
            "latitude": ride.destination_latitude,
            "longitude": ride.destination_longitude
        } if ride.destination_latitude and ride.destination_longitude else None,
        "observation": ride.observation,
        "indication_source": ride.indication_source,
        "positions": formatted_positions
    }
    
    return response

async def get_ride_statistics(db: AsyncSession):
    """
    Obtém estatísticas gerais das corridas
    
    Args:
        db: Sessão assíncrona do banco de dados
        
    Returns:
        Estatísticas das corridas
    """
    try:
        stats = await RideRepository.get_ride_stats(db)
        return stats
    except Exception as e:
        print(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")

async def get_distance_by_month(db: AsyncSession):
    """
    Calcula a distância total percorrida por mês
    
    Args:
        db: Sessão assíncrona do banco de dados
        
    Returns:
        Distância por mês
    """
    rides = await RideRepository.get_ride(db)
    distance_by_month = defaultdict(float)
    
    for ride in rides:
        if ride.ride_date and ride.distance_km:
            month = ride.ride_date.strftime('%Y-%m')
            distance_by_month[month] += ride.distance_km
    
    # Arredondar valores para 2 casas decimais
    for month in distance_by_month:
        distance_by_month[month] = round(distance_by_month[month], 2)
    
    return dict(distance_by_month)
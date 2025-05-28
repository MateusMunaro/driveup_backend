from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import *
from app.schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class RideRepository:
    @staticmethod
    async def get_ride(db: AsyncSession, ride_id: Optional[int] = None, start_date: Optional[str] = None):
        if ride_id is not None:
            # Busca uma corrida específica pelo ID
            result = await db.execute(select(StgRides).where(StgRides.ride_id == ride_id))
            ride = result.scalars().first()
            return [ride] if ride else []  # Retorna uma lista com a corrida ou vazia
        else:
            # Busca todas as corridas
            result = await db.execute(select(FctRides))
            rides = result.scalars().all()
            return rides
    
    # Versão corrigida do service
    @staticmethod
    async def create_tracked_ride(
        db: AsyncSession, 
        ride_data: Dict[str, Any],
        positions: Optional[List[Dict[str, Any]]] = None
    ):
        async with db.begin():
            if ride_data.get("origin_coords"):
                ride_data["origin_latitude"] = ride_data["origin_coords"]["latitude"]
                ride_data["origin_longitude"] = ride_data["origin_coords"]["longitude"]
                del ride_data["origin_coords"]
                
            if ride_data.get("destination_coords"):
                ride_data["destination_latitude"] = ride_data["destination_coords"]["latitude"]
                ride_data["destination_longitude"] = ride_data["destination_coords"]["longitude"]
                del ride_data["destination_coords"]

            if "ride_positions" in ride_data:
                del ride_data["ride_positions"]
                
            # Formatar datas, se necessário
            if isinstance(ride_data.get("start_time"), str):
                ride_data["start_time"] = datetime.fromisoformat(ride_data["start_time"].replace('Z', '+00:00'))
                
            if isinstance(ride_data.get("end_time"), str):
                ride_data["end_time"] = datetime.fromisoformat(ride_data["end_time"].replace('Z', '+00:00'))
                
            if isinstance(ride_data.get("ride_date"), str):
                ride_data["ride_date"] = datetime.strptime(ride_data["ride_date"], '%Y-%m-%d').date()
            
            # Criar a corrida no banco de dados
            print(ride_data)
            new_ride = StgRides(**ride_data)
            print(f"nova corrida {new_ride}")
            db.add(new_ride)
            
            await db.flush()
            
            if positions:
                for pos in positions:
                    # Converter timestamp para datetime, se for string
                    if isinstance(pos.get("timestamp"), str):
                        pos["timestamp"] = datetime.fromisoformat(pos["timestamp"].replace('Z', '+00:00'))
                    
                    position_data = {
                        "ride_id": new_ride.ride_id,  # Associar à corrida
                        "latitude": pos.get("latitude"),
                        "longitude": pos.get("longitude"),
                        "accuracy": pos.get("accuracy"),
                        "timestamp": pos.get("timestamp")
                    }
                    
                    new_position = DimPositionModel(**position_data)
                    db.add(new_position)
            
            # O commit é implícito com o 'async with db.begin()'
            return new_ride
        
    @staticmethod
    async def get_ride_with_positions(db: AsyncSession, ride_id: str):
        result = await db.execute(select(StgRides).where(StgRides.ride_id == ride_id))
        ride = result.scalars().first()
        
        if not ride:
            return None
        
        # Buscar as posições
        positions_result = await db.execute(
            select(DimPositionModel)
            .where(DimPositionModel.ride_id == ride_id)
            .order_by(DimPositionModel.timestamp)
        )
        positions = positions_result.scalars().all()
        
        # Construir o resultado
        return {
            "ride": ride,
            "positions": positions
        }
    
    @staticmethod
    async def get_ride_stats(db: AsyncSession):
        """
        Obter estatísticas de todas as corridas
        
        Args:
            db: Sessão assíncrona do banco de dados
            
        Returns:
            Dict com estatísticas
        """
        # Total de corridas
        total_rides_result = await db.execute(select(func.count()).select_from(StgRides))
        total_rides = total_rides_result.scalar() or 0
        
        # Total de distância
        total_distance_result = await db.execute(select(func.sum(StgRides.distance_km)))
        total_distance = total_distance_result.scalar() or 0
        
        # Total de faturamento
        total_revenue_result = await db.execute(select(func.sum(StgRides.total_value)))
        total_revenue = total_revenue_result.scalar() or 0
        
        # Duração média
        avg_duration_result = await db.execute(select(func.avg(StgRides.duration_seconds)))
        avg_duration = avg_duration_result.scalar() or 0
        
        return {
            "total_rides": total_rides,
            "total_distance_km": round(total_distance, 2),
            "total_revenue": round(total_revenue, 2),
            "average_duration_seconds": round(avg_duration, 2)
        }
    
    @staticmethod
    async def get_rides_with_distance(db: AsyncSession, date: Optional[int] = None):
        """
        Obter corridas com distância total
        
        Args:
            db: Sessão assíncrona do banco de dados
            start_date: Data de início para filtrar as corridas (opcional)
            
        Returns:
            Lista de corridas com distância total
        """
        query = select(
            FctRides.ride_id,
            FctRides.client_id,
            FctRides.driver_id,
            DimDrivers.driver_name,
            FctRides.creation_date,
            DimPositionModel.latitude,
            DimPositionModel.longitude,
            DimPositionModel.accuracy
        ).join(
            DimPositionModel, FctRides.ride_id == DimPositionModel.ride_id
        ).join(
            DimDrivers, FctRides.driver_id == DimDrivers.driver_id
        ).order_by(FctRides.ride_id)

        if date:
            query = query.where(func.date(FctRides.creation_date) == date)
    
        result = await db.execute(query)
        rides = result.all()

        print(f"Rides: {rides}")
        
        return rides
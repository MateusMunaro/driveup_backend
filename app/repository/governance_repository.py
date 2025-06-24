from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import *
from schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class GovernancaRepository:
    async def get_all_drivers(db: AsyncSession):
        result = await db.execute(select(DimDrivers))
        drivers = result.scalars().all()
        return drivers
    
    async def get_ranking(db: AsyncSession, driver_id: Optional[int] = None):
        """
        Get ranking of drivers by number of rides.
        Returns driver name and ride count in a structured format.
        """
        if driver_id is not None:
            # Query for a specific driver
            query = select(
                DimDrivers.driver_id,
                DimDrivers.driver_name,
                func.count(FctRides.ride_id).label('ride_count')
            ).\
            join(FctRides, DimDrivers.driver_id == FctRides.driver_id).\
            where(DimDrivers.driver_id == driver_id).\
            group_by(DimDrivers.driver_id, DimDrivers.driver_name).\
            order_by(func.count(FctRides.ride_id).desc())
        else:
            # Query for all drivers, now using FctRides instead of StgRides
            query = select(
                DimDrivers.driver_id,
                DimDrivers.driver_name,
                func.count(FctRides.ride_id).label('ride_count')
            ).\
            join(FctRides, DimDrivers.driver_id == FctRides.driver_id).\
            group_by(DimDrivers.driver_id, DimDrivers.driver_name).\
            order_by(func.count(FctRides.ride_id).desc())

        result = await db.execute(query)
        ranking_data = result.all()
        
        # Format the results as a list of dictionaries with the required information
        ranking = [
            {
                "driver_id": row.driver_id,
                "driver_name": row.driver_name,
                "ride_count": row.ride_count
            }
            for row in ranking_data
        ]
        
        return ranking

    async def create_or_edit_driver(db: AsyncSession, driver: DriverSchema):
        if driver.driver_id is not None:
            # Atualiza um motorista existente
            result = await db.execute(select(DimDrivers).where(DimDrivers.driver_id == driver.driver_id))
            driver_to_update = result.scalars().first()
            if driver_to_update is None:
                raise ValueError(f"Motorista com ID {driver.driver_id} não encontrado")
            for key, value in driver.dict().items():
                setattr(driver_to_update, key, value)
            await db.commit()
            await db.refresh(driver_to_update)
            return driver_to_update
        else:
            # Cria um novo motorista
            new_driver = DimDrivers(**driver.dict())
            db.add(new_driver)
            await db.commit()
            await db.refresh(new_driver)
            return new_driver
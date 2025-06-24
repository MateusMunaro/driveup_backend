from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import *
from schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class ClientRepository:
    @staticmethod
    async def get_clients(db: AsyncSession, client_id: Optional[int] = None):
        if client_id is not None:
            result = await db.execute(select(DimClients).where(DimClients.client_id == client_id))
            client = result.scalars().first()
            return [client] if client else []
        else:
            result = await db.execute(select(DimClients))
            clients = result.scalars().all()  # Obtém uma lista de instâncias de DimClients
            return clients
        
    @staticmethod
    async def create_client(db: AsyncSession, client_data: DimClientsSchema):
        """
        Cria um novo cliente no banco de dados
        
        Args:
            db: Sessão assíncrona do banco de dados
            client_data: Dados do cliente a ser criado
            
        Returns:
            O cliente criado
        """
        new_client = DimClients(**client_data.dict())
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        return new_client
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from repository.client_repository import ClientRepository
from schemas.schemas import *
from database import get_db

router = APIRouter()

@router.get("/clients")
async def get_client(client_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    clients = await ClientRepository.get_clients(db, client_id)
    validate_clients = [DimClientsSchema.model_validate(client.__dict__) for client in clients]
    if validate_clients is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validate_clients

@router.post("/add/clients")
async def create_client(client: DimClientsSchema, db: AsyncSession = Depends(get_db)):
    client = await ClientRepository.create_client(db, client)
    if client is None:
        raise HTTPException(status_code=400, detail="Erro ao criar cliente")
    return DimClientsSchema.model_validate(client.__dict__)
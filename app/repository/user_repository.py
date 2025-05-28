from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import *
from app.schemas.schemas import *
from typing import Optional
from passlib.context import CryptContext
import uuid

class UserRepository:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def authenticate_user(username: str, password: str, db: AsyncSession):

        query = select(DimDrivers, DriverAuthentication).\
            join(DriverAuthentication, DimDrivers.driver_id == DriverAuthentication.driver_id).\
            where(DimDrivers.driver_name == username)
        
        result = await db.execute(query)
        user, auth = result.first() or (None, None)

        if not user or not auth:
            return False

        # Verifica se a senha está correta
        if not UserRepository.pwd_context.verify(password, auth.hash_password):
            print("Senha incorreta ❌")
            return False

        return user
    
    @staticmethod
    async def get_user_roles(db: AsyncSession, drivet_id: int):
        query = select(DimDrivers.driver_role).where(DimDrivers.driver_id == drivet_id)
        result = await db.execute(query)
        roles = result.scalars().all()

        return roles
    
    @staticmethod
    async def create_user(db: AsyncSession, driver_data: DriverSchema):
        """
        Cria ou atualiza um motorista no sistema com autenticação
        
        Args:
            db: Sessão assíncrona do banco de dados
            driver_data: Dados completos do motorista (incluindo password)
            
        Returns:
            O motorista criado/atualizado
        """
        # Extrair e remover a senha do objeto de dados para não salvar na tabela DimDrivers
        password = driver_data.password
        driver_dict = driver_data.dict(exclude={"password"})
        
        # Hash da senha
        hashed_password = UserRepository.pwd_context.hash(password)
        
        if driver_data.driver_id is not None:
            # Atualiza um motorista existente
            result = await db.execute(select(DimDrivers).where(DimDrivers.driver_id == driver_data.driver_id))
            driver = result.scalars().first()
            
            if driver is None:
                raise ValueError(f"Motorista com ID {driver_data.driver_id} não encontrado")
                
            # Atualiza os dados do motorista
            for key, value in driver_dict.items():
                if key != "driver_id" and value is not None:
                    setattr(driver, key, value)
                
            # Busca registro de autenticação ou cria um novo
            auth_result = await db.execute(
                select(DriverAuthentication).where(DriverAuthentication.driver_id == driver.driver_id)
            )
            auth = auth_result.scalars().first()
            
            if auth:
                auth.hash_password = hashed_password
            else:
                auth = DriverAuthentication(driver_id=driver.driver_id, hash_password=hashed_password)
                db.add(auth)
        else:
            # Cria um novo motorista
            driver = DimDrivers(**driver_dict)
            db.add(driver)
            await db.flush()  # Para obter o ID gerado
            
            # Cria o registro de autenticação
            auth = DriverAuthentication(driver_id=driver.driver_id, hash_password=hashed_password)
            db.add(auth)
        
        await db.commit()
        await db.refresh(driver)
        return driver
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, List
from jose import JWTError, jwt
from app.schemas.user_schemas import User, Token, TokenData
from datetime import datetime, timedelta
from app.repository.user_repository import UserRepository

app = FastAPI()

# Configurações
SECRET_KEY = "DriveUp10"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependência para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Funções auxiliares
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await UserRepository.authenticate_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Função melhorada para verificação de múltiplas roles
# async def check_user_role(required_roles: List[str], token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
#     user = await get_current_user(token, db)
    
#     # Buscar as roles do usuário no banco de dados
#     user_roles = await UserRepository.get_user_roles(db, user.id)
    
#     # Verificar se o usuário tem pelo menos uma das roles requeridas
#     has_required_role = any(role in required_roles for role in user_roles)
    
#     if not has_required_role:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Permissão negada. Role necessária."
#         )
    
#     # Retornar o usuário com suas roles
#     return {"user": user, "roles": user_roles}

async def get_current_user_with_role(required_role: str, current_user: User = Depends(get_current_user)):
    if current_user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada",
        )
    return current_user

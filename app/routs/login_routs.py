from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from schemas.user_schemas import Token, User, TokenData
from services.login_service import create_access_token, get_current_user, get_current_user_with_role
from repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from functools import partial

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await UserRepository.authenticate_user(form_data.username, form_data.password, db)
    print(user)
    print(form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_roles = await UserRepository.get_user_roles(db, user.driver_id)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.driver_name, "roles": user.driver_role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "Você está autenticado!", "user": current_user.username}

@router.get("/admin")
async def admin_route(current_user: dict = Depends(partial(get_current_user_with_role, "admin"))):
    return {"message": "Acesso concedido ao admin!", "user": current_user}
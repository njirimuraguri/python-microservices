# src/main/auth/routes.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from . import jwt_security, schema, model, crud
# from main.auth import jwt_security
# from main.auth.schemas import Token
from src.main.core.dependencies import get_session
from src.main.config import Settings, get_settings

router = APIRouter()

settings: Settings = get_settings()
# OAuth2PasswordBearer is a class we use to receive the token from a request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def create_user(async_db: AsyncSession, user_in: schema.UserCreate) -> model.User:
    user = await crud.user.create_user(async_db=async_db, obj_in=user_in)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return jwt_security.verify_token(token)


@router.post("/register", response_model=model.User)
async def register_user(user_in: schema.UserCreate, async_db: AsyncSession = Depends(get_session)):
    existing_user = await crud.user.get_user_by_email(async_db=async_db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered",
        )

    user = await crud.user.create_user(async_db=async_db, obj_in=user_in)
    return user


# Route to log in and generate a JWT token
@router.post("/token", response_model=schema.Token)
async def login_for_access_token(async_db: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate(async_db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": jwt_security.create_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


# Example route that requires authentication
@router.get("/users/me", response_model=model.User)
def read_users_me(current_user: model.User = Depends(get_current_user)):
    return current_user
# src/main/auth/routes.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from . import jwt_security, schema, model, crud
from src.main.core.dependencies import get_session
from src.main.config import Settings, get_settings

router = APIRouter()

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# create user
async def create_user(async_db: AsyncSession, user_in: schema.UserCreate) -> model.User:
    user = await crud.user.create_user(async_db=async_db, obj_in=user_in)
    return user


# get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return jwt_security.verify_token(token)


# route to register a user
@router.post("/Register User", response_model=schema.User)
async def register_user(user_in: schema.UserCreate, async_db: AsyncSession = Depends(get_session)):
    async with async_db as session:
        existing_user = await crud.user.get_user_by_email(async_db=session, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered",
        )

    user = await crud.user.create_user(async_db=session, obj_in=user_in)
    return user


# Route to log in and generate a JWT token
@router.post("/Token", response_model=schema.Token)
async def login_for_access_token(async_db: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):  # noqa: E501
    async with async_db as session:
        user = await crud.user.authenticate(session, email=form_data.username, password=form_data.password)

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
@router.get("/users/me", response_model=schema.User)
def read_users_me(current_user: model.User = Depends(get_current_user)):
    return current_user

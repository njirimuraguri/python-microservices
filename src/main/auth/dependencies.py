from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.config import Settings, get_settings
from src.main.core.dependencies import get_session
from . import crud, model, schema, jwt_security

settings: Settings = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)


async def get_current_user(
    async_db: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> model.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schema.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_list = await crud.user.get_users(async_db, id=token_data.sub)  # type: ignore
    if user_list == []:
        raise HTTPException(status_code=404, detail="User not found")
    return user_list[0]
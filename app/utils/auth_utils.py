from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.hashing import Hasher
from app.models.auth_models import TokenData
from app.models.user_models import SUser
from app.repos.user_repository import UserRepository
from app.config import Settings, get_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# token == username == email
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> SUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.algoritm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await UserRepository.find_one(token_data.email)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(
    data: dict, settings: Settings, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.algoritm
    )
    return encoded_jwt

async def authenticate_user(email: str, password: str) -> SUser | bool:
    user = await UserRepository.find_one(email)

    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False

    return user

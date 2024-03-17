from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import Settings, get_settings
from app.models.auth_models import Token
from app.models.user_models import SUser
from app.utils.auth_utils import (
    authenticate_user,
    create_access_token,
    oauth2_scheme,
    get_current_user,
)


authorize_router = APIRouter(prefix="/auth", tags=["Authorization"])


@authorize_router.get("/")
async def test_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# username == email
@authorize_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
):
    user = await authenticate_user(form_data.username, form_data.password)
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, settings=settings, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@authorize_router.get("/me")
async def read_users_me(current_user: Annotated[SUser, Depends(get_current_user)]):
    return current_user

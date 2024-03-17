from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.hashing import Hasher
from app.repository import UserRepository
from app.schemas import SUser


authorize_router = APIRouter(prefix="/auth", tags=["Authorization"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@authorize_router.get("/")
async def test_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# token == username == email
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await UserRepository.find_one(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# username == email
@authorize_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserRepository.find_one(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not Hasher.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}


@authorize_router.get("/me")
async def read_users_me(current_user: Annotated[SUser, Depends(get_current_user)]):
    return current_user

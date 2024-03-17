from typing import Annotated
from fastapi import APIRouter, Depends

from app.hashing import Hasher
from app.repository import UserRepository
from app.schemas import SUser, SUserAdd, SUserId


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/")
async def create_user(user: Annotated[SUserAdd, Depends()]) -> SUserId:
    user.password = Hasher.get_password_hash(user.password)
    user_id = await UserRepository.add_one(user)
    return SUserId(user_id=user_id)


@user_router.get("/")
async def get_users() -> list[SUser]:
    users = await UserRepository.find_all()
    return users


@user_router.get("/{email}")
async def get_user(email: str) -> SUser:
    user = await UserRepository.find_one(email)
    return user


@user_router.put("/{id}")
async def update_user(id: int, user: Annotated[SUserAdd, Depends()]) -> SUserId:
    user.password = Hasher.get_password_hash(user.password)
    await UserRepository.update_one(id, user)
    return SUserId(user_id=id)


@user_router.delete("{email}")
async def delete_user(email: str) -> SUser:
    return await UserRepository.delete_one(email)

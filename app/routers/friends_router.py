from typing import Annotated
from fastapi import APIRouter, Depends

from app.models.friend_models import SFriend, SFriendAdd
from app.repos.friends_repository import FriendsRepository


friends_router = APIRouter(prefix="/friends", tags=["Friends"])


@friends_router.post("/")
async def add_friend(friend: Annotated[SFriendAdd, Depends()]) -> SFriend:
    return await FriendsRepository.add_one(friend)


@friends_router.delete("/")
async def delete_friend(friends: Annotated[SFriend, Depends()]) -> SFriend:
    return await FriendsRepository.delete_one(friends)


@friends_router.get("/{user_id}")
async def get_friends(user_id: int) -> list[SFriend]:
    return await FriendsRepository.find_all(user_id)

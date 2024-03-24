from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.friend_models import SFriendAdd
from app.models.friend_request_models import SFriendRequest, SFriendRequestAdd
from app.repos.friends_request_repository import FriendsRequestRepository
from app.repos.friends_repository import FriendsRepository


friends_requests_router = APIRouter(prefix="/friends_requests", tags=["Friends requests"])

@friends_requests_router.post("/")
async def send_friend_request(request: Annotated[SFriendRequestAdd, Depends()]) -> SFriendRequest:
    return await FriendsRequestRepository.add_one(request)

@friends_requests_router.get("/{user_id}")
async def get_friend_requests(user_id: int) -> list[SFriendRequest]:
    return await FriendsRequestRepository.find_all(user_id);


@friends_requests_router.post("/accept")
async def accept_friend_request(request: Annotated[SFriendRequest, Depends()]):
    friends_request = await FriendsRequestRepository.find_one(request) 

    if not friends_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found")

    await FriendsRepository.add_one(SFriendAdd(user_id=friends_request.user_id, friend_id=friends_request.friend_id))
    await FriendsRequestRepository.delete_one(friends_request)

    return {"message": "Friend request accepted"}

@friends_requests_router.post("/reject")
async def reject_friend_request(request: Annotated[SFriendRequest, Depends()]):
    friends_request = await FriendsRequestRepository.find_one(request) 

    if not friends_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found")

    await FriendsRequestRepository.delete_one(friends_request)

    return {"message": "Friend request rejected"}


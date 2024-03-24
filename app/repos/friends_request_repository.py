from sqlalchemy import delete, select
from app.models.friend_request_models import SFriendRequestAdd, SFriendRequest
from app.database import FriendRequestOrm, new_session


class FriendsRequestRepository:
    @classmethod
    async def add_one(cls, data: SFriendRequestAdd) -> SFriendRequest:
        async with new_session() as session:
            request_dict = data.model_dump()
            request = FriendRequestOrm(**request_dict)
            session.add(request)
            await session.flush()
            await session.commit()
            return SFriendRequest(user_id=request.user_id, friend_id=request.friend_id)

    @classmethod
    async def find_one(cls, data: SFriendRequest) -> SFriendRequest:
        async with new_session() as session:
            query = select(FriendRequestOrm).where(
                FriendRequestOrm.user_id == data.user_id,
                FriendRequestOrm.friend_id == data.friend_id
            )
            result = await session.execute(query)
            request_model = result.scalar()
            request_schema = SFriendRequest.model_validate(request_model)
            return request_schema

    @classmethod
    async def find_all(cls, user_id: int) -> list[SFriendRequest]:
        async with new_session() as session:
            query = select(FriendRequestOrm).where(
                FriendRequestOrm.user_id == user_id,
            )
            result = await session.execute(query)
            request_models = result.scalars().all()
            request_schemas = [
                SFriendRequest.model_validate(request_model)
                for request_model in request_models
            ]
            return request_schemas

    @classmethod
    async def delete_one(cls, data: SFriendRequest):
        async with new_session() as session:
            query = delete(FriendRequestOrm).where(
                FriendRequestOrm.user_id == data.user_id,
                FriendRequestOrm.friend_id == data.friend_id,
            )
            await session.execute(query)
            await session.commit()

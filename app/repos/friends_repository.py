from sqlalchemy import delete, select
from app.models.friend_models import SFriend, SFriendAdd
from app.database import FriendOrm, new_session


class FriendsRepository:
    @classmethod
    async def add_one(cls, data: SFriendAdd) -> SFriend:
        async with new_session() as session:
            friend_dict = data.model_dump()
            friend = FriendOrm(**friend_dict)
            session.add(friend)
            await session.flush()
            await session.commit()
            return SFriend(user_id=friend.user_id, friend_id=friend.friend_id)

    @classmethod
    async def delete_one(cls, data: SFriend):
        async with new_session() as session:
            query = delete(FriendOrm).where(
                FriendOrm.user_id == data.user_id, FriendOrm.friend_id == data.friend_id
            )
            result = await session.execute(query)
            friend_model = result.scalar()
            friend_schema = SFriend.model_validate(friend_model)
            await session.commit()
            return friend_schema

    @classmethod 
    async def find_all(cls, user_id: int) -> list[SFriend]:
        async with new_session() as session:
            query = select(FriendOrm).where(FriendOrm.user_id == user_id)
            result = await session.execute(query)
            friend_models = result.scalars().all()
            friend_schemas = [SFriend.model_validate(friend_model) for friend_model in friend_models]
            return friend_schemas

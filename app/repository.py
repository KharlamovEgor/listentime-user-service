from sqlalchemy import delete, update, select
from app.schemas import SUser, SUserAdd
from app.database import UserOrm, new_session


class UserRepository:
    @classmethod
    async def add_one(cls, data: SUserAdd) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UserOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def find_all(cls) -> list[SUser]:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_schemas = [SUser.model_validate(user) for user in user_models]
            return user_schemas

    @classmethod
    async def find_one(cls, email: str) -> SUser:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user_model = result.scalar_one_or_none()
            user_schema = SUser.model_validate(user_model)
            return user_schema

    @classmethod
    async def update_one(cls, id: int, data: SUserAdd) -> None:
        async with new_session() as session:
            query = (
                update(UserOrm)
                .where(UserOrm.id == id)
                .values(
                    username=data.username, email=data.email, password=data.password
                )
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_one(cls, email: str) -> SUser:
        async with new_session() as session:
            query = delete(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user_model = result.scalar()
            user_schema = SUser.model_validate(user_model)
            return user_schema

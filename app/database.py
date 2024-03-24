from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

engine = create_async_engine("sqlite+aiosqlite:///users.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


class FriendOrm(Model):
    __tablename__ = "friends"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class FriendRequestOrm(Model):
    __tablename__ = "friend_requests"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync((Model.metadata.drop_all))

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_tables, delete_tables
from app.routers.users_router import user_router
from app.routers.authorize_router import authorize_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield
    print("END")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(authorize_router)

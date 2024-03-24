from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run

from app.database import create_tables, delete_tables
from app.routers.users_router import user_router
from app.routers.authorize_router import authorize_router
from app.routers.friends_router import friends_router
from app.routers.friends_requests_router import friends_requests_router
from app.config import get_settings

# Temporary solution
@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield
    print("END")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(authorize_router)
app.include_router(friends_router)
app.include_router(friends_requests_router)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=get_settings().port)

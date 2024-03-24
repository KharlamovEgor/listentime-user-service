from pydantic import BaseModel, ConfigDict 


class SUserAdd(BaseModel):
    username: str
    email: str
    password: str


class SUser(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    user_id: int
    ok: bool = True



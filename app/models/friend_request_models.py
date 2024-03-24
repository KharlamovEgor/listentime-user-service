from pydantic import BaseModel, ConfigDict


class SFriendRequestAdd(BaseModel):
    user_id: int
    friend_id: int


class SFriendRequest(SFriendRequestAdd):
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict


class SFriendAdd(BaseModel):
    user_id: int
    friend_id: int


class SFriend(SFriendAdd):
    model_config = ConfigDict(from_attributes=True)

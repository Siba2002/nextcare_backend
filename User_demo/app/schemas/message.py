from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    user_id: int
    message: str
    is_bot: bool = False


class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    user_id: int
    message: str
    is_bot: bool = False
    created_at: datetime

    class Config:
        orm_mode = True

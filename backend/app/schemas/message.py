from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    chat_id: int
    sender_id: int

class MessageOut(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class MessageIn(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str

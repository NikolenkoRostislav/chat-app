from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    chat_id: int

class MessageRead(MessageBase):
    id: int
    sender_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MessageSend(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str

from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class MessageBase(BaseModel):
    content: Annotated[str, Field(min_length=1, max_length=500)]
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

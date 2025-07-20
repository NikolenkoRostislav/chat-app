from pydantic import BaseModel

class ChatBase(BaseModel):
    is_group: bool
    group_name: str | None = None

class ChatOut(ChatBase):
    id: int

    class Config:
        from_attributes = True

class ChatIn(ChatBase):
    pass

class ChatUpdate(BaseModel):
    group_name: str

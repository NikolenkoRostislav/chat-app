from pydantic import BaseModel

class ChatBase(BaseModel):
    name: str | None = None
    icon_url: str | None = None

class ChatRead(ChatBase):
    creator_id: int
    id: int

    class Config:
        from_attributes = True

class ChatCreate(ChatBase):
    pass

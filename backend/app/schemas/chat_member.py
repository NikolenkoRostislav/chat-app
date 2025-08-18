from pydantic import BaseModel

class ChatMemberBase(BaseModel):
    chat_id: int
    user_id: int

class ChatMemberRead(ChatMemberBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class ChatMemberCreate(ChatMemberBase):
    pass

class ChatMemberDelete(ChatMemberBase):
    pass

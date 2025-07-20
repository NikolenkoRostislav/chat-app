from pydantic import BaseModel

class ChatMemberBase(BaseModel):
    chat_id: int
    user_id: int

class ChatMemberOut(ChatMemberBase):
    id: int

    class Config:
        from_attributes = True

class ChatMemberIn(ChatMemberBase):
    pass

from pydantic import BaseModel

class ChatMemberBase(BaseModel):
    chat_id: int
    user_id: int

class ChatMemberOut(ChatMemberBase):
    id: int

    class Config:
        orm_mode = True

class ChatMemberIn(ChatMemberBase):
    pass

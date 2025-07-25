from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String, index=True)
    icon_url = Column(String)

    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    is_group = Column(Boolean, nullable=False, default=False)
    group_name = Column(String)

    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")
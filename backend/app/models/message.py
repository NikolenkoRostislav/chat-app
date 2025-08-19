from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="messages_sent", lazy="joined")
    chat = relationship("Chat", back_populates="messages", lazy="joined")

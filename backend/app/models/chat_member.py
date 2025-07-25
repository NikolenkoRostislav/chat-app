from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="uix_chat_user"),
    )

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")
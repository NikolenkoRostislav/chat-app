from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    pfp_url = Column(String)
    last_online = Column(DateTime, default=datetime.utcnow)

    messages_sent = relationship("Message", back_populates="sender")
    chat_memberships = relationship("ChatMember", back_populates="user")
    telegram_connection = relationship("TelegramConnection", back_populates="user")
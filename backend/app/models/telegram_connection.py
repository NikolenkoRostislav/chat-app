from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base

class TelegramConnection(Base):
    __tablename__ = "telegram_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    telegram_chat_id = Column(String, unique=True, index=True, nullable=True)
    temp_code = Column(String)
    code_expiry_time = Column(DateTime)

    user = relationship("User", back_populates="telegram_connection", uselist=False)
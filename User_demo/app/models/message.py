from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from ..database import Base



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(String(100), default="")
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow() + timedelta(days=1))

    # Relationship to the User model
    user = relationship("User")

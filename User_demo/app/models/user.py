from uuid import uuid4
from ..database import Base

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure id is auto-incremented
    name = Column(String(30))
    dob = Column(DateTime)
    gender = Column(String(10))
    mobile = Column(String(10), unique=True)
    password = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow() + timedelta(days=1))



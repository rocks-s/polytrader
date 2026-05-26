from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True, default=None)
    addresses_data = Column(JSON, unique=True, default=dict)
    is_subscribed = Column(Boolean, default=False)
    
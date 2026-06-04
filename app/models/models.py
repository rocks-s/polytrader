from sqlalchemy import Column, Integer, String, Boolean, JSON
from config.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, default=None)
    is_subscribed = Column(Boolean, default=False)
    chkTrsf_attempts_spent = Column(JSON, default=dict)
    autotrading_stgs = Column(JSON, default=list)
    addresses_data = Column(JSON, unique=True, default=dict)

    
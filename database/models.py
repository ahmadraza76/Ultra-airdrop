from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Index
from database.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    wallet = Column(String)
    points = Column(Float, default=0.0)
    tasks_completed = Column(JSON, default=[])
    referred_by = Column(String)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_bonus = Column(DateTime)

    __table_args__ = (
        Index("idx_telegram_id", "telegram_id"),
    )

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    wallet = Column(String)
    amount = Column(Float)
    status = Column(String, default="Pending")
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)

    __table_args__ = (
        Index("idx_withdrawal_telegram_id", "telegram_id"),
        Index("idx_status", "status"),
        Index("idx_requested_at", "requested_at"),
    )

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_activity_telegram_id", "telegram_id"),
    )

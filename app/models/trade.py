import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from models.base import AuditBase, CommonBase


class Trade(Base, AuditBase, CommonBase):
    __tablename__ = "trades"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stock_id = Column(ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", back_populates="trades", foreign_keys=[stock_id])

    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="trades", foreign_keys=[user_id])

    trade_done_by = Column(String, nullable=False)

    trade_start_price = Column(Float, nullable=False)
    trade_end_price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=False)
    trade_start_date = Column(DateTime, nullable=False)
    trade_end_date = Column(DateTime, nullable=True)
    trade_type = Column(String, nullable=False)
    trade_status = Column(String, nullable=False)
    is_Automated = Column(Boolean, nullable=False)
    trade_profit = Column(Float, nullable=True)

class Prediction(Base, AuditBase, CommonBase):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stock_id = Column(ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", back_populates="predictions", foreign_keys=[stock_id])
    symbol = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    opening_price = Column(Float, nullable=True)
    closing_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from models.base import AuditBase, CommonBase

class Stock(Base, AuditBase, CommonBase):
    __tablename__ = "stocks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)
    stockPrices = relationship("StockPrice", back_populates="stock")  # Corrected here
    trades = relationship("Trade", back_populates="stock")
    predictions = relationship("Prediction", back_populates="stock")

class StockPrice(Base, AuditBase, CommonBase):
    __tablename__ = "stock_prices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stock_id = Column(ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", back_populates="stockPrices", foreign_keys=[stock_id])  # Corrected here
    startPrice = Column(Float, nullable=False)
    endPrice = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    lowPrice = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    date = Column(Date, nullable=False, unique=True)

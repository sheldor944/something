import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from models.base import AuditBase, CommonBase

class Account(Base, AuditBase, CommonBase):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="account", foreign_keys=[user_id])

    balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base, AuditBase, CommonBase):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    account_id = Column(ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    amount = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_status = Column(String, nullable=False)

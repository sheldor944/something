import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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
    automated_balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="account")
    automated_account = relationship("AutomatedAccount", back_populates="account")


class Transaction(Base, AuditBase, CommonBase):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    account_id = Column(ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    amount = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
    transaction_done_by = Column(String, nullable = False)
    transaction_type = Column(String, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    transaction_status = Column(String, nullable=False)

class AutomatedAccount(Base, AuditBase, CommonBase):
    __tablename__ = "automated_accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    account_id = Column(ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="automated_account", foreign_keys=[account_id])
    balance = Column(Float, nullable=False)
    automated_handler = relationship("AutomatedHandler", back_populates="automated_account")

class AutomatedHandler(Base, AuditBase, CommonBase):
    __tablename__ = "automated_handlers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    automated_account_id = Column(ForeignKey("automated_accounts.id"), nullable=False)
    automated_account = relationship("AutomatedAccount", back_populates="automated_handler", foreign_keys=[automated_account_id])
    symbol = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    profit_lower_bound = Column(Float, nullable=False)
    profit_upper_bound = Column(Float, nullable=False)
    profit = Column(Float, nullable=True)
    status = Column(String, nullable=True)    
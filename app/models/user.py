import uuid
from sqlalchemy import Column, Integer,  String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base
from models.base import CommonBase  
from models.trade import Trade  
from models.account import Account

class User(Base,CommonBase):
        __tablename__ = "users"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
        user_name = Column(String, nullable=False,unique=True)
        email = Column(String, nullable=False, unique=True)
        password = Column(String, nullable=False)
        password_salt = Column(String, nullable=False)

        role_id = Column(Integer, ForeignKey("roles.id"))
        role = relationship("Role", back_populates="users",foreign_keys=[role_id])

        profile = relationship("Profile", back_populates="user",cascade="all, delete-orphan")
        trades = relationship("Trade", back_populates="user", foreign_keys=[Trade.user_id])
        account = relationship("Account", back_populates="user", foreign_keys=[Account.user_id])

class Profile(Base,CommonBase):
        __tablename__ = "profiles"
        user_id = Column(ForeignKey("users.id"), primary_key=True)
        user = relationship("User",back_populates="profile", foreign_keys=[user_id])
        first_name = Column(String, nullable=True)
        last_name = Column(String, nullable=True)
        bio = Column(String, nullable=True)
        phone = Column(String, nullable=True)
        image_id = Column(ForeignKey("images.id"))
        image = relationship("Image")

class UserSession(Base,CommonBase):
        __tablename__ = "user_sessions"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
        user_id = Column(ForeignKey("users.id"))
        ip_address = Column(String, nullable=False)
        os = Column(String, nullable=False)
        device = Column(String, nullable=False)
        browser = Column(String, nullable=False)
        token = Column(String, nullable=False)


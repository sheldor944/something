from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base
from models.base import AuditBase, CommonBase

class Department(Base,AuditBase,CommonBase):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    profiles = relationship("Profile", back_populates="department")

class Program(Base,AuditBase,CommonBase):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    profiles = relationship("Profile", back_populates="program")

class Session(Base,AuditBase,CommonBase):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    years = Column(String, nullable=False, unique=True) 
    
    profiles = relationship("Profile", back_populates="session")

from sqlalchemy import Column, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

class CommonBase:
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, index=True) 
    last_updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)

class AuditBase:
    created_by = Column(ForeignKey("users.id"), nullable=False)
    @declared_attr
    def create_user(cls):
        return relationship("User", foreign_keys=[cls.created_by])
    
    last_updated_by = Column(ForeignKey("users.id"), nullable=True)
    @declared_attr
    def last_update_user(cls):
        return relationship("User", foreign_keys=[cls.last_updated_by])
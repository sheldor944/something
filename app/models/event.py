import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from models.base import AuditBase, CommonBase


class Event(Base,AuditBase,CommonBase):  
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False, index=True)
    venue = Column(String, nullable=False)
    event_link = Column(String, nullable=True)

    banner_id = Column(ForeignKey("images.id"), nullable=True)
    banner = relationship("Image")

   



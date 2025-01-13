import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from models.base import AuditBase, CommonBase


class ExecutiveCommittee(Base,AuditBase,CommonBase):
    __tablename__ = "executive_committees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    members = relationship("ECMember", back_populates="committee")

class ECMember(Base,CommonBase):
    __tablename__ = "ec_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    user_id = Column(ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="ec_member", foreign_keys=[user_id])

    post = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    note = Column(String, nullable=True)

    image_id = Column(ForeignKey("images.id"), nullable=True)
    image = relationship("Image")

    committee_id = Column(ForeignKey("executive_committees.id"), nullable=False)
    committee = relationship("ExecutiveCommittee", back_populates="members", foreign_keys=[committee_id])


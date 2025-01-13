import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base
from models.base import AuditBase, CommonBase

people_in_hall_of_fame = Table(
    "people_in_hall_of_fame",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("hall_of_fame_id", ForeignKey("hall_of_fames.id"), primary_key=True)
)

images_in_hall_of_fame = Table(
    "images_in_hall_of_fame",
    Base.metadata,
    Column("hall_of_fame_id", ForeignKey("hall_of_fames.id"), primary_key=True),
    Column("image_id", ForeignKey("images.id"), primary_key=True)
)

class HallOfFame(Base,AuditBase,CommonBase):
    __tablename__ = "hall_of_fames"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    images = relationship("Image",secondary="images_in_hall_of_fame",single_parent=True,cascade="all, delete-orphan")

    people = relationship("User", secondary=people_in_hall_of_fame, back_populates="hall_of_fames")

        


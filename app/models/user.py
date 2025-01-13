import uuid
from sqlalchemy import Column, Integer,  String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base
from models.base import CommonBase    

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
        ec_member = relationship("ECMember", back_populates="user")
        hall_of_fames = relationship("HallOfFame", secondary="people_in_hall_of_fame", back_populates="people")

class Profile(Base,CommonBase):
        __tablename__ = "profiles"
        user_id = Column(ForeignKey("users.id"), primary_key=True)
        user = relationship("User",back_populates="profile", foreign_keys=[user_id])
        first_name = Column(String, nullable=True)
        last_name = Column(String, nullable=True)
        reg_no = Column(String, nullable=True)
        bio = Column(String, nullable=True)
        phone = Column(String, nullable=True)

        department_id = Column(ForeignKey("departments.id"))
        department = relationship("Department", back_populates="profiles", foreign_keys=[department_id]) 

        program_id = Column(ForeignKey("programs.id"))
        program = relationship("Program", back_populates="profiles", foreign_keys=[program_id])

        session_id = Column(ForeignKey("sessions.id"))
        session = relationship("Session", back_populates="profiles", foreign_keys=[session_id])

        codeforces_handle = Column(String, nullable=True)
        atcoder_handle = Column(String, nullable=True)
        vjudge_handle = Column(String, nullable=True)
        discord_handle = Column(String, nullable=True)
        github_handle = Column(String, nullable=True)
        google_account = Column(String, nullable=True)

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


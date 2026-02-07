from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstName = Column(String)
    lastName = Column(String)
    password_hash = Column(String, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    found_items = relationship("FoundItem", back_populates="user")

    claims_made = relationship(
        "ClaimRequest",
        foreign_keys="ClaimRequest.claimant_id",
        back_populates="claimant"
    )

    claims_reviewed = relationship(
        "ClaimRequest",
        foreign_keys="ClaimRequest.admin_id",
        back_populates="admin"
    )
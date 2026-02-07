from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class FoundItem(Base):
    __tablename__ = "found_items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)

    location_found = Column(String, nullable=True)
    date_found = Column(DateTime, nullable=True)

    image_url = Column(String, nullable=True)

    status = Column(String, default="available")

    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="found_items")

    claim_requests = relationship("ClaimRequest", back_populates="item")

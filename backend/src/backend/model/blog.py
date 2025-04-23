from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    published = Column(Boolean, server_default="false")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

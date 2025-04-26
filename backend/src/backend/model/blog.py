from datetime import datetime, timezone
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))  # 外键
    user: Mapped["User"] = relationship("User", back_populates="blogs")  # 关系
    title: Mapped[str] = mapped_column(String(233), index=True)
    body: Mapped[str] = mapped_column(Text, index=True)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    like: Mapped[List["User"]] = relationship(
        "User",
        secondary="blog_likes",
        back_populates="liked_blogs",
    )  # 多对多关系
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


from .user import User

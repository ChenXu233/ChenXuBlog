from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.schema.blog import BlogResponse

from ..database import Base

blog_tags = Table(
    "blog_tags",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

blog_likes = Table(
    "blog_likes",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id")),
    Column("user_uuid", String(36), ForeignKey("users.uuid")),
)


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid"))  # 外键
    user: Mapped["User"] = relationship(
        "User", back_populates="blogs", foreign_keys=[user_uuid]
    )  # 关系

    title: Mapped[str] = mapped_column(String(233), index=True)
    headshot: Mapped[Optional[str]] = mapped_column(String(233), nullable=True)
    body: Mapped[str] = mapped_column(Text, index=True)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="blog_tags",
        back_populates="blogs",
    )  # 多对多关系
    like: Mapped[List["User"]] = relationship(
        "User",
        secondary="blog_likes",
        back_populates="blog_likes",
    )  # 多对多关系
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    async def to_ResponseModel(self, db: AsyncSession) -> BlogResponse:
        await db.refresh(self, ["tags", "like"])
        return BlogResponse(**self)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    blogs: Mapped[List[Blog]] = relationship(
        "Blog",
        secondary="blog_tags",
        back_populates="tags",
    )  # 多对多关系


from .user import User

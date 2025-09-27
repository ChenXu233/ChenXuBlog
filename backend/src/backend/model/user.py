from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from backend.database import Base

# 中间关联表定义
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)


class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # 双向关系
    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permission, back_populates="permissions"
    )

    @property
    def display_name(self):
        return self.code.replace("_", " ").title()


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    # 双向关系
    users: Mapped[List["User"]] = relationship(
        secondary=user_role, back_populates="roles"
    )
    permissions: Mapped[List[Permission]] = relationship(
        secondary=role_permission, back_populates="roles"
    )

    def has_permission(self, permission_code: str) -> bool:
        return any(p.code == permission_code for p in self.permissions)


class UserInfo(Base):
    __tablename__ = "user_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid"))
    user: Mapped["User"] = relationship("User", back_populates="user_info")
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    birthday: Mapped[Optional[datetime]] = mapped_column(DateTime)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    introduction: Mapped[Optional[str]] = mapped_column(Text)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid4().hex), unique=True, index=True
    )
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))  # 扩展长度
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verify_token: Mapped[Optional[str]] = mapped_column(String(255))
    verify_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime)
    blog_likes: Mapped[List["Blog"]] = relationship(
        "Blog",
        secondary="blog_likes",
        back_populates="like",
    )  # 多对多关系
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    blogs: Mapped[List["Blog"]] = relationship(
        "Blog", back_populates="user", cascade="all, delete-orphan"
    )

    roles: Mapped[List[Role]] = relationship(
        secondary=user_role, back_populates="users"
    )
    user_info: Mapped[UserInfo] = relationship(
        "UserInfo", back_populates="user", uselist=False
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha512")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_code: str) -> bool:
        return any(role.has_permission(permission_code) for role in self.roles)


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    return (await db.execute(select(User).where(User.id == user_id))).scalars().first()


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    verification_token: str,
    token_expiry: datetime,
) -> User:
    user = User(
        username=username,
        email=email,
        password=password,
        verification_token=verification_token,
        verification_expiry=token_expiry,
    )

    try:
        # 添加默认角色
        default_role = (
            (await db.execute(select(Role).where(Role.is_default == True)))
            .scalars()
            .first()
        )
        if default_role:
            user.roles.append(default_role)

        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise e
    return user


from backend.model.blog import Blog

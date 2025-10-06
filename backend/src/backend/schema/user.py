from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    email: str = Field(..., description="邮箱")


class UserResponse(BaseModel):
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    bio: Optional[str] = Field(..., description="个人简介")
    avatar: Optional[str] = Field(..., description="头像")


class UserRegisterResponse(BaseModel):
    user_uuid: str = Field(..., description="用户UUID")

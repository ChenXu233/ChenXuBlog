from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    email: str = Field(..., description="邮箱")
    phone: str = Field(..., description="电话号码")
    avatar: str = Field(..., description="头像")
    bio: str = Field(..., description="个人简介")
    location: str = Field(..., description="所在地")
    website: str = Field(..., description="个人网站")
    github: str = Field(..., description="GitHub链接")

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    evidence: str = Field(..., description="用户名或邮箱或其他证据")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    user_uuid: str = Field(..., description="用户UUID")
    access_token: str = Field(..., description="访问令牌")

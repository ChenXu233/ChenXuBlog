from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    evidence: str = Field(..., description="用户名或邮箱或其他证据")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    user_uuid: str = Field(..., description="用户UUID")
    access_token: str = Field(..., description="访问令牌")


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., description="用户邮箱")


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="重置令牌")
    new_password: str = Field(..., description="新密码")


class MessageResponse(BaseModel):
    message: str = Field(..., description="消息")

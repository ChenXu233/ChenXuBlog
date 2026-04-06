from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User
from backend.schema.auth import (
    ForgotPasswordRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordRequest,
    UserLogin,
)
from backend.utils.jwt import (
    decode_reset_token,
    generate_access_token,
    generate_refresh_token,
    generate_reset_token,
    get_refresh_token_user,
)

auth = APIRouter(prefix="/apis/v1/auth", tags=["auth"])


async def get_user_by_evidence(evidence: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == evidence))
    result = result.scalars().first()
    if result:
        return result
    result = await db.execute(select(User).where(User.username == evidence))
    result = result.scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@auth.post("/login", response_model=LoginResponse)
async def login(request: Request, user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_evidence(user.evidence, db)

    if not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")

    jwt_token = generate_access_token(
        db_user.uuid,
    )
    refresh_token = generate_refresh_token(db_user.uuid)

    request.cookies["refresh_token"] = refresh_token

    return LoginResponse(user_uuid=db_user.uuid, access_token=jwt_token)


@auth.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """发送密码重置邮件"""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()

    # 即使用户不存在也返回成功，防止枚举邮箱攻击
    if not user:
        return MessageResponse(message="If the email exists, a reset link has been sent")

    # 生成密码重置令牌
    reset_token = generate_reset_token(user.uuid)

    # 将令牌保存到用户记录（使用 verify_token 和 verify_expiry）
    user.verify_token = reset_token
    user.verify_expiry = datetime.now(timezone.utc) + timedelta(hours=1)

    await db.commit()

    # TODO: 实际发送邮件逻辑在这里
    # 目前只记录日志
    print(f"Password reset token for {request.email}: {reset_token}")

    return MessageResponse(message="If the email exists, a reset link has been sent")


@auth.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """使用令牌重置密码"""
    try:
        token_info = decode_reset_token(request.token)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user_uuid = token_info.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    result = await db.execute(select(User).where(User.uuid == user_uuid))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 检查令牌是否匹配且未过期
    if user.verify_token != request.token:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    if not user.verify_expiry or user.verify_expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token has expired")

    # 更新密码
    user.password = request.new_password
    user.verify_token = None
    user.verify_expiry = None

    await db.commit()

    return MessageResponse(message="Password has been reset successfully")


@auth.post("/refresh", response_model=LoginResponse)
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db)):
    """刷新访问令牌"""
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    user = await get_refresh_token_user(refresh_token, db)
    access_token = generate_access_token(user.uuid)
    new_refresh_token = generate_refresh_token(user.uuid)

    request.cookies["refresh_token"] = new_refresh_token

    return LoginResponse(user_uuid=user.uuid, access_token=access_token)

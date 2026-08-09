import uuid
from datetime import UTC, datetime, timedelta, timezone
from inspect import cleandoc

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User, create_user
from backend.schema.auth import (
    ForgotPasswordRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordRequest,
    UserLogin,
)
from backend.schema.user import UserCreate, UserRegisterResponse
from backend.service.email import send_verify_email
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


@auth.post("/register", name="register_user")
async def signup_user(
    request: Request, user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserRegisterResponse:
    # 生成用户验证token，60分钟后过期
    verify_token = str(uuid.uuid4())
    token_expiry = datetime.now(UTC) + timedelta(minutes=60)

    # 确保用户名和邮箱的唯一性
    existing = await db.execute(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )
    existing_user = existing.scalars().first()

    if existing_user:
        if existing_user.is_verified:
            raise HTTPException(
                status_code=400, detail="User already exists and is verified"
            )
        # 未验证用户，更新验证token
        try:
            existing_user.verify_token = verify_token
            existing_user.verify_expiry = token_expiry
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error updating verify token: {str(e)}"
            ) from e
        await send_verify_email(request, user.email, verify_token)
        return UserRegisterResponse(user_uuid=existing_user.uuid)

    # 创建新用户
    db_user = await create_user(
        db,
        user.username,
        user.email,
        user.password,
        verify_token,
        token_expiry,
    )

    # 发送验证邮件
    await send_verify_email(request, user.email, verify_token)

    return UserRegisterResponse(user_uuid=db_user.uuid)


@auth.get("/verify/{token}", response_class=HTMLResponse, name="verify_email")
async def verify_email(
    token: str, request: Request, db: AsyncSession = Depends(get_db)
):
    """根据token对邮箱进行验证"""
    db_user = await db.execute(select(User).where(User.verify_token == token))
    db_user = db_user.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification token"
        )

    if db_user.verify_expiry is None:
        raise HTTPException(status_code=400, detail="Token expiry time missing")

    token_expiry_with_tz = db_user.verify_expiry.replace(tzinfo=timezone.utc)

    # 检查是否已经过期
    if token_expiry_with_tz < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Verification token has expired")

    # 邮箱已验证
    try:
        db_user.is_verified = True
        db_user.verify_token = None  # 将token移除
        db_user.verify_expiry = None  # 将token过期时间移除
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error verifying email: {str(e)}"
        ) from e

    html_page = cleandoc(
        """
    <html>

    <head>
        <title>Email Verification</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            p {
                color: #666;
                font-size: 18px;
            }
        </style>
    </head>
    """
        + """
    <body>
        <div class="container">
            <h1>Email Verification</h1>
            <p>Hello,{username}.</p>
            <p>Your email has been successfully verified.</p>
            <p>You can now log in to your account.</p>
        </div>
    </body>

    </html>
    """.format(username=db_user.username)
    )
    return HTMLResponse(content=html_page, status_code=200)


@auth.post("/login", response_model=LoginResponse)
async def login(
    response: Response, user: UserLogin, db: AsyncSession = Depends(get_db)
):
    db_user = await get_user_by_evidence(user.evidence, db)

    if not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")

    jwt_token = generate_access_token(db_user.uuid)
    refresh_token = generate_refresh_token(db_user.uuid)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 3600,
        samesite="lax",
    )

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
async def refresh_token(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    """刷新访问令牌"""
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    user = await get_refresh_token_user(refresh_token, db)
    access_token = generate_access_token(user.uuid)
    new_refresh_token = generate_refresh_token(user.uuid)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=7 * 24 * 3600,
        samesite="lax",
    )

    return LoginResponse(user_uuid=user.uuid, access_token=access_token)

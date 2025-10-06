import uuid
from datetime import UTC, datetime, timedelta, timezone
from inspect import cleandoc

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User, create_user
from backend.schema.user import UserCreate, UserRegisterResponse
from backend.service.email import send_verify_email

register = APIRouter(prefix="/apis/v1/auth", tags=["register"])


@register.post(
    "/register",
    name="register_user",
)
async def signup_user(
    request: Request, user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserRegisterResponse:
    # 确保用户名和邮箱的唯一性
    db_user = await db.execute(select(User).where(User.username == user.username))
    db_user = db_user.scalars().first()
    if not db_user:
        db_user = await db.execute(select(User).where(User.email == user.email))
        db_user = db_user.scalars().first()

    # 生成用户验证token，并在5分钟后过期
    verify_token = str(uuid.uuid4())
    token_expiry = datetime.now(UTC) + timedelta(minutes=60)

    if not db_user:
        # 创建用户
        db_user = await create_user(
            db,
            user.username,
            user.email,
            user.password,
            verify_token,
            token_expiry,
        )
    else:
        # 如果用户已存在，则更新验证token和过期时间
        if db_user.is_verified:
            raise HTTPException(
                status_code=400, detail="User already exists and is verified"
            )
        try:
            db_user.verify_token = verify_token
            db_user.verify_expiry = token_expiry
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error updating verify token: {str(e)}"
            ) from e

    # 发送验证邮件
    await send_verify_email(request, user.email, verify_token)

    return UserRegisterResponse(user_uuid=db_user.user_uuid)


@register.get("/verify/{token}", response_class=HTMLResponse, name="verify_email")
async def verify_email(
    token: str, request: Request, db: AsyncSession = Depends(get_db)
):
    """根据token对邮箱进行验证"""
    db_user = await db.execute(select(User).where(User.verification_token == token))
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

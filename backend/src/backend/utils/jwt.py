from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import CONFIG
from backend.database import get_db
from backend.model.user import User


def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    """生成JWT令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, CONFIG.JWT_SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> dict:
    """解码JWT令牌"""
    try:
        info = jwt.decode(token, CONFIG.JWT_SECRET_KEY, algorithms="HS256")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return info


def get_jwt_token_user_uuid(token: str = Header(..., description="JWT Token")) -> int:
    """获取JWT令牌中的用户信息"""
    if user_uuid := decode_jwt_token(token).get("sub", None) is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user_uuid


async def get_jwt_token_user(
    token: str = Header(..., description="JWT Token"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取JWT令牌中的用户信息"""
    user_uuid = decode_jwt_token(token).get("sub", None)
    user = await db.execute(select(User).where(User.uuid == user_uuid))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user

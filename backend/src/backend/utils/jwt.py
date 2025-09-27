from datetime import datetime

import jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import CONFIG
from backend.database import get_db
from backend.model.user import User


def generate_access_token(user_uuid: str) -> str:
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
            "sub": user_uuid,
            "type": "access",
        }
        return jwt.encode(payload, CONFIG.ACCESS_SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_refresh_token(user_uuid: str) -> str:
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
            "sub": user_uuid,
            "type": "refresh",
        }
        return jwt.encode(payload, CONFIG.REFRESH_SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def decode_access_token(token: str) -> dict:
    """解码访问令牌"""
    try:
        info = jwt.decode(token, CONFIG.ACCESS_SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return info


def decode_refresh_token(token: str = Header(..., description="Access Token")) -> dict:
    """解码刷新令牌"""
    try:
        info = jwt.decode(token, CONFIG.REFRESH_SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return info


def get_access_token_user_uuid(
    token: str = Header(..., description="Access Token"),
) -> str:
    """获取访问令牌中的用户信息"""
    if user_uuid := decode_access_token(token).get("sub", None) is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user_uuid


async def get_access_token_user(
    token: str = Header(..., description="Access Token"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取访问令牌中的用户信息"""
    user_uuid = decode_access_token(token).get("sub", None)
    user = await db.execute(select(User).where(User.uuid == user_uuid))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


async def get_refresh_token_user(
    token,
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取刷新令牌中的用户信息"""
    user_uuid = decode_refresh_token(token).get("sub", None)
    user = await db.execute(select(User).where(User.uuid == user_uuid))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user

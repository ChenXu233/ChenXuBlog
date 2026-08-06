from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import CONFIG
from backend.database import get_db
from backend.logger import logger
from backend.model.user import Role, User


def _generate_token(user_uuid: str, token_type: str, expires_delta: timedelta, secret_key: str) -> str:
    """通用 token 生成器"""
    payload = {
        "exp": datetime.now(timezone.utc) + expires_delta,
        "iat": datetime.now(timezone.utc),
        "sub": user_uuid,
        "type": token_type,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def generate_access_token(user_uuid: str) -> str:
    """生成访问令牌"""
    logger.info(f"Generating access token for user {user_uuid}")
    try:
        return _generate_token(user_uuid, "access", timedelta(minutes=15), CONFIG.ACCESS_SECRET_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_refresh_token(user_uuid: str) -> str:
    """生成刷新令牌"""
    logger.info(f"Generating refresh token for user {user_uuid}")
    try:
        return _generate_token(user_uuid, "refresh", timedelta(days=7), CONFIG.REFRESH_SECRET_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_reset_token(user_uuid: str) -> str:
    """生成密码重置令牌"""
    logger.info(f"Generating reset token for user {user_uuid}")
    try:
        return _generate_token(user_uuid, "reset", timedelta(hours=1), CONFIG.ACCESS_SECRET_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def decode_reset_token(token: str) -> dict:
    """解码密码重置令牌"""
    logger.info(f"Decoding reset token {token}")
    try:
        info = jwt.decode(token, CONFIG.ACCESS_SECRET_KEY, algorithms="HS256")
        if info.get("type") != "reset":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return info
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid reset token"
        )


def decode_access_token(token: str) -> dict:
    """解码访问令牌"""
    logger.info(f"Decoding access token {token}")
    try:
        info = jwt.decode(token, CONFIG.ACCESS_SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return info


def decode_refresh_token(token: str) -> dict:
    """解码刷新令牌"""
    logger.info(f"Decoding refresh token {token}")
    try:
        info = jwt.decode(token, CONFIG.REFRESH_SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return info


def extract_bearer_token(authorization: Optional[str] = Header(None, description="Authorization: Bearer <token>")) -> str:
    """从 Authorization header 中提取 Bearer token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    return authorization[7:]


def get_access_token_user_uuid(
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """从 Authorization: Bearer header 中获取用户 UUID"""
    token = extract_bearer_token(authorization)
    if user_uuid := decode_access_token(token).get("sub", None):
        return user_uuid
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")


async def get_access_token_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """从 Authorization: Bearer header 中获取用户信息"""
    from sqlalchemy.orm import selectinload
    token = extract_bearer_token(authorization)
    user_uuid = decode_access_token(token).get("sub", None)
    user = await db.execute(
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.user_info),
        )
        .where(User.uuid == user_uuid)
    )
    user = user.unique().scalars().first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


async def get_refresh_token_user(
    token: str,
    db: AsyncSession,
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
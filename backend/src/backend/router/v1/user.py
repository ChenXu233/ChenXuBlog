from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User, UserInfo
from backend.schema.user import UserEdit, UserResponse
from backend.utils.jwt import get_access_token_user
from backend.utils.permission import require_permissions

user = APIRouter(prefix="/apis/v1/user", tags=["user"])


@user.get(
    "/info",
    response_model=UserResponse,
    dependencies=[Depends(require_permissions("user:read", "Read user info"))],
)
async def get_user_info(user: User = Depends(get_access_token_user)):
    user_response = UserResponse(
        id=user.id,
        uuid=user.uuid,
        username=user.username,
        email=user.email,
        avatar=user.user_info.avatar if user.user_info else None,
        bio=user.user_info.introduction if user.user_info else None,
    )
    return user_response


@user.get(
    "/info/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permissions("user:read"))],
)
async def get_user_info_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.user_info.avatar,
        bio=user.user_info.introduction,
    )
    return user_response


@user.post(
    "/edit",
    response_model=UserResponse,
    dependencies=[Depends(require_permissions("user:edit"))],
)
async def edit_user_info(
    user_edit: UserEdit,
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    # 更新基本信息
    if user_edit.username is not None:
        user.username = user_edit.username
    if user_edit.email is not None:
        user.email = user_edit.email

    # 更新或创建 UserInfo
    if user.user_info is None:
        user.user_info = UserInfo(user_uuid=user.uuid)

    if user_edit.avatar is not None:
        user.user_info.avatar = user_edit.avatar
    if user_edit.gender is not None:
        user.user_info.gender = user_edit.gender
    if user_edit.birthday is not None:
        user.user_info.birthday = datetime.fromisoformat(user_edit.birthday)
    if user_edit.location is not None:
        user.user_info.location = user_edit.location
    if user_edit.bio is not None:
        user.user_info.introduction = user_edit.bio

    await db.commit()
    await db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.user_info.avatar if user.user_info else None,
        bio=user.user_info.introduction if user.user_info else None,
    )

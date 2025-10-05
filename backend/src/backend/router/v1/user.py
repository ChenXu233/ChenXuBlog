from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User
from backend.schema.user import UserResponse
from backend.utils.jwt import get_access_token_user
from backend.utils.permission import require_permissions

user = APIRouter(prefix="/apis/v1/user", tags=["user"])


@user.get(
    "/info",
    response_model=UserResponse,
    dependencies=[Depends(require_permissions("user:get", "Get user info"))],
)
async def get_user_info(user: User = Depends(get_access_token_user)):
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.user_info.avatar,
        bio=user.user_info.introduction,
    )
    return user_response


@user.get(
    "/info/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permissions("user:get"))],
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


@user.post("/edit")
async def edit_user_info(user_edit, user: User = Depends(get_access_token_user)): ...

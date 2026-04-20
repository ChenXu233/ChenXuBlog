from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User
from backend.schema.permission import PermissionsResponse
from backend.utils.jwt import get_access_token_user

permission = APIRouter(prefix="/apis/v1/permission", tags=["permission"])


@permission.post("/", response_model=bool)
async def have_permission(
    permission_code: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    for i in user.roles:
        if i.has_permission(permission_code):
            return True
    return False


@permission.get("/", response_model=PermissionsResponse)
async def get_permission(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    permissions = []
    seen = set()
    for role in user.roles:
        for p in role.permissions:
            if p.code not in seen:
                seen.add(p.code)
                permissions.append(p.code)

    return PermissionsResponse(permissions=permissions)

from functools import wraps
from typing import List

from fastapi import Depends, HTTPException, status

from backend.logger import logger
from backend.model.user import User
from backend.schema.permission import Permission
from backend.utils.jwt import get_access_token_user


def require_permissions(required_permission: str, permission_description: str):
    """
    权限判断装饰器，用于检查用户是否具有所需权限。

    :param required_permissions: 需要的权限列表
    """
    if not any(p.code == required_permission for p in permission_manager.permissions):
        logger.trace(
            f"Adding permission: {required_permission} - {permission_description}"
        )
        permission_manager.add_permission(required_permission, permission_description)

    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args, current_user: User = Depends(get_access_token_user), **kwargs
        ):
            # 检查用户是否具有所有所需权限
            logger.info(
                f"Checking permission: {required_permission} for user {current_user.uuid}"
            )
            if not current_user.has_permission(required_permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{required_permission}' is required to access this resource.",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


class PermissionManager:
    def __init__(self):
        self.permissions: List[Permission] = []

    def add_permission(self, code: str, description: str) -> None:
        self.permissions.append(Permission(code=code, description=description))

    def get_permissions(self) -> List[Permission]:
        return self.permissions


permission_manager = PermissionManager()

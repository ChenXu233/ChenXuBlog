from functools import wraps

from fastapi import Depends, HTTPException, status

from backend.logger import logger
from backend.model.user import User
from backend.utils.jwt import get_access_token_user

from .manager import permission_manager


def require_permissions(
    required_permission: str, permission_description: str | None = None
):
    """
    权限装饰器，将资源的权限添加到权限管理器中，并检查用户是否具有所需权限。

    :param required_permission: 需要的权限
    :param permission_description: 权限描述
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

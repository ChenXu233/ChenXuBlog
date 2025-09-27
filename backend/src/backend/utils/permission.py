from functools import wraps
from typing import List

from fastapi import Depends, HTTPException, status

from backend.model.user import User
from backend.utils.jwt import generate_access_token


def require_permissions(required_permissions: List[str]):
    """
    权限判断装饰器，用于检查用户是否具有所需权限。

    :param required_permissions: 需要的权限列表
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args, current_user: User = Depends(generate_access_token), **kwargs
        ):
            # 检查用户是否具有所有所需权限
            for permission in required_permissions:
                if not current_user.has_permission(permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission '{permission}' is required to access this resource.",
                    )
            return await func(*args, **kwargs)

        return wrapper

    return decorator

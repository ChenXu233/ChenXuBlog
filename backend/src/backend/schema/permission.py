from typing import List

from pydantic import BaseModel


class PermissionResponse(BaseModel):
    permissions: List[bool]


class Permission(BaseModel):
    permission: List[str]

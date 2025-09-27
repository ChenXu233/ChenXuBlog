from typing import List

from pydantic import BaseModel


class PermissionResponse(BaseModel):
    permissions: List[bool]


class Permission(BaseModel):
    code: str
    description: str

    class Config:
        from_attributes = True

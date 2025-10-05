from typing import List

from pydantic import BaseModel


class PermissionsResponse(BaseModel):
    permissions: List[bool]


class Permission(BaseModel):
    target: str
    action: str
    code: str
    description: str

    class Config:
        from_attributes = True

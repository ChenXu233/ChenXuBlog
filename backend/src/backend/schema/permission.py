from typing import List

from pydantic import BaseModel


class Permission(BaseModel):
    permission: List[str]

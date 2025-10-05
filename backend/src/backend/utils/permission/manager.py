from typing import List

from backend.schema.permission import Permission


class PermissionManager:
    def __init__(self):
        self.permissions: List[Permission] = []

    def add_permission(self, code: str, description: str | None = None) -> None:
        if ":" not in code:
            raise ValueError("Permission code must be in the format 'target:action'")
        if code in [p.code for p in self.permissions]:
            return
        self.permissions.append(
            Permission(
                target=code.split(":")[0],
                action=code.split(":")[1],
                code=code,
                description=description or "",
            )
        )

    def get_permissions(self) -> List[Permission]:
        return self.permissions


permission_manager = PermissionManager()

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger import logger
from backend.model.user import Permission as PermissionDB
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

    async def update_permission_db(
        self,
        db: AsyncSession,
    ) -> None:
        # 获取现有权限
        existing_permissions = (await db.execute(select(PermissionDB))).scalars().all()
        existing_set = {(p.target, p.action) for p in existing_permissions}

        # 过滤新权限
        new_permissions = [
            PermissionDB(target=p.target, action=p.action, description=p.description)
            for p in self.permissions
            if (p.target, p.action) not in existing_set
        ]
        logger.info(f"New permissions to add: {new_permissions}")

        # 批量添加新权限
        if new_permissions:
            db.add_all(new_permissions)
            await db.commit()


permission_manager = PermissionManager()

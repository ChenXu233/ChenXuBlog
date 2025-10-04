from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger import logger
from backend.model.user import Permission, Role
from backend.utils.permission import permission_manager


async def init_permissions(db: AsyncSession):
    """
    初始化权限。
    """
    logger.info("Initializing permissions")
    for permission in permission_manager.get_permissions():
        _permission = Permission(
            name=permission.code,
            description=permission.description,
        )
        db.add(_permission)
    await db.commit()


async def create_default_role(db: AsyncSession):
    """
    创建默认角色。
    """
    logger.info("Creating default role")
    superuser_role = Role(
        name="superuser",
        description="超级用户",
    )
    superuser_role.permissions = list(
        (await db.execute(select(Permission))).scalars().all()
    )
    db.add(superuser_role)
    default_role = Role(
        name="default",
        description="默认角色",
    )
    db.add(default_role)
    await db.commit()


async def create_admin_user(db: AsyncSession):
    """
    创建默认管理员用户。
    """
    logger.info("Creating default admin user")


async def first_start(db: AsyncSession):
    """
    初始化数据库，创建默认角色和管理员用户。
    """
    logger.info("First start database initialization")
    # 检查是否存在默认角色
    ...

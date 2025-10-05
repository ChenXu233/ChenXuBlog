from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger import logger
from backend.model.user import Permission, Role, User
from backend.utils.permission import permission_manager


async def check_is_first_start(db: AsyncSession) -> bool:
    """
    检查数据库是否为首次启动。
    """
    logger.info("Checking if database is first start")
    result = await db.execute(select(User))
    return result.scalars().first() is None


async def init_permissions(db: AsyncSession):
    """
    初始化权限。
    """
    logger.info("Initializing permissions")
    for permission in permission_manager.get_permissions():
        _permission = Permission(
            target=permission.target,
            action=permission.action,
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
        is_default=True,
    )
    db.add(default_role)
    await db.commit()


async def create_admin_user(db: AsyncSession):
    """
    创建默认管理员用户。
    """
    logger.info("Creating default admin user")
    superuser_role = (
        (await db.execute(select(Role).where(Role.name == "superuser")))
        .scalars()
        .first()
    )
    admin_user = User(
        username="admin",
        password="123456",
        email="admin@example.com",
        roles=[superuser_role],
    )
    db.add(admin_user)
    await db.commit()


async def first_start(db: AsyncSession):
    """
    初始化数据库，创建默认角色和管理员用户。
    """

    logger.info("Database is first start, initializing...")
    await init_permissions(db)
    await create_default_role(db)
    await create_admin_user(db)
    logger.info("Database initialization completed")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import CONFIG
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


# 基础权限定义：启动时注册，确保 default 角色可用
BASE_PERMISSIONS = [
    ("admin", "access", "访问管理后台"),
    ("user", "read", "读取用户信息"),
    ("user", "edit", "编辑用户信息"),
    ("blog", "create", "创建文章"),
    ("blog", "update", "更新文章"),
    ("blog", "delete", "删除文章"),
    ("blog", "read", "阅读文章"),
    ("comment", "create", "创建评论"),
    ("comment", "read", "阅读评论"),
    ("comment", "delete", "删除评论"),
    ("comment", "update", "更新评论"),
    ("img_bed", "create", "上传图片"),
    ("img_bed", "read", "读取图片"),
]

# default 角色拥有的基础权限
DEFAULT_ROLE_PERMISSIONS = [
    "user:read",
    "user:edit",
    "blog:create",
    "blog:update",
    "blog:delete",
    "blog:read",
    "comment:create",
    "comment:read",
    "img_bed:create",
    "img_bed:read",
]


async def init_permissions(db: AsyncSession):
    """
    初始化权限。
    """
    logger.info("Initializing permissions")
    # 注册基础权限到 permission_manager
    for target, action, description in BASE_PERMISSIONS:
        permission_manager.add_permission(f"{target}:{action}", description)

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
    # 默认角色拥有基础权限（读自己信息/写文章/评论/上传）
    all_perms = (await db.execute(select(Permission))).scalars().all()
    default_role.permissions = [
        p for p in all_perms if p.code in DEFAULT_ROLE_PERMISSIONS
    ]
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
        username=CONFIG.ADMIN_USERNAME,
        password=CONFIG.ADMIN_PASSWORD,
        email=CONFIG.ADMIN_EMAIL,
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

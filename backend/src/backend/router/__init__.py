from fastapi import FastAPI

from .v1.admin import admin
from .v1.auth import auth
from .v1.blog import blog
from .v1.comment import comment
from .v1.img_bed import img_bed
from .v1.permission import permission
from .v1.user import user


def init_routers(app: FastAPI) -> None:
    """直接注册所有路由（替代 RouterManager）。"""
    app.include_router(blog)
    app.include_router(auth)
    app.include_router(img_bed)
    app.include_router(permission)
    app.include_router(user)
    app.include_router(comment)
    app.include_router(admin)

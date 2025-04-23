from backend.router.router_manager import RouterManager

from .v1.blog import blog

router_manager = RouterManager()

router_manager.add_router(blog)

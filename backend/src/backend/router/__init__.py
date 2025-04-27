from backend.router.router_manager import RouterManager

from .v1.auth import auth
from .v1.blog import blog

router_manager = RouterManager()

router_manager.add_routers([blog, auth])

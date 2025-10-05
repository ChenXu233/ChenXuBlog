from backend.router.router_manager import RouterManager

from .v1.auth import auth
from .v1.blog import blog
from .v1.img_bed import img_bed
from .v1.permission import permission
from .v1.register import register
from .v1.token import token
from .v1.user import user

router_manager = RouterManager()

router_manager.add_routers([blog, auth, register, img_bed, permission, token, user])

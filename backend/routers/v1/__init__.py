__all__ = ["all_routers"]

from routers.v1.auth import router as auth_router
from routers.v1.users import router as users_router

all_routers = [auth_router, users_router]

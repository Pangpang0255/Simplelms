from ninja import NinjaAPI
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

api = NinjaAPI(urls_namespace='auth')
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()
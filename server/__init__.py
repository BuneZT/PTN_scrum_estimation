from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
)
from authorization import decode_jwt
from database.users_model import User

from server.api import api_routes

routes = [
    Mount("/api", routes=api_routes, name="api"),
]


class JWTAuth(AuthenticationBackend):
    async def authenticate(self, conn):

        if "authorization" not in conn.headers:
            return

        token: str = conn.headers["authorization"]
        if not token.startswith("JWT "):
            return

        token = token[4:]
        user_id = decode_jwt(token)

        if user_id is None:
            return

        return AuthCredentials(["authenticated"]), User(user_id)


def run():
    middleware = [
        Middleware(AuthenticationMiddleware, backend=JWTAuth()),
        Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    app = Starlette(True, routes, middleware=middleware)

    return app

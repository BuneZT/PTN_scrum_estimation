from typing import List
from starlette.routing import Route

from server.api.users.endpoints import Login, Register, Refresh, List

users_routes = [
    Route("/login", Login),
    Route("/register", Register),
    Route("/refresh", Refresh),
    Route("/list", List),
]

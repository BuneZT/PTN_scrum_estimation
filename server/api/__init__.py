from starlette.routing import Mount

from server.api.users import users_routes
from server.api.rooms import rooms_routes


api_routes = [
    Mount("/users", routes=users_routes),
    Mount("/rooms", routes=rooms_routes),
]

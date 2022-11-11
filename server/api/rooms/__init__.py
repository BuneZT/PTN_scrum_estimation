from typing import List
from starlette.routing import Route

from server.api.rooms.endpoints import Create, Join, My, ById, Vote

rooms_routes = [
    Route("/create", Create),
    Route("/{id:int}/join", Join),
    Route("/{id:int}/vote", Vote),
    Route("/{id:int}", ById),
    Route("/my", My),
]

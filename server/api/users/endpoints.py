from starlette.authentication import requires


from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse

from commands import users_commands
from commands.users_commands import register, WrongDataException, UserExistsException
from database.database import  get_session
from authorization import generate_jwt, decode_jwt
from users import users_service


class List(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        filter = None

        if request.query_params:
            filter = request.query_params["filter"]

        session = get_session()
        users = []
        for user in users_service.get_all_users(session):
            if filter is None:
                users.append({"username": user.login})
            elif user.login.find(filter) > -1:
                users.append({"username": user.login})

        return JSONResponse(users)


class Login(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if "login" not in body or "password" not in body:
            return Response(JSONResponse({}).body, status_code=400)

        session = get_session()

        out = users_commands.login(session, body["login"], body["password"])
        if out is None:
            return Response(JSONResponse({}).body, status_code=401)

        jwt = generate_jwt(out.id)

        return JSONResponse({"token": jwt})


class Register(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if "login" not in body or "password" not in body:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)

        try:
            register(get_session(), body["login"], body["password"])
        except WrongDataException:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)
        except UserExistsException:
            return Response(
                JSONResponse({"error": "existing_user"}).body, status_code=400
            )

        return JSONResponse({})


class Refresh(HTTPEndpoint):
    async def post(self, request):
        if "authorization" not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers["authorization"]
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)

        token = token[4:]
        user_id = decode_jwt(token)

        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)

        return JSONResponse({"token": generate_jwt(user_id)})

import typing
from datetime import datetime, timezone, timedelta

import jwt

secret = "d12pokmlkmgfl;d-012cij23cl,ssdfskd;lk32"


def generate_jwt(user_id):
    return jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=900),
        },
        secret,
        algorithm="HS256",
    )


def decode_jwt(token: str) -> typing.Union[None, int]:
    try:
        token = jwt.decode(token, secret, algorithms=["HS256"])
    except:
        return None

    return token.get("sub")

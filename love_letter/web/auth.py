import datetime

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from love_letter import config


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(token: str) -> bool:
        """
        Verify jwt token iss and aud are as expected, and not expired
        :param token:
        :return:
        """
        try:
            jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                audience=config.LOBBY_AUDIENCE,
                issuer=config.LOBBY_ISSUER,
            )
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def create_jwt():
        now = datetime.datetime.now()
        token = jwt.encode(
            payload={
                "aud": config.LOBBY_AUDIENCE,
                "iss": config.LOBBY_ISSUER,
                "exp": now + datetime.timedelta(hours=1),
            },
            key="",
        )
        return f"Bearer {token}"

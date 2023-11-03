import datetime
from functools import lru_cache

import jwt
import requests
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from love_letter.config import config


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

    @staticmethod
    @lru_cache
    def get_player_id(jwt_token: str) -> str:
        response = ""
        try:
            response = requests.get(
                config.LOBBY_USERS_ME_API, headers={"Authorization": jwt_token}
            )
        except Exception as e:
            print(e)

        if response and response.status_code == 200:
            return response.json()["id"]
        raise ValueError("Not found player id")

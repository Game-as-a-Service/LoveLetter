import time

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
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
        Issuer / Authority / Domain: https://dev-1l0ixjw8yohsluoi.us.auth0.com/
        Audience: https://api.gaas.waterballsa.tw
        :param token:
        :return:
        """
        try:
            token = jwt.get_unverified_claims(token)
            print(token)
            if (
                token["iss"] == config.LOBBY_ISSUER
                and config.LOBBY_AUDIENCE in token["aud"]
                and token["exp"] >= time.time()
            ):
                return True
        except Exception as e:
            print(e)
        return False

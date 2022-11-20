from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_INITDB_DATABASE: str = "test"
    MONGODB_URL: str = f"mongodb+srv://love:loveletter@loveletter.gjppig9.mongodb.net/" \
                       f"{MONGODB_INITDB_DATABASE}?retryWrites=true&w=majority"


settings = Settings()

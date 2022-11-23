from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# path variables
# https://fastapi.tiangolo.com/tutorial/path-params/
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# query string
# https://fastapi.tiangolo.com/tutorial/query-params/#__tabbed_4_2
@app.get("/items_with_params/{item_id}")
async def read_user_item(
        item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    # Note: mixed path variables with query string
    #
    # path variables:
    # item_id is a path variable, others are query string which don't present on the URI
    #
    # query string:
    # * needy => required, because without a default value
    # * skip => optional by a default value, client could ignore it
    # * limit => optional for int or a default None value
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# Example for request body
# https://fastapi.tiangolo.com/tutorial/body/
#
# note: it could be mixed with either path variables or query string
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    return item


# Example for response model
# https://fastapi.tiangolo.com/tutorial/response-model/
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    # password will not go to the response
    return user

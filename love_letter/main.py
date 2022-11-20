import uvicorn

from fastapi import FastAPI

from love_letter.databases import db
from love_letter.schemas import GameBaseSchema

app = FastAPI()


@app.get("/")
def read_main():
    return {"msg": "Hello World"}
    

@app.post("/enter_game")
def enter_game(game_base: GameBaseSchema):
    # 檢查DB內是否有未開賽的
    # 有的話就把玩家加進去吧
    # 沒有的話開新的賽事把玩家加進去
    
    game_base.id = 1
    r = db.customer.insert_one(game_base.dict())
    return {"msg": str(r.inserted_id)}


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=8000)

import asyncio
import json

import uvicorn
from fastapi import FastAPI
from sse_starlette import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from love_letter.repository import create_default_repository
from love_letter.service import GameService
from love_letter.web.dto import GameStatus

STREAM_DELAY = 2  # second
RETRY_TIMEOUT = 15000  # milisecond

app = FastAPI()
origins = ["*", "http://localhost:3000", "http://localhost:8081"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "POST", "OPTIONS"],
    allow_headers=[
        "accept",
        "content-type",
        "content-language",
        "accept-language",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
    ],
)

service = GameService(create_default_repository())


@app.get("/stream/{game_id}/player/{player_id}/status")
async def message_stream(request: Request, game_id: str, player_id: str):
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            status: GameStatus = GameStatus.parse_obj(
                service.get_status(game_id, player_id)
            )
            status_str = ""
            try:
                status_str = GameStatus.json(status)
            except TypeError as e:
                print(status, e)
                yield {"event": "end", "retry": RETRY_TIMEOUT, "data": e.args[0]}

            # Game is progress
            if status.final_winner is None:
                yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry": RETRY_TIMEOUT,
                    "data": status_str,
                }
            else:
                print(status)
                yield {"event": "end", "retry": RETRY_TIMEOUT, "data": status_str}
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run("love_letter.web.sse:app", host="0.0.0.0", port=8081)

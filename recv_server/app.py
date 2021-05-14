import typing as t

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from kvdb.client import KVDBClient

import json


app = FastAPI()

db = KVDBClient()


class WebHookEvent(BaseModel):
    event: str
    time: str


@app.get("/events-so-far")
async def root():
    data = []
    for key in db.list_keys():
        data.append(db.get(key))
    return {"data": data}


@app.post("/webhook")
async def register(event: WebHookEvent):
    data = jsonable_encoder(event)
    db.put(f"{data}", data)
    return {"status": "ok"}, 202

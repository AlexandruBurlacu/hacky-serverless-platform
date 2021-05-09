import typing as t

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from kvdb import KVDB

import datetime
import requests
import logging

import json

app = FastAPI()

db = KVDB("/tmp/kvdb")

logger = logging.getLogger("uvicorn.access")

class WebHookRegistration(BaseModel):
    user_email: str
    url: str
    registration_name: str


@app.get("/status")
async def root():
    return {"status": "up"}


@app.get("/trigger-event")
async def root():
    for key in db.list_keys():
        wh_reg = db.get(key)
        logger.info(f"Sending event to {wh_reg['url']}")
        requests.post(wh_reg['url'], data=json.dumps({"event": "triggered", "time": f"{datetime.datetime.now()}"}))
    return {"status": "fired"}


@app.post("/register-webhook")
async def register(registration: WebHookRegistration):
    key = f"{registration.user_email}:{registration.registration_name}"
    value = jsonable_encoder(registration)
    db.put(key, value)
    return {"status": "ok"}

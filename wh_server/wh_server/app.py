import typing as t

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from kvdb import KVDB

app = FastAPI()

db = KVDB("/tmp/kvdb")

class WebHookRegistration(BaseModel):
    user_email: str
    url: str
    registration_name: str


@app.get("/status")
async def root():
    return {"status": "up"}


@app.get("/trigger-event")
async def root():
    return {"status": "fired"}


@app.post("/register-webhook")
async def register(registration: WebHookRegistration):
    key = f"{registration.user_email}:{registration.registration_name}"
    value = jsonable_encoder(registration)
    db.put(key, value)
    return {"status": "ok"}

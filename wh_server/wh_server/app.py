import typing as t

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from kvdb import KVDBClient

import datetime
import requests
import logging

import json

app = FastAPI()

db = KVDBClient() # has to be a TCP client


class WebHookRegistration(BaseModel):
    user_email: str
    url: str
    registration_name: str


@app.get("/status") # healhcheck
async def root():
    return {"status": "up"}


@app.get("/trigger-event") # not-CRUD
async def event_trigger():
    for key in db.list_keys():
        wh_reg = db.get(key)
        requests.post(wh_reg['url'], data=json.dumps({"event": "triggered", "time": f"{datetime.datetime.now()}"}))
    return {"status": "fired"}


@app.get("/webhooks") # Read(All)
async def event_trigger():
    return {"registrations": [{"key": key, "value": db.get(key)} for key in db.list_keys()]}


@app.get("/webhooks/:key") # Read(One)
async def event_trigger(key: str):
    return {"registration": {"key": key, "value": db.get(key)}}


@app.delete("/webhooks/:key") # Delete
async def event_trigger(key: str):
    resp = {"status": "deleted", "deleted_entry": {"key": key, "value": db.get(key)}}
    db.delete(key)
    return resp


@app.post("/webhooks") # Create
async def register(registration: WebHookRegistration):
    key = f"{registration.user_email}:{registration.registration_name}"
    value = jsonable_encoder(registration)
    db.put(key, value)
    return {"status": "ok"}

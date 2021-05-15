import docker
import pathlib
import uuid
import time

import os

import typing as t

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from kvdb import KVDBClient

app = FastAPI()
docker_client = docker.from_env()
kvdb_client = KVDBClient()


FUNCTION_STORAGE_DIR = pathlib.Path(os.environ.get("FUNCS_STORAGE_DIR_HOST", "/tmp/func-temp-storage"))
FUNCTION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

MODULE_CACHE_DIR = "/home/alexburlacu/Experiments/serverless/function_server/builder/site-packages/"


class CodeSubmission(BaseModel):
    event_type: str
    code: str


class Event(BaseModel):
    input_data: str
    event_type: str


@app.post("/submit-serverless")
def submit_serverless(code_submission: CodeSubmission):
    tempdir_name = uuid.uuid4()
    function_location_host = FUNCTION_STORAGE_DIR / pathlib.Path(str(tempdir_name) + "-func.py")
    function_location_host.write_text(code_submission.code)
    # also save the event type
    kvdb_client.put(f"{code_submission.event_type}:{tempdir_name}", function_location_host.as_posix())

    return {"status": "ok"}


@app.get("/get-serverless-instance/:cid")
def get_serverless(cid: str):
    return docker_client.containers.get(cid) # it works, all good, just make it reacher


@app.post("/trigger-serverless")
def run_serverless(event: Event):
    container_refs = []
    for serverless_id in kvdb_client.list_only(f"{event.event_type}:*"):
        tempdir_name = serverless_id.split(":")[1]
        setup_string = f"export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;"
        container_name = "python:3.6-alpine"

        function_location_host = kvdb_client.get(serverless_id)

        volumes={
            function_location_host: {"bind": f"/tmp/{tempdir_name}/function.py", "mode": "ro"},
            MODULE_CACHE_DIR: {"bind": f"/tmp/{tempdir_name}/site-packages", "mode": "ro"}
        }

        resource_constraints = {"cpu_shares": 2, "mem_limit": "256mb", "pids_limit": 10}

        command = f"sh -c '{setup_string} python /tmp/{tempdir_name}/function.py'"
        container_ref = docker_client.containers.run(container_name, command,
                                            remove=True, volumes=volumes,
                                            environment=[f"INPUT_DATA={event.input_data}"],
                                            detach=True, stderr=True, stdout=True,
                                            **resource_constraints)
        container_refs.append(container_ref.id)

    return {"status": "success", "ids": container_refs}


# docker run
#   -v $PWD/function_server/spike/function.py:/tmp/{tempdir_name}/function.py
#   -v $PWD/.venv/lib/python3.6/site-packages/:/tmp/{tempdir_name}/site-packages
#   --rm
#   python:3.6-alpine sh -c 'export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;
#                            python /tmp/{tempdir_name}/function.py'
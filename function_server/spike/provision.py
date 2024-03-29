import docker
import pathlib
import uuid
import hashlib
import time
import os
import json
from typing import Optional

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from kvdb import KVDBClient

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

docker_client = docker.from_env()
kvdb_client = KVDBClient()


FUNCTION_STORAGE_DIR = pathlib.Path(os.environ.get("FUNCS_STORAGE_DIR_HOST", "/tmp/func-temp-storage"))
FUNCTION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

FUNCTION_OUTPUTS_DIR = pathlib.Path(os.environ.get("FUNCS_OUTPUTS_DIR_HOST", "/tmp/func-temp-out"))
FUNCTION_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

MODULE_CACHE_DIR = "/home/alexburlacu/Experiments/serverless/function_server/builder/site-packages/"


class CodeSubmission(BaseModel):
    event_type: str
    code: str


class Event(BaseModel):
    input_data: str
    event_type: str


@app.get("/serverless")
def get_by_event_type_serverless_submissions(event_type: Optional[str] = None):
    if event_type:
        keys = kvdb_client.list_only(predicate=f"{event_type}:*")
    else:
        keys = kvdb_client.list_keys()
    return {"status": "ok", "serverless_ids": keys}


@app.get("/serverless/{serverless_id}")
def get_serverless_submission_summary(serverless_id: str = Path(...)):
    # also save the event type
    function_location_host = kvdb_client.get(serverless_id)
    code = pathlib.Path(function_location_host).read_text()

    return {"status": "ok", "serverless": {"event_type": serverless_id.split(":")[0], "code": code}}


@app.delete("/serverless/{serverless_id}")
def delete_serverless_submission(serverless_id: str = Path(...)):
    # also save the event type
    kvdb_client.delete(serverless_id)
    return {"status": "ok", "removed_serverless_id": serverless_id}, 202



@app.post("/serverless")
def submit_serverless_code(code_submission: CodeSubmission):
    tempdir_name = uuid.uuid4()
    function_location_host = FUNCTION_STORAGE_DIR / pathlib.Path(str(tempdir_name) + "-func.py")
    function_location_host.write_text(code_submission.code)
    # also save the event type
    serverless_id = f"{code_submission.event_type}:{tempdir_name}"
    kvdb_client.put(serverless_id, function_location_host.as_posix())

    return {"status": "ok", "serverless_id": serverless_id}, 201


###############################################################


@app.get("/serverless/instance/{instance_id}/logs")
def get_serverless_instance_logs(instance_id: str = Path(...)):
    function_logs_dir = os.path.join(FUNCTION_OUTPUTS_DIR, instance_id, "logs")
    out = pathlib.Path(function_logs_dir) / "out.log"
    err = pathlib.Path(function_logs_dir) / "err.log"
    return {"outputs": out.read_text(), "stderr": err.read_text()}


@app.post("/serverless/instance")
def run_serverless_instance_on_event(event: Event):
    instance_refs = []
    for serverless_id in kvdb_client.list_only(f"{event.event_type}:*"):
        tempdir_name = serverless_id.split(":")[1]
        setup_string = f"export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;"
        container_name = "python:3.6-alpine"

        function_location_host = kvdb_client.get(serverless_id)


        unique_name = hashlib.sha1(f"{tempdir_name}:{time.time()}".encode()).hexdigest()
        function_logs_dir = os.path.join(FUNCTION_OUTPUTS_DIR, unique_name, "logs")
        os.makedirs(function_logs_dir, exist_ok=True)

        volumes={
            function_location_host: {"bind": f"/tmp/{tempdir_name}/function.py", "mode": "ro"},
            MODULE_CACHE_DIR: {"bind": f"/tmp/{tempdir_name}/site-packages", "mode": "ro"},
            function_logs_dir: {"bind": f"/tmp/{tempdir_name}/logs"}
        }

        resource_constraints = {"cpu_shares": 2, "mem_limit": "256mb", "pids_limit": 10}

        log_config = docker.types.LogConfig(type=docker.types.LogConfig.types.JSON, config={
                                              'max-size': '1g',
                                              'labels': 'production_status,geo'
                                            })
        # hc = client.create_host_config(log_config=lc)

        command = f"sh -c '{setup_string} python -u /tmp/{tempdir_name}/function.py > /tmp/{tempdir_name}/logs/out.log 2>> /tmp/{tempdir_name}/logs/err.log'"
        container_ref = docker_client.containers.run(container_name, command, network="cloud_net",
                                            remove=True, volumes=volumes, name=unique_name,
                                            environment=[f"INPUT_DATA={event.input_data}"],
                                            detach=True, stderr=True, stdout=True, log_config=log_config,
                                            **resource_constraints)
        instance_refs.append(unique_name)

    return {"status": "success", "instance_ids": instance_refs}


# docker run
#   -v $PWD/function_server/spike/function.py:/tmp/{tempdir_name}/function.py
#   -v $PWD/.venv/lib/python3.6/site-packages/:/tmp/{tempdir_name}/site-packages
#   --rm
#   python:3.6-alpine sh -c 'export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;
#                            python /tmp/{tempdir_name}/function.py'
import docker
import pathlib
import uuid
import time

import os

import typing as t

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()
client = docker.from_env()


FUNCTION_STORAGE_DIR = pathlib.Path(os.environ.get("FUNCS_STORAGE_DIR_HOST", "/tmp/func-temp-storage"))
FUNCTION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

MODULE_CACHE_DIR = "/home/alexburlacu/Experiments/serverless/function_server/builder/site-packages/"


class CodeSubmission(BaseModel):
    input_data: str
    code: str


@app.post("/run-serverless")
def run_serverless(code_submission: CodeSubmission):
    tempdir_name = uuid.uuid4()
    setup_string = f"export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;"
    container_name = "python:3.6-alpine"

    function_location_host = FUNCTION_STORAGE_DIR / pathlib.Path(str(tempdir_name) + "-func.py")
    function_location_host.write_text(code_submission.code)

    volumes={
        function_location_host.as_posix(): {"bind": f"/tmp/{tempdir_name}/function.py", "mode": "ro"},
        MODULE_CACHE_DIR: {"bind": f"/tmp/{tempdir_name}/site-packages", "mode": "ro"}
        }

    resource_constraints = {"cpu_shares": 2, "mem_limit": "256mb", "pids_limit": 10}

    command = f"sh -c '{setup_string} python /tmp/{tempdir_name}/function.py'"
    container_logs = client.containers.run(container_name, command,
                                        remove=True, volumes=volumes,
                                        environment=[f"INPUT_DATA={code_submission.input_data}"],
                                        detach=False, stderr=True, stdout=True,
                                        **resource_constraints)

    function_location_host.unlink()

    return {"status": "success", "logs": container_logs}


# docker run
#   -v $PWD/function_server/spike/function.py:/tmp/{tempdir_name}/function.py
#   -v $PWD/.venv/lib/python3.6/site-packages/:/tmp/{tempdir_name}/site-packages
#   --rm
#   python:3.6-alpine sh -c 'export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;
#                            python /tmp/{tempdir_name}/function.py'
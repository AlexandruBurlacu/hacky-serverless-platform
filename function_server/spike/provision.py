import docker

import uuid
import time

client = docker.from_env()

tempdir_name = uuid.uuid4()
setup_string = f"export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;"
container_name = "python:3.6-alpine"

volumes={
    "/home/alexburlacu/Experiments/serverless/function_server/spike/function.py": {"bind": f"/tmp/{tempdir_name}/function.py", "mode": "ro"},
    "/home/alexburlacu/Experiments/serverless/.venv/lib/python3.6/site-packages/": {"bind": f"/tmp/{tempdir_name}/site-packages", "mode": "ro"}
    }


resource_constraints = {"cpu_shares": 2, "mem_limit": "256mb", "pids_limit": 10}

def run_container():
    # https://docker-py.readthedocs.io/en/stable/containers.html
    container = client.containers.run(container_name, f"sh -c '{setup_string} python /tmp/{tempdir_name}/function.py'", remove=True,
                                volumes=volumes, detach=False, stderr=True, stdout=True, **resource_constraints)
    # container.stop(timeout=60)
    return container


# start = time.time()
# for _ in range(10):
#     run_container()

# end = time.time()

# print(f"10 container instantiations took {end-start} seconds, which is on avg {(end-start)/10} seconds per iteration")


start = time.time()
print(run_container())
took = time.time() - start

print(took)

# docker run
#   -v $PWD/function_server/spike/function.py:/tmp/{tempdir_name}/function.py
#   -v $PWD/.venv/lib/python3.6/site-packages/:/tmp/{tempdir_name}/site-packages
#   --rm
#   python:3.6-alpine sh -c 'export PYTHONPATH=$PYTHONPATH:/tmp/{tempdir_name}/site-packages;
#                            python /tmp/{tempdir_name}/function.py'
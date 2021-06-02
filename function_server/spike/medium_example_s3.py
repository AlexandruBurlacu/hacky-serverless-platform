import boto3
from botocore.client import Config

import os
import json
import socket

# {"user": "minio", "pswd": "minio123", "bucket": "anotherone", "content": "Hop hei la la lei"}
config = json.loads(os.environ.get("INPUT_DATA"))

s3 = boto3.resource('s3',
                    endpoint_url=f"http://{socket.gethostbyname('object_storage')}:9000",
                    aws_access_key_id=config["user"],
                    aws_secret_access_key=config["pswd"],
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

try:
  s3.create_bucket(Bucket=config["bucket"])
except Exception as ex:
  print(ex, flush=True, out=os.sys.stderr)

with open('/tmp/sample.txt', "w+") as fptr:
    fptr.write(config["content"])


s3.Bucket(config["bucket"]).upload_file('/tmp/sample.txt', 'sample.txt')

s3.Bucket(config["bucket"]).download_file('sample.txt', '/tmp/new_sample.txt')

with open('/tmp/new_sample.txt') as fptr:
    print(fptr.read())




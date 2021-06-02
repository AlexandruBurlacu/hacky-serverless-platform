import pika
import boto3
from botocore.client import Config

import os
import json
import socket

import pprint
import requests

# {"user": "minio", "pswd": "minio123", "bucket": "anotherone", "url": "https://www.rabbitmq.com/tutorials/tutorial-one-python.html"}
# HEADERS: list
# corr_id: uuid
config = json.loads(os.environ.get("INPUT_DATA"))

pprint.pprint(config)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='message_queue'))
channel = connection.channel()
channel.queue_declare(queue=config["corr_id"])

s3 = boto3.resource('s3',
                    endpoint_url=f"http://{socket.gethostbyname('object_storage')}:9000",
                    aws_access_key_id=config["body"]["user"],
                    aws_secret_access_key=config["body"]["pswd"],
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

try:
  s3.create_bucket(Bucket=config["body"]["bucket"])
except Exception as ex:
  pprint.pprint(ex, stream=os.sys.stderr)

resp = requests.get(config["body"]["url"])

with open('/tmp/sample.txt', "w+") as fptr:
    fptr.write(resp.content.decode())


s3.Bucket(config["body"]["bucket"]).upload_file('/tmp/sample.txt', 'sample.txt')

s3.Bucket(config["body"]["bucket"]).download_file('sample.txt', '/tmp/new_sample.txt')

with open('/tmp/new_sample.txt') as fptr:
    body = fptr.read()



channel.basic_publish(exchange='', routing_key=config["corr_id"], body=body)
print(f"[x] Sent {body}")
connection.close()

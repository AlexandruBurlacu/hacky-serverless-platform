# import requests
import pprint
import time
import os

input_data = os.environ.get("INPUT_DATA")

# print(requests.get("https://www.reddit.com/r/MachineLearning/comments/ncdy6m/r_google_replaces_bert_selfattention_with_fourier.json").json())
while True:
    print("Say something")
    print(f"{input_data}")
    time.sleep(2)

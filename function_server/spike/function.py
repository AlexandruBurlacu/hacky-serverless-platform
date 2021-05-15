import requests
import pprint

print(requests.get("https://www.reddit.com/r/MachineLearning/comments/ncdy6m/r_google_replaces_bert_selfattention_with_fourier.json").json())
print("Say something")

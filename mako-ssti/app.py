from flask import Flask, request
from mako.template import Template

import sys
def hook(evt,arg):
    if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__"]:
        return
    frame = sys._getframe(0)
    f = frame.f_code.co_filename
    
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        
        func_name = frame.f_code.co_name
        if frame.f_code.co_filename == f:
            if func_name == "index":
                if evt not in ['open','builtins.id','compile','exec']:
                    # print(evt)
                    raise RuntimeError('Event not allowed')
                
sys.addaudithook(hook)

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get('name', 'guest')
    if name == None:
        return Template("Hello").render()
    t = Template(name)
    return t.render()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
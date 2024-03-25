from flask import Flask, request
import subprocess, sys
import os 

def hook(evt, arg):
    if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__"]:
        return
    print(evt)
    frame = sys._getframe(0)
    f = frame.f_code.co_filename
    
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        
        try:
            class_name = frame.f_locals['self'].__class__.__name__
        except KeyError:
            class_name = None
        
        func_name = frame.f_code.co_name
        if frame.f_code.co_filename == f:

            if class_name == None:
                if func_name == "hello_world":
                    if evt not in ['fcntl.fcntl', 'sys._getframe', 'open', 'os.posix_spawn', 'subprocess.Popen']:
                        raise RuntimeError('Event not allowed')

sys.addaudithook(hook)
app = Flask(__name__)
@app.route("/")
def hello_world():
    hostname = request.args.get('hostname')
    if hostname is None:
        return "No hostname provided"
    user_input = "cat /etc/passwd" # value supplied by user
    subprocess.run(["bash", "-c", user_input], shell=True)
    return subprocess.check_output(hostname, shell=True)

if __name__ == '__main__':
    app.debug = False
    app.run()
from flask import Flask, request
from jinja2 import Template
import base64, pickle

import os, sys, subprocess
import syslog

import sys, time
ignored_events = ["sys._getframe", "cpython.PyInterpreterState_Clear", "cpython.PyInterpreterState_New", 
                  "cpython._PySys_ClearAuditHooks", "cpython.run_command", "cpython.run_file", 
                  "cpython.run_interactivehook", "cpython.run_module", "cpython.run_startup", 
                  "cpython.run_stdin", "ctypes.addressof", "ctypes.call_function", "ctypes.cdata", 
                  "ctypes.cdata/buffer", "ctypes.create_string_buffer", "ctypes.create_unicode_buffer", 
                  "ctypes.dlopen", "ctypes.dlsym", "ctypes.dlsym/handle", "ctypes.get_errno", "ctypes.get_last_error", 
                  "ctypes.seh_exception", "ctypes.set_errno", "ctypes.set_last_error", "ctypes.string_at", 
                  "ctypes.wstring_at", "ensurepip.bootstrap", "msvcrt.get_osfhandle", "msvcrt.locking", 
                  "msvcrt.open_osfhandle", "object.__delattr__", "object.__getattr__", "object.__setattr__", 
                  "winreg.ConnectRegistry", "winreg.CreateKey", "winreg.DeleteKey", "winreg.DeleteValue", 
                  "winreg.DisableReflectionKey", "winreg.EnableReflectionKey", "winreg.EnumKey", 
                  "winreg.EnumValue", "winreg.ExpandEnvironmentStrings", "winreg.LoadKey", "winreg.OpenKey", 
                  "winreg.OpenKey/result", "winreg.PyHKEY.Detach", "winreg.QueryInfoKey", "winreg.QueryReflectionKey", 
                  "winreg.QueryValue", "winreg.SaveKey", "winreg.SetValue"]

def hook(evt, arg):
    start_time = time.time()
    if evt in ignored_events:
        return
    # pass
    try:
        frame = sys._getframe(0)
    except ValueError:
        return

    f = frame.f_code.co_filename
    # print(f"event {evt} in {frame.f_code.co_filename}")
    # print(f"\n{datetime.fromtimestamp(datetime.now().timestamp())} {evt} {frame.f_code.co_name}\n")
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        func_name = frame.f_code.co_name
        # print(f"{datetime.fromtimestamp(datetime.now().timestamp())} {evt} {func_name}\n")
        if func_name == "ssti":
            if evt not in ['open']:
                raise RuntimeError('Event not allowed')

        if func_name == "peko":
            # print(f"{datetime.fromtimestamp(datetime.now().timestamp())} {evt} {func_name}\n")
            if evt not in ['pickle.find_class', 'sys._getframe']:
                raise RuntimeError('Event not allowed')

        if func_name == "evt_test":
            if evt not in ['os.system', 'sys._getframe', 'subprocess.Popen', 'os.posix_spawn', 'fcntl.fcntl', 'syslog.syslog', 'builtins.id', 'open']:
                raise RuntimeError('Event not allowed')
        # if "app.py" in frame.f_code.co_filename:
        #     if func_name == "evt_test":
        #         if evt not in ["syslog.syslog", "syslog.openlog", "os.system", "open", "subprocess.Popen", "builtins.id"]:
        #             raise RuntimeError('Event not allowed')
        #     if func_name == "ssti":
        #         if evt not in ["compile", "exec"]:
        #             raise RuntimeError('Event not allowed')
        #     if func_name == "peko":
        #         if evt not in ["pickle.find_class"]:
        #             raise RuntimeError('Event not allowed')

        # print(f"---- using {time.time() - start_time}s----") 

sys.addaudithook(hook)

app = Flask(__name__)

@app.route("/")
def index():
    return "hello"

@app.route("/ssti")
def ssti():
    name = request.args.get('name', 'guest')

    t = Template("Hello " + name)
    return t.render()

@app.route("/peko", methods=["POST"])
def peko():
    data = base64.urlsafe_b64decode(request.form['pickled'])
    deserialized = pickle.loads(data)
    for i in deserialized:
        os.system(i)
    return "Wat"

@app.route("/many")
def evt_test():
    syslog.syslog('Running performance test.')
    os.system("id")
    test = subprocess.check_output("id")
    id(test)
    os.system("id")
    test = subprocess.check_output("id")
    id(test)
    os.system("id")
    test = subprocess.check_output("id")

    return "Audit events test ok."

if __name__ == "__main__":
    app.run(host='0.0.0.0')
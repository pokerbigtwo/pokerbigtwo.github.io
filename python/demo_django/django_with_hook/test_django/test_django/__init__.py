import sys
from datetime import datetime 
file=open("event.log","w")
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
                  "winreg.QueryValue", "winreg.SaveKey", "winreg.SetValue","pathlib.Path.glob"]

def hook(evt, arg):
    if evt in ignored_events:
        return
    # pass
    try:
        frame = sys._getframe(0)
    except ValueError:
        return

    f = frame.f_code.co_filename
    # file.write(f"\n{datetime.fromtimestamp(datetime.now().timestamp())} {evt} from {frame.f_code.co_name} in {frame.f_code.co_filename}\n")
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        func_name = frame.f_code.co_name
        if frame.f_code.co_filename=="/test/py_sandbox/py_sandbox-main/testcase/django/test_django/test_audit/views.py":
            # file.write(f"{datetime.fromtimestamp(datetime.now().timestamp())} {evt} from {func_name} in {frame.f_code.co_filename}\n")
            if func_name == "index":
                if evt not in ['marshal.loads', 'open']:
                    print(evt)
                    raise RuntimeError('Event not allowed')

            if func_name == "ssti":
                if evt not in ['marshal.loads', 'open']:
                    print(evt)
                    raise RuntimeError('Event not allowed')

            if func_name == "peko":
                if evt not in ['marshal.loads', 'sys._getframe', 'open', 'pickle.find_class']:
                    print(evt)
                    raise RuntimeError('Event not allowed')

            if func_name == "evt_test":
                if evt not in ['builtins.id', 'subprocess.Popen', 'marshal.loads', 'fcntl.fcntl', 'os.posix_spawn', 'sys._getframe', 'open', 'syslog.syslog']:
                    print(evt)
                    raise RuntimeError('Event not allowed')
        # if "view" in frame.f_code.co_filename or "manage.py" in frame.f_code.co_filename or "urls.py" in frame.f_code.co_filename or "wsgi.py" in frame.f_code.co_filename:
        #   print(f"event {evt} from {func_name} in {frame.f_code.co_filename}")
        #     if func_name == "evt_test":
        #         # print(f"event {evt} from {func_name} in {frame.f_code.co_filename}")
        #         if evt not in ["syslog.syslog", "syslog.openlog", "os.system", "open", "subprocess.Popen", "builtins.id"]:
        #             raise RuntimeError('Event not allowed')
        #         break
        #     if func_name == "ssti":
        #         # print(f"event {evt} from {func_name} in {frame.f_code.co_filename}")
        #         if evt not in ["compile", "exec", "open", "marshal.loads"]:
        #             # print(f"event {evt} from {func_name} in {frame.f_code.co_filename}")
        #             raise RuntimeError('Event not allowed')
        #         break
            # elif func_name != "<module>":
            #     raise RuntimeError('Event not allowed')

sys.addaudithook(hook)
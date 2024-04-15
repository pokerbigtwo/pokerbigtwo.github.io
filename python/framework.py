import sys

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

# framework of hook
def hook(evt, arg):
    if evt in ignored_events:
        return

    try:
        frame = sys._getframe(0)
    except ValueError:
        return

    f = frame.f_code.co_filename
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        func_name = frame.f_code.co_name
        if frame.f_code.co_filename == f:
            # 放該檢查的部分的 code
            # if func_name == "function name":
            #   if evt not in ["allow list"]:
            #       print("Weird Detect !")    
            print(f"{evt} and {arg} by function {func_name}")
            break
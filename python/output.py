
import sys

def hook(evt, arg):
    if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__"]:
        return
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

            if class_name == "FlaskClient":
                if func_name == "open":
                    if evt not in ['builtins.id']:
                        raise RuntimeError('Event not allowed')


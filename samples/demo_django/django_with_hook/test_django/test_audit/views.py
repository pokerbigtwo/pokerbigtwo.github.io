# Create your views here.
from django.http import HttpResponse
from django.template import engines
import base64, pickle
import os, sys, subprocess
import syslog

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

            if class_name == None:
                if func_name == "index":
                    if evt not in ['marshal.loads', 'open']:
                        raise RuntimeError('Event not allowed')

            if class_name == None:
                if func_name == "ssti":
                    if evt not in ['marshal.loads', 'open']:
                        raise RuntimeError('Event not allowed')

            if class_name == None:
                if func_name == "peko":
                    if evt not in ['marshal.loads', 'open', 'pickle.find_class', 'sys._getframe']:
                        raise RuntimeError('Event not allowed')

            if class_name == None:
                if func_name == "evt_test":
                    if evt not in ['syslog.openlog', 'builtins.id', 'open', 'os.posix_spawn', 'syslog.syslog', 'fcntl.fcntl', 'subprocess.Popen', 'marshal.loads', 'sys._getframe']:
                        raise RuntimeError('Event not allowed')

sys.addaudithook(hook)

def index(request):
    return HttpResponse("hello")

def ssti(request):
    name = request.GET.get('name', 'guest')
    engine = engines["django"]
    template = engine.from_string("Hello" + name + "!")
    return HttpResponse(template.render({}, request))

def peko(request):
    data = base64.urlsafe_b64decode(request.POST.get('pickled'))
    deserialized = pickle.loads(data)
    return HttpResponse("Wat")

def evt_test(request):
    syslog.syslog('Running performance test.')
    # os.system("id")
    test = subprocess.check_output("id")
    id(test)
    # os.system("id")
    test = subprocess.check_output("id")
    id(test)
    # os.system("id")
    test = subprocess.check_output("id")
    return HttpResponse("Audit events test ok.")
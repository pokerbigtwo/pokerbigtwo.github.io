# Create your views here.
from django.http import HttpResponse
from django.template import engines
import base64, pickle
import os, sys, subprocess
import syslog

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
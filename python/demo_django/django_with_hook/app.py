from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import base64
import pickle

import os
import sys
import subprocess
import syslog

from django.urls import path

def index(request):
    return HttpResponse("hello")

def ssti(request):
    name = request.GET.get('name', 'guest')
    template = Template("Hello {{ name }}")
    context = Context({'name': name})
    output = template.render(context)
    return HttpResponse(output)

@csrf_exempt
def peko(request):
    data = base64.urlsafe_b64decode(request.POST.get('pickled', ''))
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

urlpatterns = [
    path("", index),
    path("ssti", ssti),
    path("peko", peko),
    path("many", evt_test),
]
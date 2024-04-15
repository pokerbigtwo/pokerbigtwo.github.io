from flask import Flask, request
from jinja2 import Template
import base64, pickle

import os, sys, subprocess
import syslog

import sys, time

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
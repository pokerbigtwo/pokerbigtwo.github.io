from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from mako.template import Template
import base64, pickle
import subprocess
import syslog, os


def index(request):
    return Response('hello')

def ssti(request):
    name = request.params.get('name', 'guest')
    template = Template("Hello %s" % name)
    rendered = template.render(name="guest")
    return Response(rendered)


def peko(request):
    data = base64.urlsafe_b64decode(request.params['pickled'])
    deserialized = pickle.loads(data)
    for i in deserialized:
        os.system(i)
    return Response('Wat')


def evt_test(request):
    syslog.syslog('Running performance test.')
    os.system("id")
    test = subprocess.check_output("id")
    id(test)
    os.system("id")
    test = subprocess.check_output("id")
    id(test)
    os.system("id")
    test = subprocess.check_output("id")
    return Response('Audit events test ok.')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_view(index, route_name='index')
        config.add_route('ssti', '/ssti')
        config.add_view(ssti, route_name='ssti')
        config.add_route('peko', '/peko', request_method='POST')
        config.add_view(peko, route_name='peko')
        config.add_route('evt_test', '/many')
        config.add_view(evt_test, route_name='evt_test')
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 8080, app)
    print("Running Pyramid app on http://0.0.0.0:8080")

    from app_hook import hook
    import sys
    sys.addaudithook(hook)

    server.serve_forever()

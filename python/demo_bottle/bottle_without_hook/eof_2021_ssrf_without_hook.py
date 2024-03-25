from bottle import default_app, get, run, request, response, template

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

import sys, traceback
# from datetime import datetime  
secret = "cCySMEDJ9LOlStFzu-k9HE0XUZIkGlGqMkDOBHOldXI"
# file=open("event.log","w")

# def hook(evt, arg):
#     if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__","os.utime"]:
#         return
#     frame = sys._getframe(0)
#     f = frame.f_code.co_filename
#     file.write(f"\n{datetime.fromtimestamp(datetime.now().timestamp())} {evt} {frame.f_code.co_name}\n")
#     while frame:
#         if frame.f_back is None:
#             break
#         else:
#             frame = frame.f_back
        
#         func_name = frame.f_code.co_name
#         file.write(f"{datetime.fromtimestamp(datetime.now().timestamp())} {evt} {func_name}\n")


app = default_app()


@get("/")
def home():
    session = request.get_cookie('session', secret=secret)
    if not session:
        session = {"payloads": []}
        response.set_cookie('session', session, secret=secret)
    return template('index', payloads=session['payloads'])


@get("/proxy")
def proxy():
    url = request.params.url

    sess = request.get_cookie('session', secret=secret)
    sess['payloads'].append(url)
    response.set_cookie('session', sess, secret=secret)

    netloc = urlparse(url).netloc.lower()

    if netloc == '':
        response.status = 400
        response.content_type = 'text/plain'
        return "400: urlparse(url).netloc should not be empty"

    if netloc in ('localhost', '127.0.0.1', '127.0.1', '127.1', '2130706433', '0x7f000001'):
        response.status = 400
        response.content_type = 'text/plain'
        return "400: netloc should not be localhost, don't SSRF me!"

    try:
        resp = urlopen(url)
        response.content_type = resp.info().get_content_type()
        return resp.read()
    except (URLError, HTTPError) as e:
        response.status = 500
        return f"Fetch `{url}` failed: {e.reason}"


if __name__ == '__main__':
    run(host='0.0.0.0', port=9453, reloader=True)
    # file.close()
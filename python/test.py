from flask import Flask
from jinja2 import Template

app = Flask(__name__)

@app.route('/')
def index():
    T= Template('Hello!')
    return T.render()

if __name__ == '__main__':
    app.run()
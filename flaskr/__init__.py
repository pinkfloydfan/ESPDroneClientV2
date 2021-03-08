import os

from flask import Flask
from flask import render_template

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
# websocket boilerplate

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### open ###")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        print("trying to open websocket")
        ws = websocket.WebSocketApp("ws://192.168.4.22:80", on_open = on_open, on_message = on_message, on_error = on_error, on_close = on_close)
        print("websocket instance created")
        ws.run_forever()
        return render_template('index.html',title="henlo")


    return app
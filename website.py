import pandas as pd

# Bokeh basics
from bokeh.models.widgets import Tabs
from bokeh.embed import server_document
from bokeh.server.server import Server

from threading import Thread
from tornado.ioloop import IOLoop

from flask import Flask, render_template
from dashboard import _tab as dashboard_tab

app = Flask(__name__)


def make_doc(doc):
    policy_data = pd.read_csv("static/data/Auto - Policy Export.csv", low_memory=False)
    # Create each of the tabs
    tab1 = dashboard_tab(policy_data)
    TABS = Tabs(tabs=[tab1])
    # Put the tabs in the current document for display
    doc.add_root(TABS)


@app.route('/')
def template():
    return render_template("home.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/gallery")
def about():
    return render_template("gallery.html")


@app.route("/projects")
def contact():
    return render_template("projects.html")


# @app.route("/dashboard")
@app.route('/dashboard')
def dashboard():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("dashboard.html", script=script)


def bk_worker():
    server = Server({'/bkapp': make_doc}, io_loop=IOLoop(), allow_websocket_origin=["*"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:{}/'.format(5006))
    app.run(port=5000, debug=True)

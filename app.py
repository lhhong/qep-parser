from flask import Flask
from parseTree import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/plot_query_tree')
def plot_query_tree():
    return 'plot tree'

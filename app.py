from flask import Flask, request, jsonify
from parse_tree import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/plot_query_tree", methods=["POST"])
def plot_query_tree():
    data = request.get_json()
    stats, all_nodes = plotQueryTree(data["qep"])
    return jsonify(stats=stats, all_nodes=all_nodes)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

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
    stats, all_nodes, _ = plotQueryTree(data['query'], data["qep"])
    return jsonify(stats=stats, all_nodes=all_nodes)

@app.route("/plot_query_tree_from_sql", methods=["POST"])
def plot_query_tree_from_sql():
    data = request.get_json()

    try:
        conn = psycopg2.connect(host=data['host'],
                                database=data['database'],
                                user=data['user'],
                                password=data['password'])
        cur = conn.cursor()
        cur.execute('EXPLAIN(FORMAT JSON) ' + data['query'])
        result = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()

    qep = result[0][0][0]
    stats, all_nodes, _ = plotQueryTree(data['query'], qep)
    return jsonify(stats=stats, all_nodes=all_nodes)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

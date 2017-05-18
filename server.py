
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
app = Flask(__name__)
CORS(app)


if "AWSTODO_DB_CONN_STR" in os.environ:
    db_conn_str = os.environ["AWSTODO_DB_CONN_STR"]
else:
    db_conn_str = "dbname='awstodo1' user='postgres' host='127.0.0.1' password='123456'"


@app.route("/tarefas", methods=["GET"])
def get_tarefas():
    conn = psycopg2.connect(db_conn_str)
    cur = conn.cursor()
    cur.execute("""SELECT id, descricao, concluida FROM tarefas""")
    rows = cur.fetchall()
    tarefas = []
    for row in rows:
        tarefas.append({
            "id": row[0],
            "descricao": row[1],
            "concluida": row[2]
        })
    cur.close()
    conn.close()
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def nova_tarefa():
    conn = psycopg2.connect(db_conn_str)
    cur = conn.cursor()
    cur.execute("""INSERT INTO tarefas (descricao, concluida) VALUES (%s, %s)""",
                (request.form["descricao"], False))
    conn.commit()
    cur.close()
    conn.close()
    return ''


@app.route("/tarefas/<id>/concluir", methods=["POST"])
def concluir_tarefa(id):
    conn = psycopg2.connect(db_conn_str)
    cur = conn.cursor()
    cur.execute("""UPDATE tarefas SET concluida = %s WHERE id = %s""",
                (True, id))
    conn.commit()
    cur.close()
    conn.close()
    return ''


if __name__ == "__main__":
    app.run(host="0.0.0.0")

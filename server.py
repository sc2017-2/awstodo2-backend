
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

tarefas = [
    { "id": 1, "descricao": "Comprar pão", "concluida": True },
    { "id": 2, "descricao": "Ler e-mails", "concluida": False }
]


@app.route("/tarefas", methods=["GET"])
def get_tarefas():
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def nova_tarefa():
    global tarefas
    tarefa = {
        "id": max(map(lambda x: x["id"], tarefas)) + 1,
        "descricao": request.form["descricao"],
        "concluida": False
    }
    tarefas.append(tarefa)
    return ''


@app.route("/tarefas/<id>/concluir", methods=["POST"])
def concluir_tarefa(id):
    global tarefas
    for tarefa in filter(lambda x: x["id"] == int(id), tarefas):
        tarefa["concluida"] = True
    return ''


if __name__ == "__main__":
    app.run(host="0.0.0.0")

from flask import Blueprint, render_template, request, jsonify

from app.ai.chef_ai import gerar_resposta

main = Blueprint("main", __name__)


@main.route("/")
def home():

    return render_template("index.html")


@main.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    mensagem = data.get("message")

    resposta = gerar_resposta(mensagem)

    return jsonify({
        "response": resposta
    })
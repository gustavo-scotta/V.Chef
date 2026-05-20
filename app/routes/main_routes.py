from flask import Blueprint, render_template, request, jsonify
from app.ai.chef_ai import gerar_resposta

main = Blueprint("main", __name__)

preferencias_usuario = [
    "Comida italiana",
    "Receitas rápidas",
    "Sobremesas"
]


@main.route("/")
def home():

    return render_template(
        "home.html",
        usuario="Fabio"
    )

@main.route("/mensagem", methods=["POST"])
def mensagem():

    dados = request.get_json()
    texto = dados["mensagem"]

    resposta = gerar_resposta(
        texto,
        ingredientes=None,
        preferencias=preferencias_usuario
    )

    return jsonify({
        "resposta": resposta
    })

@main.route("/despensa")
def despensa():
    return render_template(
        "despensa.html"
    )

@main.route("/preferencias")
def preferencias():
    return render_template(
        "preferencias.html"
    )
from flask import Blueprint, render_template, jsonify, request
from app.models.despensa import DespensaModel

# Criamos um Blueprint específico para a despensa
despensa_bp = Blueprint("despensa", __name__)

@despensa_bp.route("/despensa")
def despensa_view():
    return render_template("despensa.html")

@despensa_bp.route("/api/despensa", methods=["GET"])
def listar_despensa():
    # O Controller interage com o Model pedindo os dados
    ingredientes = DespensaModel.obtem_ingredientes_despensa()

    resposta = []
    for item in ingredientes:
        resposta.append({
            "id": item[0],
            "nome": item[1],
            "quantidade": item[2],
            "categoria": item[3],
            "unidade": item[4],
            "emoji": item[5] or "🍽️"
        })

    return jsonify(resposta)

@despensa_bp.route("/api/despensa", methods=["POST"])
def adicionar_despensa():
    dados = request.get_json()
    DespensaModel.cadastra_ingrediente_na_despensa(
        nome_ingrediente=dados["nome"],
        nome_categoria=dados["categoria"],
        unidade_medida=dados["unidade"],
        quantidade=dados["quantidade"],
        codigo_icone=dados.get("emoji", "🍽️")
    )
    return jsonify({"status": "ok"})

@despensa_bp.route("/api/despensa/<int:id>/aumentar", methods=["POST"])
def aumentar_despensa(id):
    DespensaModel.aumentar_ingrediente_despensa(id)
    return jsonify({"status": "ok"})

@despensa_bp.route("/api/despensa/<int:id>/diminuir", methods=["POST"])
def diminuir_despensa(id):
    DespensaModel.diminuir_ingrediente_despensa(id)
    return jsonify({"status": "ok"})
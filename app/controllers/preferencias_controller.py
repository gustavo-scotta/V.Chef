from flask import Blueprint, render_template, request, jsonify
from app.models.preferencia import PreferenciasModel

preferencias_bp = Blueprint("preferencias", __name__)

@preferencias_bp.route("/preferencias")
def preferencias():
    PreferenciasModel.cadastra_preferencias_padrao()

    restricoes = PreferenciasModel.lista_restricoes()
    observacoes = PreferenciasModel.lista_observacoes()
    nao_gosta = PreferenciasModel.lista_nao_gosta()

    return render_template(
        "preferencias.html",
        restricoes=restricoes,
        observacoes=observacoes,
        nao_gosta=nao_gosta
    )

@preferencias_bp.route("/preferencias/salvar", methods=["POST"])
def salvar_preferencias():
    dados = request.get_json()

    PreferenciasModel.salvar_preferencias(
        nao_gosta=dados.get("nao_gosta", []),
        restricoes=dados.get("restricoes", []),
        observacoes=dados.get("observacoes", [])
    )

    return jsonify({
        "status": "ok"
    })
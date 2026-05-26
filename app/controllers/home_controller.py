from flask import Blueprint, render_template, request, jsonify
from app.ai.chef_ai import gerar_resposta # Ajuste o caminho do import da sua IA se necessário
from app.models.despensa import DespensaModel
from app.models.preferencia import PreferenciasModel # Usando os nomes exatos dos seus arquivos!

home_bp = Blueprint("home", __name__, template_folder='../templates')

@home_bp.route("/")
def home():
    return render_template(
        "home.html",
        usuario="Fábio"
    )

@home_bp.route("/mensagem", methods=["POST"])
def mensagem():
    try:
        dados = request.get_json()
        texto = dados["mensagem"]

        # Busca os dados usando os novos Models
        ingredientes_despensa = DespensaModel.obtem_ingredientes_despensa()
        preferencias_usuario = PreferenciasModel.obtem_preferencias_ativas()
        nao_gosta = [item["nome"] for item in PreferenciasModel.lista_nao_gosta()]

        print("Preferências ativas:", preferencias_usuario)
        print("Não gosta:", nao_gosta)

        # IA recebe os ingredientes da despensa
        resposta = gerar_resposta(
            texto,
            ingredientes=ingredientes_despensa,
            preferencias=preferencias_usuario,
            nao_gosta=nao_gosta
        )

        return jsonify({
            "resposta": resposta
        })

    except Exception as e:
        print("Erro:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
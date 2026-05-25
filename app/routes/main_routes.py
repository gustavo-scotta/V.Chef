from flask import Blueprint, render_template, request, jsonify
from app.ai.chef_ai import gerar_resposta
from app.database import banco

main = Blueprint("main", __name__)

""" ROTAS HOME"""
@main.route("/")
def home():

    return render_template(
        "home.html",
        usuario="Fábio"
    )


@main.route("/mensagem", methods=["POST"])
def mensagem():
    try:
        dados = request.get_json()
        texto = dados["mensagem"]

        # Busca os ingredientes salvos na despensa
        ingredientes_despensa = banco.obtem_ingredientes_despensa()

        # Busca preferencias true
        preferencias_usuario = banco.obtem_preferencias_ativas()

        nao_gosta = [item["nome"] for item in banco.lista_nao_gosta()]

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




""" ROTAS DESPENSA """
@main.route("/despensa")
def despensa():
    return render_template(
        "despensa.html"
    )


@main.route("/api/despensa", methods=["GET"])
def listar_despensa():
    ingredientes = banco.obtem_ingredientes_despensa()

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


@main.route("/api/despensa", methods=["POST"])
def adicionar_despensa():
    dados = request.get_json()

    banco.cadastra_ingrediente_na_despensa(
        nome_ingrediente=dados["nome"],
        nome_categoria=dados["categoria"],
        unidade_medida=dados["unidade"],
        quantidade=dados["quantidade"],
        codigo_icone=dados.get("emoji", "🍽️")
    )

    return jsonify({
        "status": "ok"
    })


@main.route("/api/despensa/<int:id>/aumentar", methods=["POST"])
def aumentar_despensa(id):
    banco.aumentar_ingrediente_despensa(id)

    return jsonify({
        "status": "ok"
    })


@main.route("/api/despensa/<int:id>/diminuir", methods=["POST"])
def diminuir_despensa(id):
    banco.diminuir_ingrediente_despensa(id)

    return jsonify({
        "status": "ok"
    })


""" ROTAS PREFERENCIAS """
@main.route("/preferencias")
def preferencias():
    banco.cadastra_preferencias_padrao()

    restricoes = banco.lista_restricoes()
    observacoes = banco.lista_observacoes()
    nao_gosta = banco.lista_nao_gosta()

    return render_template(
        "preferencias.html",
        restricoes=restricoes,
        observacoes=observacoes,
        nao_gosta=nao_gosta
    )

@main.route("/preferencias/salvar", methods=["POST"])
def salvar_preferencias():
    dados = request.get_json()

    banco.salvar_preferencias(
        nao_gosta=dados.get("nao_gosta", []),
        restricoes=dados.get("restricoes", []),
        observacoes=dados.get("observacoes", [])
    )

    return jsonify({
        "status": "ok"
    })
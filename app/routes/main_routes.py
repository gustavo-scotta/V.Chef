from flask import Blueprint, render_template, request, jsonify
from app.ai.chef_ai import gerar_resposta
from app.database import banco

main = Blueprint("main", __name__)

preferencias_usuario = [
    "Comida italiana",
    "Receitas rápidas",
    "Sobremesas"
]

""" ROTAS HOME/IA"""
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

        # IA recebe os ingredientes da despensa
        resposta = gerar_resposta(
            texto,
            ingredientes=ingredientes_despensa,
            preferencias=preferencias_usuario
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
    return render_template(
        "preferencias.html"
    )

@main.route('/preferencias/nao-gosta', methods=['POST'])
def adicionar_nao_gosta():
    dados = request.get_json()

    nome = dados.get('nome', '').strip()

    if not nome:
        return jsonify({'erro': 'Ingrediente inválido'}), 400

    id_ingrediente = banco.cadastra_nao_gosta(nome)

    return jsonify({
        'id': id_ingrediente,
        'nome': nome
    }), 201

@main.route('/preferencias/nao-gosta/<int:id_ingrediente>', methods=['DELETE'])
def remover_nao_gosta(id_ingrediente):

    banco.remove_nao_gosta(id_ingrediente)

    return jsonify({
        'status': 'ok'
    })

@main.route('/preferencias/restricao', methods=['POST'])
def adicionar_restricao():
    dados = request.get_json()

    nome = dados.get('nome', '').strip()

    if not nome:
        return jsonify({'erro': 'Restrição inválida'}), 400

    id_restricao = banco.cadastra_restricao(nome, True)

    return jsonify({
        'id': id_restricao,
        'nome': nome,
        'status': True
    }), 201

@main.route('/preferencias/restricao/status', methods=['POST'])
def alterar_status_restricao():

    dados = request.get_json()

    id_restricao = dados.get('id')
    status = dados.get('status')

    banco.altera_status_restricao(id_restricao, status)

    return jsonify({
        'id': id_restricao,
        'status': status
    })

@main.route('/preferencias/restricao/<int:id_restricao>', methods=['DELETE'])
def remover_restricao(id_restricao):
    banco.remove_restricao(id_restricao)

    return jsonify({
        'status': 'ok'
    })
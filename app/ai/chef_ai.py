import json

from google import genai
from google.genai import types

from app.ai.prompts import filtro
from app.config import API_KEY

client = genai.Client(api_key=API_KEY)


def extrair_json_array(texto):

    texto = texto.strip()

    try:
        receitas = json.loads(texto)
    except json.JSONDecodeError:
        inicio = texto.find("[")
        fim = texto.rfind("]") + 1

        if inicio == -1 or fim == 0 or fim <= inicio:
            raise

        receitas = json.loads(texto[inicio:fim])

    if not isinstance(receitas, list):
        raise ValueError("A resposta da IA nao e uma lista JSON.")

    return receitas


def gerar_conteudo(prompt, temperature=0.1):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=filtro,
            temperature=temperature,
            max_output_tokens=8000,
            response_mime_type="application/json"
        )
    )

    return response.text.strip()


def corrigir_json(texto_invalido):

    prompt_correcao = f"""
    Corrija o conteudo abaixo para JSON valido.

    Regras:
    - Retorne somente um array JSON valido.
    - Nao use markdown.
    - Nao escreva explicacoes.
    - Mantenha no maximo 3 receitas.
    - Cada receita deve ter titulo, descricao, tempo, dificuldade e modo_preparo.
    - Se um campo estiver incompleto, complete de forma curta e culinaria.

    Conteudo com erro:
    {texto_invalido}
    """

    texto_corrigido = gerar_conteudo(prompt_correcao, temperature=0)
    return extrair_json_array(texto_corrigido)


def gerar_resposta(mensagem, ingredientes=None, preferencias=None):

    mensagem_lower = mensagem.lower()
    usar_despensa = "despensa" in mensagem_lower

    contexto = ""

    if usar_despensa and ingredientes:

        ingredientes_texto = []

        for item in ingredientes:

            nome = item[1]
            quantidade = item[2]
            categoria = item[3]
            unidade = item[4]

            ingredientes_texto.append(
                f"{nome} - {quantidade} {unidade} ({categoria})"
            )

        contexto += "\nIngredientes disponiveis na despensa:\n"
        contexto += "\n".join(ingredientes_texto)

    if preferencias:

        contexto += "\n\nPreferencias do usuario:\n"
        contexto += "\n".join(preferencias)

    prompt = f"""
    {contexto}

    Pedido do usuario:
    {mensagem}

    Responda exatamente ao pedido do usuario.

    Se ele pedir receitas:
    - Gere exatamente 3 receitas.
    - Considere a despensa se o usuario pedir receitas com base na despensa.
    - Considere as preferencias do usuario sempre que elas forem informadas.
    - Use textos curtos para evitar JSON longo demais.
    - Retorne somente JSON valido.

    Formato obrigatorio:
    [
      {{
        "id": "1",
        "titulo": "Receita",
        "categoria": "Categoria",
        "tempo": "20 min",
        "dificuldade": "Facil",
        "rendimento": "2 porcoes",
        "descricao": "Descricao curta.",
        "imagem": "palavras chave",
        "ingredientes": ["ingrediente 1", "ingrediente 2"],
        "modo_preparo": ["Passo 1.", "Passo 2."],
        "dica_chef": "Dica curta.",
        "tags": ["tag1", "tag2"]
      }}
    ]

    Limites:
    - ingredientes: no maximo 7 itens por receita.
    - modo_preparo: no maximo 4 passos por receita.
    - descricao e dica_chef: uma frase curta.
    - tags: no maximo 3.

    Sem markdown.
    Sem texto extra.
    """

    texto = ""

    try:

        texto = gerar_conteudo(prompt)
        return extrair_json_array(texto)

    except Exception as primeiro_erro:

        try:
            return corrigir_json(texto)
        except Exception as segundo_erro:

            print("ERRO JSON:")
            print(f"Erro inicial: {primeiro_erro}")
            print(f"Erro ao corrigir: {segundo_erro}")
            print("Resposta recebida:")
            print(texto[:2000])

            return [
                {
                    "titulo": "Erro ao gerar receita"
                }
            ]

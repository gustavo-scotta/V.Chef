import json

from google import genai
from google.genai import types

from app.ai.prompts import filtro
from app.config import API_KEY

client = genai.Client(api_key=API_KEY)


def gerar_resposta(mensagem):

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=mensagem,

        config=types.GenerateContentConfig(

            system_instruction=filtro,

            temperature=0.7,

            max_output_tokens=4000,
        )
    )

    texto = response.text.strip()

    texto = texto.replace("```json", "")
    texto = texto.replace("```", "")

    receitas = json.loads(texto)

    return receitas
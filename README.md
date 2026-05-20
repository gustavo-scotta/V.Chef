# V.Chef

O **V.Chef** é um assistente culinário inteligente que simula um chef profissional utilizando Inteligência Artificial.

O sistema permite que o usuário converse com um chef virtual e receba **4 sugestões de pratos completas**, cada uma contendo:

- Nome do prato
- Tempo de preparo
- Dificuldade
- Descrição profissional
- Modo de preparo
- Imagem ilustrativa (gerada por IA) --em andamento

---

# Tecnologias Utilizadas

## Backend
- Python 3.11+
- Flask
- Gemini API (Google AI)
- python-dotenv

## Frontend
- HTML5
- CSS3
- JavaScript

## IA de Imagens (opcional)
- Hugging Face (Stable Diffusion)
- Leonardo AI
- Outras APIs de geração de imagem

---

# Como o Sistema Funciona

1. O usuário envia uma mensagem pelo chat (frontend)  
2. O Flask recebe a requisição na rota `/chat`  
3. A mensagem é enviada para o **Gemini**  
4. A IA retorna **4 receitas em formato JSON**  
5. (Opcional) O sistema gera imagens para cada prato  
6. O frontend renderiza os pratos em **cards interativos**

---

# Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

GEMINI_API_KEY=sua_chave_aqui  
---

# Instalação

## 1. Clone o repositório

git clone URL_DO_REPOSITORIO

## 2. Acesse a pasta

cd V.CHEF

## 3. Crie o ambiente virtual

### Windows
python -m venv .venv

### Linux/Mac
python3 -m venv .venv

---

## 4. Ative o ambiente virtual

### PowerShell
.\.venv\Scripts\Activate.ps1

### CMD
.\.venv\Scripts\activate.bat

### Linux/Mac
source .venv/bin/activate

---

## 5. Instale as dependências

pip install -r requirements.txt

---

# Executando o Projeto

Execute o servidor Flask:

python run.py

---

## Acesse no navegador

http://127.0.0.1:5000

---

# Como Usar

Digite qualquer pedido culinário, por exemplo:

- "Quero receitas de lasanha"
- "Ideias para jantar romântico"
- "Receitas rápidas"

O sistema retornará **3 pratos completos em formato visual**.

---

# Regras da IA

O V.Chef foi treinado para:

✅ Responder apenas sobre culinária  
✅ Gerar exatamente 3 receitas  
✅ Usar linguagem profissional de chef  
✅ Fornecer instruções detalhadas  

---

## Bloqueios

A IA NÃO responde sobre:

- Política  
- Tecnologia  
- Esportes  
- Assuntos pessoais  
- Qualquer tema fora da culinária  

---

# 👨‍🍳 Objetivo do Projeto

Este projeto foi desenvolvido para praticar:

- Integração com IA  
- Engenharia de Prompt  
- Desenvolvimento Web (Flask)  
- Arquitetura de Software  
- Experiência do usuário  
- Integrações front end e back end

---

# Autores

Desenvolvido pelo turma 2026/1 de Engenharia de Software 

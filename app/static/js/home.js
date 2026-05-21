const botao = document.getElementById("botao-enviar");
const campoMensagem = document.getElementById("mensagem");

// variável global para guardar as receitas retornadas pela IA
let receitas = [];

botao.addEventListener("click", enviarMensagem);

campoMensagem.addEventListener("keydown", (evento) => {
  if (evento.key === "Enter") {
    evento.preventDefault();
    enviarMensagem();
  }
});

async function enviarMensagem() {
  const mensagem = campoMensagem.value;
  const areaResposta = document.getElementById("resposta-ia");

  campoMensagem.value = "";

  areaResposta.innerText = "🥘 Preparando...";

  try {
    // Envia a mensagem para a rota /mensagem do Flask
    const resposta = await fetch("/mensagem", {
      method: "POST",

      // Informa ao Flask que os dados enviados estão em formato JSON
      headers: {
        "Content-Type": "application/json",
      },

      // Envia a mensagem digitada como JSON
      body: JSON.stringify({
        mensagem: mensagem,
      }),
    });


    if (!resposta.ok) {
      areaResposta.innerText = "Erro ao buscar resposta da IA";
      return;
    }

    // Converte a resposta do servidor para JSON
    const dados = await resposta.json();

    receitas = dados.resposta;

    mostrarCards(areaResposta);
  } catch (erro) {
    areaResposta.innerText = "Erro: resposta inválida";
  }
}

// Mstra os cards pequenos
function mostrarCards(areaResposta) {
  areaResposta.innerHTML = receitas
    .map((receita, index) => {
      if (receita.titulo === "Erro ao gerar receita") {
        return `
          <div class="card-receita card-erro">
            <h3 class="receita-titulo">Erro ao gerar receita</h3>
          </div>
        `;
      }

      return `
        <div class="card-receita" onclick="abrirReceita(${index})">
          <img
            class="receita-imagem"
            src="/static/img/food-placeholder.jpg"
            alt="Imagem da receita"
          >

          <h3 class="receita-titulo">${receita.titulo}</h3>

          <ul class="receita-resumo">
            <li>${receita.categoria || ""}</li>
            <li>${receita.tempo || ""}</li>
            <li>${receita.dificuldade || ""}</li>
            <li>${receita.rendimento || ""}</li>
          </ul>
        </div>
      `;
    })
    .join("");
}


function abrirReceita(index) {
  const areaResposta = document.getElementById("resposta-ia");

  // Pega a receita clicada pelo índice
  const receita = receitas[index];

  areaResposta.innerHTML = `
    <div class="card-receita card-receita-grande">
      <button class="botao-voltar" onclick="voltarCards()">Voltar</button>

      <h3 class="receita-titulo">${receita.titulo}</h3>

      <p><strong>Categoria:</strong> ${receita.categoria}</p>
      <p>${receita.descricao}</p>

      <div class="receita-info">
        <span>${receita.tempo}</span>
        <span>${receita.dificuldade}</span>
        <span>${receita.rendimento}</span>
      </div>

      <h4>Ingredientes</h4>
      <ul>
        ${receita.ingredientes.map((item) => `<li>${item}</li>`).join("")}
      </ul>

      <h4>Modo de preparo</h4>
      <ol>
        ${receita.modo_preparo.map((passo) => `<li>${passo}</li>`).join("")}
      </ol>
    </div>
  `;
}


function voltarCards() {
  const areaResposta = document.getElementById("resposta-ia");
  mostrarCards(areaResposta);
}
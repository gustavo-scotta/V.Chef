const botao = document.getElementById("botao-enviar");

botao.addEventListener("click", async () => {
  const mensagem = document.getElementById("mensagem").value;
  const areaResposta = document.getElementById("resposta-ia");

  areaResposta.innerText = "Preparando...";

  try {
    const resposta = await fetch("/mensagem", {
      method: "POST",

      // Informa ao Flask que os dados enviados estao em formato JSON
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        mensagem: mensagem,
      }),
    });

    if (!resposta.ok) {
      areaResposta.innerText = "Erro ao buscar resposta da IA";
      return;
    }

    // Tenta converter a resposta do servidor para JSON
    const dados = await resposta.json();
    // Mostra resposta IA

    areaResposta.innerHTML = dados.resposta
      .map(
        (receita) => `
          <div class="card-receita">
            <h3 class="receita-titulo">${receita.titulo}</h3>

            <p class="receita-linha">
              <strong>Categoria:</strong> ${receita.categoria}
            </p>

            <p class="receita-descricao">
              ${receita.descricao}
            </p>

            <div class="receita-info">
              <span>${receita.tempo}</span>
              <span>${receita.dificuldade}</span>
              <span>${receita.rendimento}</span>
            </div>

            <h4 class="receita-subtitulo">Ingredientes</h4>
            <ul class="receita-lista">
              ${receita.ingredientes
                .map(
                  (ingrediente) => `
                    <li>${ingrediente}</li>
                  `,
                )
                .join("")}
            </ul>

            <h4 class="receita-subtitulo">Modo de preparo</h4>
            <ol class="receita-lista">
              ${receita.modo_preparo
                .map(
                  (passo) => `
                    <li>${passo}</li>
                  `,
                )
                .join("")}
            </ol>
          </div>
        `,
      )
      .join("");
  } catch (erro) {
    areaResposta.innerText = "Erro: resposta inválida";
  }
});

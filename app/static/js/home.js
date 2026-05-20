const botao = document.getElementById("botao-enviar");

botao.addEventListener("click", async() => {
    const mensagem = document.getElementById("mensagem").value;

    const resposta = await fetch("/mensagem", {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        mensagem: mensagem
      })
    });

    const dados = await resposta.json();

    
    document.getElementById("resposta-ia").innerText = JSON.stringify(dados.resposta, null, 2);
})
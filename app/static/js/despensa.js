// Despensa: script exclusivo da pagina despensa.html.

// ALTERADO: removemos gerarId e localStorage.
// Agora o ID vem do banco de dados.

// ALTERADO: a lista começa vazia e será carregada do Flask.
let ingredientes = [];

let categoriaAtual = "Todos";

// Elementos principais manipulados pelo JS da Despensa.
const cards = document.getElementById("cards");

const pesquisa = document.getElementById("pesquisa");

const modalBg = document.getElementById("modalBg");

// ALTERADO: busca os ingredientes salvos no banco pelo Flask.
async function carregarIngredientes() {
  const resposta = await fetch("/api/despensa");

  ingredientes = await resposta.json();

  renderizar();
}

// Escolhe um emoji visual de acordo com a categoria do ingrediente.
function buscarEmoji(categoria) {
  const emojis = {
    Vegetais: "🥦",
    Frutas: "🍎",
    Carnes: "🍖",
    Temperos: "🧄",
    Laticínios: "🧀",
    Grãos: "🌾",
    Outros: "🍽️",
  };

  return emojis[categoria] || "🍽️";
}

// Faz uma classificacao simples pelo nome quando a categoria esta em automatico.
async function detectarIngrediente(nome) {
  nome = nome.toLowerCase();

  const categorias = {
    Vegetais: ["brocolis", "brócolis", "alface", "cenoura", "batata", "pepino"],

    Frutas: ["banana", "maçã", "maca", "uva", "laranja", "tomate"],

    Carnes: ["carne", "frango", "hamburguer", "hambúrguer", "peixe"],

    Temperos: ["alho", "cebola", "oregano"],
  };

  for (const categoria in categorias) {
    const encontrou = categorias[categoria].some((item) => nome.includes(item));

    if (encontrou) {
      return {
        categoria,
        emoji: buscarEmoji(categoria),
      };
    }
  }

  return {
    categoria: "Outros",
    emoji: "🍽️",
  };
}

// Monta o HTML de um card de ingrediente.
function criarCard(item) {
  return `

    <div class="card">

      <div>

        <div class="emoji">
          ${item.emoji}
        </div>

        <div class="nome">
          ${item.nome}
        </div>

        <div class="quantidade">
          ${item.quantidade} ${item.unidade}
        </div>

        <div class="categoria-texto">
          ${item.categoria}
        </div>

      </div>

      <div class="acoes-card">

        <button
          class="menos"
          data-id="${item.id}"
          aria-label="Remover unidade"
        >
          -
        </button>

        <button
          class="mais"
          data-id="${item.id}"
          aria-label="Adicionar unidade"
        >
          +
        </button>

      </div>

    </div>

  `;
}

// Mensagem mostrada quando nenhum ingrediente passa pelos filtros.
function criarMensagemVazia() {
  return `
    <div class="vazio">
      Nenhum ingrediente encontrado.
    </div>
  `;
}

// Aplica busca textual e filtro por categoria.
function filtrarIngredientes() {
  const textoPesquisa = pesquisa.value.toLowerCase();

  return ingredientes.filter((item) => {
    const nomeOk = item.nome.toLowerCase().includes(textoPesquisa);

    const categoriaOk =
      categoriaAtual === "Todos" || item.categoria === categoriaAtual;

    return nomeOk && categoriaOk;
  });
}

// Atualiza a grade de cards com os ingredientes filtrados.
function renderizar() {
  const filtrados = filtrarIngredientes();

  if (filtrados.length === 0) {
    cards.innerHTML = criarMensagemVazia();

    return;
  }

  let html = "";

  filtrados.forEach((item) => {
    html += criarCard(item);
  });

  cards.innerHTML = html;
}

// ALTERADO: incrementa a quantidade no banco de dados.
async function aumentar(id) {
  await fetch(`/api/despensa/${id}/aumentar`, {
    method: "POST",
  });

  await carregarIngredientes();
}

// ALTERADO: diminui a quantidade no banco.
// Se chegar a zero, o Flask remove do banco.
async function diminuir(id) {
  await fetch(`/api/despensa/${id}/diminuir`, {
    method: "POST",
  });

  await carregarIngredientes();
}

// Trata cliques nos botoes + e - dos cards.
cards.addEventListener("click", (e) => {
  const id = Number(e.target.dataset.id);

  if (e.target.classList.contains("mais")) {
    aumentar(id);
  }

  if (e.target.classList.contains("menos")) {
    diminuir(id);
  }
});

pesquisa.addEventListener("input", renderizar);

document.querySelectorAll(".categoria").forEach((botao) => {
  botao.addEventListener("click", () => {
    document
      .querySelectorAll(".categoria")
      .forEach((btn) => btn.classList.remove("ativa"));

    botao.classList.add("ativa");

    categoriaAtual = botao.dataset.categoria;

    renderizar();
  });
});

// Abre o modal de cadastro.
document.getElementById("abrirModal").addEventListener("click", () => {
  modalBg.style.display = "flex";
});

// Fecha o modal quando o usuario clica fora dele.
modalBg.addEventListener("click", (e) => {
  if (e.target === modalBg) {
    modalBg.style.display = "none";
  }
});

// Le os campos do modal e adiciona ou soma o ingrediente na lista.
document.getElementById("adicionarBtn").addEventListener("click", async () => {
  const nome = document.getElementById("nomeInput").value.trim();

  const categoriaManual = document.getElementById("categoriaSelect").value;

  const unidade = document.getElementById("unidadeSelect").value;

  const quantidade = Number(document.getElementById("quantidadeInput").value);

  if (nome === "") return;

  let info;

  if (categoriaManual === "Automático") {
    info = await detectarIngrediente(nome);
  } else {
    info = {
      categoria: categoriaManual,
      emoji: buscarEmoji(categoriaManual),
    };
  }

  // ALTERADO: em vez de ingredientes.push e localStorage,
  // envia o novo ingrediente para o Flask salvar no banco.
  await fetch("/api/despensa", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nome: nome,
      quantidade: quantidade,
      unidade: unidade,
      categoria: info.categoria,
      emoji: info.emoji,
    }),
  });

  fecharModal();

  // ALTERADO: depois de salvar, busca a lista atualizada do banco.
  await carregarIngredientes();
});

// Limpa os campos e esconde o modal apos salvar ou cancelar pelo fundo.
function fecharModal() {
  document.getElementById("nomeInput").value = "";

  document.getElementById("categoriaSelect").value = "Automático";

  document.getElementById("unidadeSelect").value = "unidades";

  document.getElementById("quantidadeInput").value = 1;

  modalBg.style.display = "none";
}

function somenteLetras(input) {
  input.value = input.value.replace(/[^A-Za-zÀ-ÿ\s]/g, "");
}

function somenteNumeros(input) {
  input.value = input.value.replace(/[^0-9]/g, "");
}

// Primeira renderizacao agora busca do banco.
carregarIngredientes();

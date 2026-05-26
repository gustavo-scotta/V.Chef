// NÃO GOSTA
function addTag() {
  const input = document.getElementById("foodInput");
  const value = input.value.trim();

  if (!value) return;

  const container = document.getElementById("tags-container");

  const tag = document.createElement("div");

  tag.className = "tag";

  tag.innerHTML = `
      ${value}

      <button
        class="tag-remove"
        onclick="removerNaoGosta(this)"
      >
        ×
      </button>
    `;

  container.appendChild(tag);

  input.value = "";
}

function removerNaoGosta(btn) {
  btn.closest(".tag").remove();
}

// RESTRIÇÕES
function addAllergy() {
  const input = document.getElementById("allergyInput");

  const value = input.value.trim();

  if (!value) return;

  const grid = document.getElementById("allergy-grid");

  const card = document.createElement("div");

  card.className = "toggle-card";

  card.innerHTML = `

      <span class="toggle-label">${value}</span>

      <button class="tag-remove-slider" onclick="removerRestricao(this)">
        ×
      </button>

      <label class="toggle-switch">

        <input type="checkbox"
        >
        <span class="slider"></span>

      </label>

    `;

  grid.appendChild(card);

  input.value = "";
}

function removerRestricao(btn) {
  btn.parentElement.remove();
}

// OBSERVAÇÕES
function addDiet() {
  const input = document.getElementById("dietInput");

  const value = input.value.trim();

  if (!value) return;

  const grid = document.getElementById("diet-grid");

  const card = document.createElement("div");

  card.className = "toggle-card";

  card.innerHTML = `

    <span class="toggle-label">${value}</span>
    <button class="tag-remove-slider" onclick="removerObservacao(this)">
      ×
    </button>

    <label class="toggle-switch">
      
      <input type="checkbox" checked>
      <span class="slider"></span>

    </label>

  `;

  grid.appendChild(card);

  input.value = "";
}

function removerObservacao(btn) {
  btn.parentElement.remove();
}

// SAVE
async function savePrefs() {
  // Busca todas as tags de "não gosto" que estão na tela.
  const naoGosta = [...document.querySelectorAll("#tags-container .tag")]
    .map((tag) => tag.childNodes[0].textContent.trim())
    .filter((nome) => nome);

  // Busca todos os cards de restrições que estão na tela.
  const restricoes = [
    ...document.querySelectorAll("#allergy-grid .toggle-card"),
  ].map((card) => {
    const input = card.querySelector("input[type='checkbox']");

    return {
      // Se já veio do banco, tem id.
      // Se foi criado agora na tela, ainda não tem id, então vai como null.
      id: input.dataset.id || null,

      nome: card.querySelector(".toggle-label").textContent.trim(),

      status: input.checked,
    };
  });

  // Busca todos os cards de observações que estão na tela.
  const observacoes = [
    ...document.querySelectorAll("#diet-grid .toggle-card"),
  ].map((card) => {
    const input = card.querySelector("input[type='checkbox']");

    return {
      id: input.dataset.id || null,

      // Pega o texto da observação.
      nome: card.querySelector(".toggle-label").textContent.trim(),

      // Pega se o switch/checkbox está ligado ou desligado.
      status: input.checked,
    };
  });

  // Esse é o pacote completo de preferências que será enviado para o Flask.
  const dados = {
    nao_gosta: naoGosta,
    restricoes: restricoes,
    observacoes: observacoes,
  };

  const response = await fetch("/preferencias/salvar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
  });

  if (!response.ok) {
    alert("Erro ao salvar preferências");
    return;
  }

  // Se salvou com sucesso, mostra o toast na tela.
  const toast = document.getElementById("toast");

  toast.classList.add("show");

  // Depois de 2,5 segundos, esconde o toast.
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2500);
}

// NÃO GOSTA
async function addTag() {
  const input = document.getElementById("foodInput");
  const value = input.value.trim();

  if (!value) return;

  const response = await fetch("/preferencias/nao-gosta", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nome: value,
    }),
  });

  const data = await response.json();

  const container = document.getElementById("tags-container");

  const tag = document.createElement("div");

  tag.className = "tag";

  tag.innerHTML = `
      ${data.nome}

      <button
        class="tag-remove"
        onclick="removerNaoGosta(this, ${data.id})"
      >
        ×
      </button>
    `;

  container.appendChild(tag);

  input.value = "";
}

async function removerNaoGosta(btn, id) {
  const response = await fetch(`/preferencias/nao-gosta/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    alert("Erro ao remover alimento");
    return;
  }

  btn.closest(".tag").remove();
}

// RESTRIÇÕES
async function addAllergy() {
  const input = document.getElementById("allergyInput");

  const value = input.value.trim();

  if (!value) return;

  const response = await fetch("/preferencias/restricao", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nome: value,
    }),
  });

  const data = await response.json();

  const grid = document.getElementById("allergy-grid");

  const card = document.createElement("div");

  card.className = "toggle-card";

  card.innerHTML = `

      <span class="toggle-label">${data.nome}</span>

      <button class="tag-remove-slider" onclick="removerRestricao(this, ${data.id})">
        ×
      </button>

      <label class="toggle-switch">

        <input type="checkbox"
        checked onchange="alterarStatusRestricao(${data.id}, this.checked)"
        >
        <span class="slider"></span>

      </label>

    `;

  grid.appendChild(card);

  input.value = "";
}

async function removerRestricao(btn, id) {
  const response = await fetch(`/preferencias/restricao/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    alert("Erro ao remover restrição");
    return;
  }

  btn.parentElement.remove();
}

// OBSERVAÇÕES
async function addDiet() {
  const input = document.getElementById("dietInput");

  const value = input.value.trim();

  if (!value) return;

  const response = await fetch("/preferencias/observacoes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nome: value,
    }),
  });

  const data = await response.json();

  const grid = document.getElementById("diet-grid");

  const card = document.createElement("div");

  card.className = "toggle-card";

  card.innerHTML = `

    <span class="toggle-label">${data.nome}</span>
    <button class="tag-remove-slider" onclick="removerObservacao(this, ${data.id})">
      ×
    </button>

    <label class="toggle-switch">
      
      <input type="checkbox"
      checked 
      onchange="alterarStatusObservacao(${data.id}, this.checked)">

      <span class="slider"></span>

    </label>

  `;

  grid.appendChild(card);

  input.value = "";
}

async function removerObservacao(btn, id) {
  const response = await fetch(`/preferencias/observacoes/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    alert("Erro ao remover restrição");
    return;
  }

  btn.parentElement.remove();
}

// Alterar status do SLIDE
async function alterarStatusRestricao(id, status) {
  await fetch("/preferencias/restricao/status", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: Number(id),
      status: status,
    }),
  });
}

async function alterarStatusObservacao(id, status) {
  await fetch("/preferencias/observacoes/status", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: Number(id),
      status: status,
    }),
  });
}

// SAVE
function savePrefs() {
  const toast = document.getElementById("toast");

  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 2500);
}

function somenteLetras(input) {
  input.value = input.value.replace(/[^A-Za-zÀ-ÿ\s]/g, "");
}

const input = document.getElementById("msgInput");
const sendBtn = document.getElementById("sendBtn");
const chat = document.getElementById("chat");

async function sendMessage() {

    const message = input.value.trim();

    if (!message) return;

    addUserMessage(message);

    input.value = "";

    showLoading();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        removeLoading();

        renderRecipes(data.response);

    } catch (error) {

        removeLoading();

        addBotMessage("Erro ao conectar com o servidor.");

        console.error(error);
    }
}


function addUserMessage(text) {

    const row = document.createElement("div");

    row.className = "msg-row user";

    row.innerHTML = `
        <div class="bubble user">
            ${text}
        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}


function addBotMessage(text) {

    const row = document.createElement("div");

    row.className = "msg-row bot";

    row.innerHTML = `
        <div class="bubble bot">
            ${text}
        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}


function renderRecipes(recipes) {

    const row = document.createElement("div");

    row.className = "msg-row bot";

    const cards = recipes.map(recipe => {

        return `
            <div class="recipe-card"
                 onclick='openRecipe(${JSON.stringify(recipe)})'>

                <img
                    src="/static/img/food-placeholder.jpg"
                    alt="${recipe.titulo}"
                >

                <div class="recipe-card-body">

                    <div class="recipe-card-title">
                        ${recipe.titulo}
                    </div>

                    <div class="recipe-card-desc">
                        ${recipe.descricao}
                    </div>

                    <div class="recipe-card-meta">

                        <span class="meta-tag">
                            ⏱ ${recipe.tempo}
                        </span>

                        <span class="meta-tag">
                            ⭐ ${recipe.dificuldade}
                        </span>

                    </div>

                </div>

            </div>
        `;
    }).join("");

    row.innerHTML = `
        <div class="cards-grid">
            ${cards}
        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}


function openRecipe(recipe) {

    const modal = document.createElement("div");

    modal.className = "recipe-modal";

    modal.innerHTML = `

        <div class="recipe-modal-content">

            <button class="close-modal"
                    onclick="this.parentElement.parentElement.remove()">
                ✕
            </button>

            <h2>${recipe.titulo}</h2>

            <p>
                <strong>Tempo:</strong> ${recipe.tempo}
            </p>

            <p>
                <strong>Dificuldade:</strong> ${recipe.dificuldade}
            </p>

            <br>

            <p>${recipe.descricao}</p>

            <br>

            <h3>Modo de preparo</h3>

            <ol>
                ${recipe.modo_preparo.map(
                    passo => `<li>${passo}</li>`
                ).join("")}
            </ol>

        </div>
    `;

    document.body.appendChild(modal);
}


function showLoading() {

    const row = document.createElement("div");

    row.className = "msg-row bot";

    row.id = "loading";

    row.innerHTML = `
        <div class="bubble bot">
            👨‍🍳 Preparando receitas...
        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}


function removeLoading() {

    const loading = document.getElementById("loading");

    if (loading) {
        loading.remove();
    }
}


function scrollBottom() {

    chat.scrollTop = chat.scrollHeight;
}


function sendChip(button) {

    input.value = button.innerText;

    sendMessage();
}


sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});
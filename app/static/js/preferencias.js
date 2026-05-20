// Preferencias: script exclusivo da pagina preferencias.html.

// Adiciona uma tag com alimento que o usuario nao gosta.
function addTag(){

  const input = document.getElementById('foodInput');

  const value = input.value.trim();

  if(!value) return;

  const container = document.getElementById('tags-container');

  const tag = document.createElement('div');

  tag.className = 'tag';

  tag.innerHTML = `
    ${value}
    <button class="tag-remove" onclick="removeTag(this)">
      ×
    </button>
  `;

  container.appendChild(tag);

  input.value = '';

}

// Remove a tag clicada pelo usuario.
function removeTag(btn){

  btn.parentElement.remove();

}

// Cria um card de restricao com switch liga/desliga.
function addAllergy(){

  const input = document.getElementById('allergyInput');

  const value = input.value.trim();

  if(!value) return;

  const grid = document.getElementById('allergy-grid');

  const card = document.createElement('div');

  card.className = 'toggle-card';

  card.innerHTML = `
  
    <span class="toggle-label">${value}</span>

    <label class="toggle-switch">
      <input type="checkbox">
      <span class="slider"></span>
    </label>

  `;

  grid.appendChild(card);

  input.value = '';

}

// Cria um card de observacao alimentar com switch liga/desliga.
function addDiet(){

  const input = document.getElementById('dietInput');

  const value = input.value.trim();

  if(!value) return;

  const grid = document.getElementById('diet-grid');

  const card = document.createElement('div');

  card.className = 'toggle-card';

  card.innerHTML = `
  
    <span class="toggle-label">${value}</span>

    <label class="toggle-switch">
      <input type="checkbox">
      <span class="slider"></span>
    </label>

  `;

  grid.appendChild(card);

  input.value = '';

}

// Exibe um toast simples confirmando a acao de salvar.
function savePrefs(){

  const toast = document.getElementById('toast');

  toast.classList.add('show');

  setTimeout(() => {

    toast.classList.remove('show');

  }, 2500);

}

// Enter nos campos executa o mesmo comportamento dos botoes de adicionar.
document.getElementById('foodInput').addEventListener('keydown', event => {
  if(event.key === 'Enter') addTag();
});

document.getElementById('allergyInput').addEventListener('keydown', event => {
  if(event.key === 'Enter') addAllergy();
});

document.getElementById('dietInput').addEventListener('keydown', event => {
  if(event.key === 'Enter') addDiet();
});

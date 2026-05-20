// Despensa: script exclusivo da pagina despensa.html.

// Gera um identificador simples para cada ingrediente salvo no navegador.
function gerarId(){

  return Date.now() + Math.floor(Math.random() * 1000);

}

// Persiste a lista atual de ingredientes no localStorage.
function salvarLocalStorage(){

  localStorage.setItem(
    'ingredientes',
    JSON.stringify(ingredientes)
  );

}

// Carrega ingredientes salvos ou cria exemplos iniciais para a primeira visita.
function carregarIngredientes(){

  const dados =
    localStorage.getItem('ingredientes');

  if(dados){

    return JSON.parse(dados);

  }

  return [

    {
      id:gerarId(),
      nome:'Tomate',
      quantidade:6,
      unidade:'unidades',
      categoria:'Frutas',
      emoji:'🍅'
    },

    {
      id:gerarId(),
      nome:'Frango',
      quantidade:2,
      unidade:'kg',
      categoria:'Carnes',
      emoji:'🍗'
    },

    {
      id:gerarId(),
      nome:'Alho',
      quantidade:500,
      unidade:'g',
      categoria:'Temperos',
      emoji:'🧄'
    },

    {
      id:gerarId(),
      nome:'Maçã',
      quantidade:4,
      unidade:'unidades',
      categoria:'Frutas',
      emoji:'🍎'
    }

  ];

}

let ingredientes = carregarIngredientes();

let categoriaAtual = 'Todos';

// Elementos principais manipulados pelo JS da Despensa.
const cards =
  document.getElementById('cards');

const pesquisa =
  document.getElementById('pesquisa');

const modalBg =
  document.getElementById('modalBg');

// Escolhe um emoji visual de acordo com a categoria do ingrediente.
function buscarEmoji(categoria){

  const emojis = {

    Vegetais:'🥦',
    Frutas:'🍎',
    Carnes:'🍖',
    Temperos:'🧄',
    Laticínios:'🧀',
    Grãos:'🌾',
    Outros:'🍽️'

  };

  return emojis[categoria] || '🍽️';

}

// Faz uma classificacao simples pelo nome quando a categoria esta em automatico.
async function detectarIngrediente(nome){

  nome = nome.toLowerCase();

  const categorias = {

    Vegetais:[
      'brocolis',
      'brócolis',
      'alface',
      'cenoura',
      'batata',
      'pepino'
    ],

    Frutas:[
      'banana',
      'maçã',
      'maca',
      'uva',
      'laranja',
      'tomate'
    ],

    Carnes:[
      'carne',
      'frango',
      'hamburguer',
      'hambúrguer',
      'peixe'
    ],

    Temperos:[
      'alho',
      'cebola',
      'oregano'
    ]

  };

  for(const categoria in categorias){

    const encontrou =
      categorias[categoria]
      .some(item => nome.includes(item));

    if(encontrou){

      return {
        categoria,
        emoji:buscarEmoji(categoria)
      };

    }

  }

  return {
    categoria:'Outros',
    emoji:'🍽️'
  };

}

// Monta o HTML de um card de ingrediente.
function criarCard(item){

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
function criarMensagemVazia(){

  return `
    <div class="vazio">
      Nenhum ingrediente encontrado.
    </div>
  `;

}

// Aplica busca textual e filtro por categoria.
function filtrarIngredientes(){

  const textoPesquisa =
    pesquisa.value.toLowerCase();

  return ingredientes.filter(item => {

    const nomeOk =
      item.nome
      .toLowerCase()
      .includes(textoPesquisa);

    const categoriaOk =
      categoriaAtual === 'Todos'
      || item.categoria === categoriaAtual;

    return nomeOk && categoriaOk;

  });

}

// Atualiza a grade de cards com os ingredientes filtrados.
function renderizar(){

  const filtrados =
    filtrarIngredientes();

  if(filtrados.length === 0){

    cards.innerHTML =
      criarMensagemVazia();

    return;

  }

  let html = '';

  filtrados.forEach(item => {

    html += criarCard(item);

  });

  cards.innerHTML = html;

}

// Incrementa a quantidade de um ingrediente.
function aumentar(id){

  const ingrediente =
    ingredientes.find(
      item => item.id === id
    );

  if(!ingrediente) return;

  ingrediente.quantidade++;

  salvarLocalStorage();

  renderizar();

}

// Diminui a quantidade ou remove o ingrediente quando chega a zero.
function diminuir(id){

  const ingrediente =
    ingredientes.find(
      item => item.id === id
    );

  if(!ingrediente) return;

  if(ingrediente.quantidade > 1){

    ingrediente.quantidade--;

  }
  else{

    ingredientes =
      ingredientes.filter(
        item => item.id !== id
      );

  }

  salvarLocalStorage();

  renderizar();

}

// Trata cliques nos botoes + e - dos cards.
cards.addEventListener('click', (e) => {

  const id =
    Number(e.target.dataset.id);

  if(e.target.classList.contains('mais')){

    aumentar(id);

  }

  if(e.target.classList.contains('menos')){

    diminuir(id);

  }

});

pesquisa.addEventListener(
  'input',
  renderizar
);

document.querySelectorAll('.categoria')
.forEach(botao => {

  botao.addEventListener('click', () => {

    document.querySelectorAll('.categoria')
    .forEach(btn =>
      btn.classList.remove('ativa')
    );

    botao.classList.add('ativa');

    categoriaAtual =
      botao.dataset.categoria;

    renderizar();

  });

});

// Abre o modal de cadastro.
document.getElementById('abrirModal')
.addEventListener('click', () => {

  modalBg.style.display = 'flex';

});

// Fecha o modal quando o usuario clica fora dele.
modalBg.addEventListener('click', (e) => {

  if(e.target === modalBg){

    modalBg.style.display = 'none';

  }

});

// Le os campos do modal e adiciona ou soma o ingrediente na lista.
document.getElementById('adicionarBtn')
.addEventListener('click', async () => {

  const nome =
    document.getElementById('nomeInput')
    .value
    .trim();

  const categoriaManual =
    document.getElementById('categoriaSelect')
    .value;

  const unidade =
    document.getElementById('unidadeSelect')
    .value;

  const quantidade =
    Number(
      document.getElementById('quantidadeInput').value
    );

  if(nome === '') return;

  const ingredienteExistente =
    ingredientes.find(item =>
      item.nome.toLowerCase()
      === nome.toLowerCase()
    );

  if(ingredienteExistente){

    ingredienteExistente.quantidade +=
      quantidade;

    salvarLocalStorage();

    fecharModal();

    renderizar();

    return;

  }

  let info;

  if(categoriaManual === 'Automático'){

    info =
      await detectarIngrediente(nome);

  }
  else{

    info = {
      categoria:categoriaManual,
      emoji:buscarEmoji(categoriaManual)
    };

  }

  ingredientes.push({

    id:gerarId(),
    nome:nome,
    quantidade:quantidade,
    unidade:unidade,
    categoria:info.categoria,
    emoji:info.emoji

  });

  salvarLocalStorage();

  fecharModal();

  renderizar();

});

// Limpa os campos e esconde o modal apos salvar ou cancelar pelo fundo.
function fecharModal(){

  document.getElementById('nomeInput').value = '';

  document.getElementById('categoriaSelect').value =
    'Automático';

  document.getElementById('unidadeSelect').value =
    'unidades';

  document.getElementById('quantidadeInput').value =
    1;

  modalBg.style.display = 'none';

}

// Primeira renderizacao ao carregar a pagina.
renderizar();

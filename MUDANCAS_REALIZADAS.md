# Mudanças realizadas no VChef

## 1. Barra de navegação movida para a base

A navegação visual que estava em `preferencias.html` foi movida para `app/templates/base.html`.

Agora todas as páginas que usam `{% extends 'base.html' %}` recebem a mesma barra com:

- Despensa
- Faça sua Receita
- Preferências

A aba ativa é definida pelo `request.endpoint`, então o Flask marca automaticamente qual página está aberta.

## 2. Preferências passou a usar a base

`app/templates/preferencias.html` deixou de ter HTML completo com `<!DOCTYPE html>`, `<head>` e `<body>`.

Agora ela usa:

- `base.html` para estrutura geral
- `preferencias.css` para estilo próprio
- `preferencias.js` para comportamento próprio

Isso evita duplicação de cabeçalho e corrige os caminhos estáticos para o padrão Flask com `url_for`.

## 3. Despensa foi corrigida para usar a base corretamente

`app/templates/despensa.html` tinha fechamento de `</body>` e `</html>` dentro de um template que já estendia a base.

Isso foi removido. A página agora contém apenas o conteúdo da despensa, e a base controla a estrutura HTML completa.

Também foi corrigida a chamada de script antigo `script.js`, que não existia, para `js/despensa.js`.

## 4. CSS separado por template

Os estilos foram organizados assim:

- `app/static/css/base.css`: layout geral, container, logo, perfil e barra de navegação
- `app/static/css/home.css`: chat, mensagens, cards de receita e modal de receita
- `app/static/css/despensa.css`: busca, categorias, cards de ingrediente e modal da despensa
- `app/static/css/preferencias.css`: tags, restrições, observações, switches e toast

O arquivo antigo `style.css` foi removido porque misturava estilos globais com estilos da Home.

## 5. JS separado por template

Os scripts ficaram organizados assim:

- `app/static/js/home.js`: envio de mensagens, resposta da IA e modal de receita
- `app/static/js/despensa.js`: ingredientes, filtros, localStorage e modal da despensa
- `app/static/js/preferencias.js`: tags, restrições, observações e toast de salvamento

O arquivo antigo `app.js` foi renomeado para `home.js`, pois ele era exclusivo da Home.

## 6. Comentários adicionados no código

Foram adicionados comentários nos templates, CSS e JavaScript explicando:

- Onde a navegação comum é montada
- Qual CSS e JS pertence a cada página
- O que cada seção visual faz
- O papel das funções principais em cada script

Esses comentários ajudam a entender a divisão do projeto sem precisar seguir todos os arquivos mentalmente.

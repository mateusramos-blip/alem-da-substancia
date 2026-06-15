# Além da Substância — Refatoração e Atualização

Este repositório contém o projeto "Além da Substância" com melhorias de legibilidade, estrutura, usabilidade e estilo visual.

## Visão geral

O objetivo desta refatoração foi tornar o front-end e o back-end mais fáceis de manter, melhorar a experiência do usuário e criar um visual mais suave e acessível.

## Changelog

### 1. Refatoração inicial
- Organizou `app.py` para um backend Flask mais claro, com rotas de API e acesso ao banco de dados melhor estruturados.
- Simplificou o JavaScript em `index.html` usando funções nomeadas e carregamento via `DOMContentLoaded`.
- Ajustou o CSS para usar variáveis, um esquema de cores suaves e componentes visuais mais consistentes.
- Adicionou `.gitignore` para excluir arquivos temporários, cache Python e pasta de dados locais.

### 2. UI e interação
- Atualizou a paleta de cores para um tom teal suave com gradientes harmônicos.
- Tornou os cards de vídeo clicáveis diretamente pelo preview, sem botão extra.
- Implementou scroll suave com snap entre seções.
- Centralizou o formulário de comentários para criar um layout mais equilibrado.
- Transformou informações de contato em links `tel:` e links de mapa `Google Maps`.

### 3. Ajustes de layout e containers
- Expandiu o container de comentários para uma largura maior e visual mais amplo.
- Garantiu que o formulário e o mural de depoimentos fiquem alinhados e mais fáceis de ler.

### 4. Animações e experiência
- Adicionou bordas animadas nos cards com um efeito wave em gradiente.
- Atualizou a animação para um ciclo mais perceptível e suave de 4 segundos.
- Implementou uma rolagem com easing no mouse, gerando uma sensação mais fluida e menos brusca.

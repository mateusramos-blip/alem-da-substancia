# Além da Substância — Refatoração

Este repositório contém o projeto "Além da Substância" com melhorias de legibilidade, estrutura e estilo.

## O que foi feito

- Refatorado `app.py` para melhorar a organização das rotas e o acesso ao banco de dados.
- Tornado o JavaScript em `index.html` mais legível com funções nomeadas e um único evento `DOMContentLoaded`.
- Corrigido o import da fonte Google e ajustado o link de navegação para a seção correta.
- Atualizado `style.css` para usar variáveis CSS, um esquema de cores 60-30-10 e um branco mais suave.
- Adicionado `.gitignore` para evitar arquivos temporários e a pasta de dados local.
- Criado este README para documentar as mudanças e facilitar futuras contribuições.

## Como testar localmente

1. Instale Python 3.
2. Abra o terminal na pasta deste projeto.
3. Execute:

```bash
python app.py
```

4. Abra no navegador:

```text
http://127.0.0.1:5000
```

## Sobre forks e commits no GitHub

Um "fork" é uma cópia de um repositório no GitHub que você pode modificar independentemente.

Se você quer enviar essas alterações para o projeto do seu amigo:

1. No GitHub, faça um fork do repositório original do seu amigo.
2. Configure seu repositório local para apontar para o fork como `origin`.
3. Crie um branch para as alterações (por exemplo, `ui-refactor`).
4. Faça `git add .`, `git commit -m "Refatoração e nova paleta de cores"` e `git push origin ui-refactor`.
5. Abra um Pull Request no GitHub.

## Observação

Este repositório ainda não estava inicializado com Git quando comecei, então o commit local foi criado aqui e você pode subir para um fork ou para o repositório do seu amigo.

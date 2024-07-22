# URL-shortener
***
Projeto da disciplina de Fundamentos de Redes de Computadores, do curso
Bacharelado em Sistemas de Informação - 
Instituto Federal de Alagoas.

**Equipe:**
 - [Esther de Freitas](github.com/estherdefreitas)
 - [Rodrigo Farias](github.com/rodrigo-farias10)
 - [Naomy](github.com/nlas2)
 - [Euber](github.com/euberskills)

*Objetivo:* construir o próprio serviço de encurtamento de URL desenvolvendo a própria comunicação por sockets 

*Linguagens utilizadas:* 
 - Backend: Python
 - Frontend: html, css, Javascript

*Como utilizar:* 

1) Baixar os arquivos do repositório https://github.com/estherdefreitas/URL-shortener

2) Abrir o arquivo main.py na IDE e executar o código. Este comando iniciará um servidor 
no modo de escuta.

3) Abrir o arquivo index.html utilizando um navegador web.

4) Copiar a URL de um site que se deseja encurtar e colar abaixo de "Enter URL".

5) Clicar no botão "Shorten". Isso irá gerar um link ao lado de "Shortened URL:"

6) Clicar em cima do link que apareceu. O link encurtado irá redirecionar para a página original.

Step Zero

Linguagens utilizadas: 
 - Backend: Python
 - Frontend: html, css, Javascript
IDE:
 - IDE: VSCode
 
Step 1: Criação de uma API REST

- AS URLs encurtadas e completas foram armazenadas localmente
- Foram utilizadas funções da biblioteca hashlib para gerar hash das URLs.
- A estrutura de resposta às requisições utilizadas foi JSON
- São retornados status HTTP (POST, GET, OPTIONS)

Step 2: Redirecionamento de URLs
- É utilizado o código 301 Found de status HTTP para redirecionamento
- O redirecionamento é realizado clicando no botão Shorten do front e clicando em cima do link gerado. 
- Para URLs inválidas é utilizado o código 404 Not Found.

Step 3: GUI
- Foi criado um front usando html, css e Javascript. Ao colar a URL a ser encurtada e clicar no botão Shorten, é gerado um link de redirecionamento. Ao clicar nesse link, há o redirecioamento para a URL original.

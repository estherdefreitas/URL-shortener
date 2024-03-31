# Desafio
# URL SHORTNER

# Objetivo: construir o próprio serviço de encurtamento de URL

# Observações: - guardar a url curta e a url que ela mapeia
#              - quando um cliente solitica a url curta, o serviço retorna
#                um código HTTP de redirecionamento, enviando ele para a URL
#                 longa.
#              - construir uma API REST para criar um encurtador de url e 
#                redirecionar a solicitação da url curta para a longa.
#              - criar um form (frontend) - opcional 
#              - Ideal - construir ambos junto com testes automatizados e
#                criar uma pipeline (CI/CD) para fazer o deploy de tudo
#                como um serviço para um provedor de nuvem (AWS, Azure ou 
#                Google Cloud)

# Passos:   
#   Passo Zero - decidir linguagem de programação e IDE
#              - nome do projeto: urlshortener   
#              - backend: python 
#              - frontend: django?
#              - IDE: VSCode
#         Passo 1- criar uma REST API que irá permitir o cliente adicionar
#                  uma URL para a lista de URLS que estão atualmente 
#                  encurtadas 
#              - banco de dado: SQL ou NoSQL? Redis?
#              - geração das chaves curtas: função hash?
#              - tornar um código de status HTTP quando a solicitação funciona
#                junto com a URL encurtada: usar estrutura JSON?
#              - API deve ser idempotente - só a primeira requisição de várias idênticas
#              - bônus: adicionar uma checagem para chaves da hash duplicadas

#          Passo 2 - redirecionar uma requisição do cliente para a URL encurtada
#                  - retornar o código de status HTTP (302 Found e o cabeçalho Location)
#                  - olhar formato de entrada e saída do exemplo
#          Passo 3 - adicionar requisição DELETE na REST API para deleter a URL encurtada
#                    se ela existe e não fazer nada se ela não existe
#                  - a chave e URL deletadas não devem existir na base de dados 
#          Passo 4 (Opcional) - criar o front e realizar testes conforme descrição do
#                    desafio
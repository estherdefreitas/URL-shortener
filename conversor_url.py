# Importação dos módulos necessários do Flask
from flask import Flask, request, jsonify, redirect
import hashlib

# Inicialização da aplicação Flask
app = Flask(__name__)

# Dicionário para armazenar os dados de URL curta e URL longa
url_shortener = {}

# Função para gerar um hash a partir de uma URL longa
def generate_hash(url):
    hash_object = hashlib.sha256(url.encode())
    return hash_object.hexdigest()[:8]

# Rota para encurtar uma URL longa
@app.route('/shorten', methods=['POST'])
def shorten_url():
    # Obter os dados JSON da solicitação POST
    data = request.get_json()
    long_url = data.get('long_url')
    
    # Verificar se o parâmetro 'long_url' está presente nos dados da solicitação
    if not long_url:
        return jsonify({'error': 'Missing long_url parameter'}), 400
    
    # Gerar um hash único para a URL longa
    url_hash = generate_hash(long_url)
    
    # Construir a URL curta usando o domínio local
    short_url = f'127.0.0.1:5000/{url_hash}'  # Domínio local - substituir se for hospedar
    
    # Armazenar os dados da URL curta e URL longa no dicionário
    url_shortener[url_hash] = {
        'long_url': long_url,
        'short_url': short_url
    }
    
    # Retornar a URL curta gerada como resposta à solicitação POST
    return jsonify({'short_url': short_url}), 201

# Rota para redirecionar para a URL longa correspondente ao hash fornecido
@app.route('/<url_hash>')
def redirect_to_long_url(url_hash):
    # Verificar se o hash fornecido está presente no dicionário de URL curta
    if url_hash not in url_shortener:
        return jsonify({'error': 'URL not found'}), 404
    
    # Obter a URL longa correspondente ao hash fornecido
    long_url = url_shortener[url_hash]['long_url']
    
    # Redirecionar para a URL longa
    return redirect(long_url, code=302)

# Executar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)

# Para testar o conversor
# Executar o script conversor_url.py - isso iniciará o servidor
# Abrir um outro terminal e executar o seguinte comando
# curl -X POST -H "Content-Type: application/json" -d '{"long_url": "https://www.exemplo.com/pagina/longa/aqui"}' http://127.0.0.1:5000/shorten
# O comando acima gerarar uma requisição POST no outro terminal e retornará o link encurtado
# Colando o link resultante no navegador, observa-se que o mesmo está funcionando
#
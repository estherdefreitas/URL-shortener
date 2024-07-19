import hashlib  # Biblioteca para criar hashes (resumos) de strings
import json  # Biblioteca para manipulação de dados JSON
import socket  # Biblioteca para comunicação de rede via sockets

url_shortener = {}  # Dicionário para armazenar os pares de hash e URLs originais
server_ip = '127.0.0.1'  # IP do servidor (localhost)
server_port = 8080  # Porta do servidor

def handle_request(data):
    # Decodifica os dados recebidos e separa-os em linhas
    request = data.decode('utf-8').split("\r\n")
    # Pega a primeira linha da requisição (linha de comando)
    request_line = request[0].split(" ")
    # Separa o método HTTP (POST, GET, etc.) e o caminho solicitado
    method = request_line[0]
    path = request_line[1]

    # Log de método e caminho
    print(f"Method: {method}, Path: {path}")

    # Responde às requisições OPTIONS para CORS (Cross-Origin Resource Sharing)
    if method == "OPTIONS":
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n"
            "Access-Control-Allow-Headers: Content-Type\r\n\r\n"
        )
        return response

    # Lida com requisições POST para encurtar URLs
    if method == "POST" and path == "/shorten":
        # Encontra o comprimento do conteúdo
        content_length = int([x for x in request if x.startswith("Content-Length:")][0].split(": ")[1])
        # Obtém o corpo da requisição
        body = data.decode('utf-8').split("\r\n\r\n")[1]
        # Converte o corpo de JSON para dicionário Python
        json_body = json.loads(body)
        # Obtém a URL original do corpo da requisição
        original_url = json_body['url']

        # Adiciona "http://" à URL se não estiver presente
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            original_url = "http://" + original_url

        # Cria um hash MD5 da URL e pega os primeiros 6 caracteres
        url_hash = hashlib.md5(original_url.encode()).hexdigest()[:6]
        # Cria a URL encurtada usando o hash
        shortened_url = f"http://{server_ip}:{server_port}/{url_hash}"
        
        # Armazena o par hash-URL original no dicionário
        url_shortener[url_hash] = original_url

        # Log de armazenamento
        print(f"Storing hash: {url_hash} -> {original_url}")
        
        # Prepara a resposta JSON com a URL encurtada
        response_body = json.dumps({'shortened_url': shortened_url})
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            f"Content-Length: {len(response_body)}\r\n\r\n{response_body}"
        )
        return response

    # Lida com requisições GET para redirecionar para a URL original
    elif method == "GET" and path.startswith("/"):
        # Extrai o hash da URL solicitada
        url_hash = path[1:]
        # Log de recuperação
        print(f"Retrieving for hash: {url_hash}")
        # Verifica se o hash existe no dicionário
        if url_hash in url_shortener:
            original_url = url_shortener[url_hash]
            # Log de URL encontrada
            print(f"Found original URL: {original_url}")
            # Resposta de redirecionamento 301 para a URL original
            response = (
                "HTTP/1.1 301 Moved Permanently\r\n"
                f"Location: {original_url}\r\n"
                "Access-Control-Allow-Origin: *\r\n\r\n"
            )
        else:
            # Log de URL não encontrada
            print("URL not found")
            # Resposta de erro 404 se o hash não for encontrado
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                "Content-Length: 13\r\n\r\nURL not found"
            )
        return response

    # Resposta de erro 404 para outras requisições
    return "HTTP/1.1 404 Not Found\r\n\r\n"

def start_server():
    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Associa o socket ao endereço e porta especificados
    server_socket.bind(('127.0.0.1', server_port))
    # Começa a escutar por conexões de entrada
    server_socket.listen(1)
    print(f"Server listening on port {server_port}")
    
    while True:
        # Aceita uma nova conexão
        client_socket, addr = server_socket.accept()
        # Recebe dados do cliente
        data = client_socket.recv(1024)
        if data:
            # Processa a requisição e obtém a resposta
            response = handle_request(data)
            # Envia a resposta para o cliente
            client_socket.sendall(response.encode('utf-8'))
        # Fecha a conexão com o cliente
        client_socket.close()

if __name__ == "__main__":
    # Inicia o servidor
    start_server()

import hashlib
import json
import socket

url_shortener = {}


def generate_hash(url):
    hash_object = hashlib.sha256(url.encode())
    return hash_object.hexdigest()[:8]


def shorten_url(long_url):
    url_hash = generate_hash(long_url)
    short_url = f'127.0.0.1:8080/{url_hash}'
    url_shortener[url_hash] = {
        'long_url': long_url,
        'short_url': short_url
    }
    return short_url


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode()
    if request_data:
        lines = request_data.split('\n')
        request_line = lines[0]
        method, path, _ = request_line.split(' ')

        if method == 'GET':
            if path == '/':
                with open('index.html', 'r') as file:
                    response_body = file.read()
                response_headers = f'HTTP/1.1 200 OK\nContent-Length: {len(response_body)}\n\n'
                response = response_headers + response_body
                client_socket.send(response.encode())
            elif path[1:] in url_shortener:
                long_url = url_shortener[path[1:]]['long_url']
                response_headers = f'HTTP/1.1 302 Found\nLocation: {long_url}\n\n'
                client_socket.send(response_headers.encode())
            else:
                response = 'HTTP/1.1 404 Not Found\n\n'
                client_socket.send(response.encode())

        elif method == 'POST':
            if path == '/shorten':
                try:
                    body_index = lines.index('\r')
                except ValueError:
                    body_index = None

                if body_index is not None and body_index + 1 < len(lines):
                    request_body = '\n'.join(lines[body_index + 1:])
                    if request_body.strip():
                        json_data = json.loads(request_body)
                        long_url = json_data.get('url')
                        if long_url:
                            if 'http' not in long_url[:4]:
                                long_url = 'https://' + long_url
                            response_data = json.dumps({'shortened_url': shorten_url(long_url)})
                            response_headers = f'HTTP/1.1 200 OK\nContent-Length: {len(response_data)}\n\n'
                            response = response_headers + response_data
                            client_socket.send(response.encode())
                            return
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\n'
                else:
                    response = 'HTTP/1.1 400 Bad Request\n\n'
                    client_socket.send(response.encode())
            else:
                response = 'HTTP/1.1 404 Not Found\n\n'
                client_socket.send(response.encode())

    client_socket.close()


def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f'Server listening on {host}:{port}...')

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Connection from {client_address}')
            handle_request(client_socket)
    except KeyboardInterrupt:
        print('Server shutting down...')
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()

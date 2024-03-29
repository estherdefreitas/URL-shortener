#!/usr/bin/env python3

# Script que age como cliente - fica esperando, escutando e aceitando conexões

import socket

HOST = '127.0.0.1'
PORT = 50000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET (endereço IPV4) SOCK_STREAM - TCP
s.connect((HOST,PORT)) # conecta um cliente a um endereço
s.sendall(str.encode('Bom dia Rodrigo')) # envia todos os bytes passados como parametro
data = s.recv(1024) # lê os bytes recebidos, retornando-os como string até o limite buffsize

print('Mensagem ecoada: ', data.decode())


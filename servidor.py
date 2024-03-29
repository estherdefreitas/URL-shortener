#!/usr/bin/env python3

# Script que age como servidor - fica esperando, escutando e aceitando conexões

import socket # fornece interface para API de sockets BSD

HOST = 'localhost' # armazena ip ou nome da máquina
PORT = 50000 #número de porta - colocar elevado pra não ter interferências

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCK_STREAM -TCP
s.bind((HOST, PORT))  # vincula porta com endereço IP
s.listen() # escutar - quando o servidor tá esperando uma conexão 
print('Aguardando conexão de um cliente')
conn, ender = s.accept() # aceita uma conexão de cliente

print('Conectado em', ender)

while True: 
	data=conn.recv(1024) # lê os bytes recebidos, retornando-os como string até o limite buffsize
	if not data:
		print('Fechando a conexão')
		conn.close() # fecha um socket, liberando todos os recursos alocados
		break
	conn.sendall(data) # envia todos os bytes passados como parâmetro
	

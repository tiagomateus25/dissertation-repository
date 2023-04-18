#!/usr/bin/env python3

import socket
import json
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.56.237', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
print('Waiting for communication.')
# Listen for incoming connections
sock.listen(1)
# connection, client_address = sock.accept()

while True:

    connection, client_address = sock.accept()

    # Receive the data in small chunks and retransmit it
    data = connection.recv(1024)
    # data = json.loads(data.decode())
    # print(type(data))

    print('Value received: ', data.decode('utf8'))
    # print('Value received: ', json.loads(data.decode()))

    # time.sleep(1)
    # connection.close()
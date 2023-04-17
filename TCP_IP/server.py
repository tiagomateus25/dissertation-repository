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

# Listen for incoming connections
sock.listen(1)

while True:

    connection, client_address = sock.accept()

    # Receive the data in small chunks and retransmit it
    data = connection.recv(5000)
    data = json.loads(data.decode())
    print('Value received: ', data)
    time.sleep(0.01)